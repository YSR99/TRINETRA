import cv2
import dlib
import numpy as np
from scipy.signal import butter, lfilter
from collections import deque

# ---------------------------
# Setup and Initialization
# ---------------------------

# Load dlib models
face_detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # Ensure this file is in your working directory

# Bandpass filter settings for heart rate frequencies (0.7–3 Hz)
fs = 30  # Frame rate (Hz)
low = 0.7 / (fs / 2)
high = 3.0 / (fs / 2)
b, a = butter(4, [low, high], btype='bandpass')

# Global variables for filtering and buffering signals
zi_green = np.zeros(max(len(a), len(b)) - 1)
zi_red = np.zeros(max(len(a), len(b)) - 1)
signal_buffer = deque(maxlen=300)         # Buffer used for FFT analysis (~10 sec at 30 FPS)
heart_rate_buffer = deque(maxlen=10)        # For smoothing heart rate estimates
heart_rate_history = deque(maxlen=60)       # History for live graph display (last minute)
green_history = deque(maxlen=200)           # History of filtered green channel values
red_history = deque(maxlen=200)             # History of filtered red channel values
frame_counter = 0
alpha = 10  # Amplification factor

# ---------------------------
# ROI and Channel Processing
# ---------------------------

def get_rois(frame):
    """
    Detect the face and define regions of interest (ROIs) for the forehead and cheeks.
    Draws rectangles on the frame.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector(gray)
    if not faces:
        cv2.putText(frame, "No face detected", (10, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        return None, None, frame
    face = faces[0]
    landmarks = shape_predictor(gray, face)
    points = np.array([[p.x, p.y] for p in landmarks.parts()])
    
    # Define forehead ROI (from top of face to the mean y-coordinate of the eyebrows)
    forehead_top = face.top()
    forehead_bottom = int(np.mean(points[17:27, 1]))
    forehead_left, forehead_right = face.left(), face.right()
    cv2.rectangle(frame, (forehead_left, forehead_top), (forehead_right, forehead_bottom), (0, 255, 0), 2)
    
    # Define combined ROI (includes forehead and cheeks)
    x_min = max(0, min(forehead_left, points[2][0], points[14][0]))
    x_max = min(frame.shape[1], max(forehead_right, points[2][0], points[14][0]))
    y_min = max(0, forehead_top)
    y_max = min(frame.shape[0], max(forehead_bottom, points[48][1], points[54][1]))
    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
    
    roi = frame[y_min:y_max, x_min:x_max]
    return roi, (x_min, y_min, x_max, y_max), frame

def get_channel_averages(roi, frame):
    """
    Extract the average green and red channel values from the ROI.
    Also displays small resized versions of these channel images in the top-left.
    """
    if roi is None or roi.size == 0:
        return None, None, frame
    green_channel = roi[:, :, 1]
    red_channel = roi[:, :, 2]
    avg_green = np.mean(green_channel)
    avg_red = np.mean(red_channel)
    
    # Visualize the channels
    green_img = np.zeros_like(roi)
    green_img[:, :, 1] = green_channel
    red_img = np.zeros_like(roi)
    red_img[:, :, 2] = red_channel
    green_resized = cv2.resize(green_img, (100, 100))
    red_resized = cv2.resize(red_img, (100, 100))
    frame[0:100, 0:100] = green_resized
    frame[0:100, 100:200] = red_resized
    cv2.putText(frame, "Green", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.putText(frame, "Red", (110, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    
    return avg_green, avg_red, frame

# ---------------------------
# Signal Processing
# ---------------------------

def filter_signal(avg_green, avg_red):
    """
    Apply the bandpass filter to the average channel values.
    """
    global zi_green, zi_red
    if avg_green is None or avg_red is None:
        return None, None
    filtered_green, zi_green = lfilter(b, a, [avg_green], zi=zi_green)
    filtered_red, zi_red = lfilter(b, a, [avg_red], zi=zi_red)
    return filtered_green[0], filtered_red[0]

def amplify_signal(avg_green, filtered_green, avg_red, filtered_red):
    """
    Amplify subtle changes using an Eulerian Video Magnification style approach.
    """
    if filtered_green is None or filtered_red is None:
        return None, None
    amplified_green = avg_green + alpha * filtered_green
    amplified_red = avg_red + alpha * filtered_red
    return amplified_green, amplified_red

def get_heart_rate(amplified_green, amplified_red):
    """
    Compute the heart rate using FFT on the difference between amplified red and green signals.
    The signal is detrended and multiplied by a Hamming window before performing the FFT.
    """
    global frame_counter, signal_buffer
    if amplified_green is None or amplified_red is None:
        return None
    # Use the difference signal (red minus green)
    signal = amplified_red - amplified_green
    signal_buffer.append(signal)
    frame_counter += 1

    # Update heart rate estimate once every second (30 frames)
    if frame_counter % 30 == 0 and len(signal_buffer) > 10:
        signal_array = np.array(signal_buffer)
        # Detrend and apply a Hamming window to reduce spectral leakage
        signal_array = signal_array - np.mean(signal_array)
        window = np.hamming(len(signal_array))
        fft_result = np.fft.fft(signal_array * window)
        frequencies = np.fft.fftfreq(len(signal_array), d=1/fs)
        
        # Consider only positive frequencies within the heart rate band (0.7–3 Hz)
        positive_idx = np.where(frequencies >= 0)
        positive_freqs = frequencies[positive_idx]
        magnitudes = np.abs(fft_result[positive_idx])
        valid_mask = (positive_freqs > 0.7) & (positive_freqs < 3)
        if not np.any(valid_mask):
            return None
        valid_freqs = positive_freqs[valid_mask]
        valid_mags = magnitudes[valid_mask]
        dominant_freq = valid_freqs[np.argmax(valid_mags)]
        bpm = dominant_freq * 60  # Convert Hz to beats per minute
        return bpm
    return None

def smooth_heart_rate(heart_rate):
    """
    Smooth the heart rate estimation using a moving average filter.
    """
    global heart_rate_buffer
    if heart_rate is not None:
        heart_rate_buffer.append(heart_rate)
    return np.mean(heart_rate_buffer) if heart_rate_buffer else None

# ---------------------------
# Visualization
# ---------------------------

def display_visualizations(frame, roi_coords, smoothed_heart_rate, filtered_green, filtered_red):
    """
    Overlay the heart rate text onto the frame and reorganize all graphs
    into a dedicated strip at the bottom of the output image.
    This strip contains two panels:
      - Left: Live heart rate history.
      - Right: Filtered signal plots for green and red channels.
    """
    global heart_rate_history, green_history, red_history

    frame_height, frame_width = frame.shape[:2]
    
    # Overlay heart rate measurement on the main frame (top-right)
    if smoothed_heart_rate is not None:
        cv2.putText(frame, f"Heart Rate: {int(smoothed_heart_rate)} bpm", 
                    (frame_width - 350, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
    
    # Extend the frame with a black strip at the bottom for graphs
    graph_strip_height = 150
    canvas = np.zeros((frame_height + graph_strip_height, frame_width, 3), dtype=np.uint8)
    canvas[:frame_height, :] = frame

    # --- Left Panel: Heart Rate History Graph ---
    history_panel_width = frame_width // 2
    history_graph = np.zeros((graph_strip_height, history_panel_width, 3), dtype=np.uint8)
    if smoothed_heart_rate is not None:
        heart_rate_history.append(smoothed_heart_rate)
    if len(heart_rate_history) > 1:
        # Define a reasonable heart rate range for normalization (e.g., 40 to 200 bpm)
        hr_min, hr_max = 40, 200
        hr_range = hr_max - hr_min
        num_points = len(heart_rate_history)
        for i in range(1, num_points):
            x1 = int((i - 1) * (history_panel_width / num_points))
            x2 = int(i * (history_panel_width / num_points))
            y1 = int(graph_strip_height - ((heart_rate_history[i - 1] - hr_min) / hr_range * graph_strip_height))
            y2 = int(graph_strip_height - ((heart_rate_history[i] - hr_min) / hr_range * graph_strip_height))
            cv2.line(history_graph, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(history_graph, "HR History", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    # --- Right Panel: Filtered Signal Graphs ---
    signal_panel_width = frame_width - history_panel_width
    signal_graph = np.zeros((graph_strip_height, signal_panel_width, 3), dtype=np.uint8)
    # Append current filtered values to history (if available)
    if filtered_green is not None and filtered_red is not None:
        green_history.append(filtered_green)
        red_history.append(filtered_red)
    if len(green_history) > 1:
        num_points = len(green_history)
        scale_factor = 100  # adjust scaling for visualization
        for i in range(1, num_points):
            x1 = int((i - 1) * (signal_panel_width / num_points))
            x2 = int(i * (signal_panel_width / num_points))
            # For green channel
            y1_g = int(graph_strip_height / 2 - green_history[i - 1] * scale_factor)
            y2_g = int(graph_strip_height / 2 - green_history[i] * scale_factor)
            # For red channel
            y1_r = int(graph_strip_height / 2 - red_history[i - 1] * scale_factor)
            y2_r = int(graph_strip_height / 2 - red_history[i] * scale_factor)
            # Clamp y-values to the graph height
            y1_g = np.clip(y1_g, 0, graph_strip_height - 1)
            y2_g = np.clip(y2_g, 0, graph_strip_height - 1)
            y1_r = np.clip(y1_r, 0, graph_strip_height - 1)
            y2_r = np.clip(y2_r, 0, graph_strip_height - 1)
            cv2.line(signal_graph, (x1, y1_g), (x2, y2_g), (0, 255, 0), 1)
            cv2.line(signal_graph, (x1, y1_r), (x2, y2_r), (0, 0, 255), 1)
    cv2.putText(signal_graph, "Filtered Signals", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    # Place the two panels in the bottom strip
    canvas[frame_height:frame_height + graph_strip_height, 0:history_panel_width] = history_graph
    canvas[frame_height:frame_height + graph_strip_height, history_panel_width:] = signal_graph

    cv2.imshow("Heart Rate Monitor", canvas)

# ---------------------------
# Main Loop
# ---------------------------

cap = cv2.VideoCapture(1)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Process frame: detect face and extract ROI
    roi, roi_coords, frame = get_rois(frame)
    # Get average channel values from ROI
    avg_green, avg_red, frame = get_channel_averages(roi, frame)
    # Filter the signals
    filtered_green, filtered_red = filter_signal(avg_green, avg_red)
    # Amplify subtle changes
    amplified_green, amplified_red = amplify_signal(avg_green, filtered_green, avg_red, filtered_red)
    # Compute heart rate from amplified signals
    heart_rate = get_heart_rate(amplified_green, amplified_red)
    # Smooth the heart rate estimate
    smoothed_heart_rate = smooth_heart_rate(heart_rate)
    
    # Update visualizations (graphs and overlays)
    display_visualizations(frame, roi_coords, smoothed_heart_rate, filtered_green, filtered_red)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
