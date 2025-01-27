import cv2
import mediapipe as mp
import time
import numpy as np

class FaceDetector():
    def __init__(self, minDetectionCon=0.5):
        self.minDetectionCon = minDetectionCon
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon)

    def findFaces(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)
        bboxs = []
        if self.results.detections:
           for id, detection in enumerate(self.results.detections):
             bboxC = detection.location_data.relative_bounding_box
             ih, iw, ic = img.shape
             bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
             bboxs.append([id, bbox, detection.score])
             if draw:
              img = self.fancyDraw(img, bbox)

             cv2.putText(img, f'{int(detection.score[0] * 100)}%',
                        (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
                        2, (255, 0, 255), 2)

        return img, bboxs

    def fancyDraw(self, img, bbox, l=30, t=5, rt= 1):
        x, y, w, h = bbox
        x1, y1 = x + w, y + h

        cv2.rectangle(img, bbox, (255, 0, 255), rt)
        # Top Left  x,y
        cv2.line(img, (x, y), (x + l, y), (255, 0, 255), t)
        cv2.line(img, (x, y), (x, y+l), (255, 0, 255), t)
        # Top Right  x1,y
        cv2.line(img, (x1, y), (x1 - l, y), (255, 0, 255), t)
        cv2.line(img, (x1, y), (x1, y+l), (255, 0, 255), t)
        # Bottom Left  x,y1
        cv2.line(img, (x, y1), (x + l, y1), (255, 0, 255), t)
        cv2.line(img, (x, y1), (x, y1 - l), (255, 0, 255), t)
        # Bottom Right  x1,y1
        cv2.line(img, (x1, y1), (x1 - l, y1), (255, 0, 255), t)
        cv2.line(img, (x1, y1), (x1, y1 - l), (255, 0, 255), t)
        return img

def build_gaussian_pyramid(frame, levels):
    pyramid = [frame]
    for _ in range(levels):
        frame = cv2.pyrDown(frame)
        pyramid.append(frame)
    return pyramid

def temporal_ideal_filter(video_frames, low, high, fps, axis=0):
    fft = np.fft.fft(video_frames, axis=axis)
    frequencies = np.fft.fftfreq(video_frames.shape[axis], d=1.0 / fps)

    # Bandpass filter mask
    mask = (frequencies > low) & (frequencies < high)
    fft *= mask

    # Apply inverse FFT and return the real part
    filtered = np.fft.ifft(fft, axis=axis)
    return np.real(filtered)

def amplify_video(video, amplification):
    return video * amplification

def reconstruct_video(amplified, original, levels):
    for _ in range(levels):
        amplified = cv2.pyrUp(amplified)
        if amplified.shape[:2] != original.shape[:2]:
            amplified = cv2.resize(amplified, (original.shape[1], original.shape[0]))
    return amplified + original

def process_frame(frame, low, high, levels, amplification, fps):
    pyramid = build_gaussian_pyramid(frame, levels)
    gaussian_frame = pyramid[-1]

    temporal_filtered = temporal_ideal_filter(
        np.expand_dims(gaussian_frame, axis=0), low, high, fps, axis=0
    )
    amplified_frame = amplify_video(temporal_filtered, amplification)
    reconstructed_frame = reconstruct_video(
        amplified_frame[0], frame, levels
    )  # Reconstruct from the pyramid
    return reconstructed_frame

def magnify_webcam_with_rgb_channels(low=0.4, high=3.0, levels=4, amplification=20, fps=30):
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    pTime = 0
    detector = FaceDetector()

    while True:
        success, img = cap.read()
        if not success:
            print("Error: Could not read frame.")
            break

        img, bboxs = detector.findFaces(img)
        print(bboxs)

        for bbox in bboxs:
            x, y, w, h = bbox[1]

            # Extract RGB channels from the ROI (face region)
            face_roi = img[y:y+h, x:x+w]
            b_channel, g_channel, r_channel = cv2.split(face_roi)

            # Create RGB visualizations for each channel
            red_frame = cv2.merge([np.zeros_like(b_channel), np.zeros_like(g_channel), r_channel])
            green_frame = cv2.merge([np.zeros_like(b_channel), g_channel, np.zeros_like(r_channel)])
            blue_frame = cv2.merge([b_channel, np.zeros_like(g_channel), np.zeros_like(r_channel)])

            # Apply Eulerian magnification to the face region
            face_roi_float = face_roi.astype(np.float32) / 255.0
            amplified_face_roi = process_frame(face_roi_float, low, high, levels, amplification, fps)
            amplified_face_roi = np.clip(amplified_face_roi * 255, 0, 255).astype(np.uint8)

            # Replace the original face region with the amplified version
            img[y:y+h, x:x+w] = amplified_face_roi

            # Display the RGB channels of the face region
            cv2.imshow("Red Channel (ROI)", red_frame)
            cv2.imshow("Green Channel (ROI)", green_frame)
            cv2.imshow("Blue Channel (ROI)", blue_frame)

        # Show the normal footage
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)
        cv2.imshow("Normal Footage", img)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' key to exit
            break

    cap.release()
    cv2.destroyAllWindows()

# Run the magnification with RGB channel visualization
if __name__ == "__main__":
    magnify_webcam_with_rgb_channels(low=0.4, high=3.0, levels=4, amplification=20, fps=30)
