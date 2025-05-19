<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TriNetraa: Contactless Heart-Rate Monitoring System</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        /* Global Styles */
        body {
            font-family: 'Poppins', sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background-color: #f0f4f8;
            color: #2c3e50;
        }
        .container {
            max-width: 1000px;
            margin: 40px auto;
            padding: 30px;
            background: #ffffff;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        h1, h2, h3 {
            color: #e84393;
            margin-bottom: 15px;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
        }
        h1 {
            font-size: 3em;
            text-align: center;
            background: linear-gradient(45deg, #e84393, #00cec9);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: fadeIn 2s ease-in-out;
        }
        h2 {
            font-size: 2em;
            border-bottom: 3px solid #00cec9;
            padding-bottom: 10px;
            position: relative;
        }
        h2::after {
            content: '';
            position: absolute;
            bottom: -3px;
            left: 0;
            width: 50px;
            height: 3px;
            background: #e84393;
            animation: slideIn 1s ease-in-out;
        }
        h3 {
            font-size: 1.6em;
            color: #00cec9;
        }
        p, li {
            font-size: 1.1em;
            margin-bottom: 10px;
        }
        ul {
            list-style: none;
            padding-left: 0;
        }
        ul li {
            padding: 10px 0;
            position: relative;
            padding-left: 40px;
            transition: transform 0.3s ease;
        }
        ul li:hover {
            transform: translateX(10px);
        }
        ul li::before {
            content: "🌟";
            position: absolute;
            left: 0;
            color: #e84393;
            font-size: 1.5em;
        }
        a {
            color: #0984e3;
            text-decoration: none;
            transition: color 0.3s, transform 0.3s;
        }
        a:hover {
            color: #e84393;
            text-decoration: underline;
            transform: scale(1.05);
        }
        code {
            background: #dfe6e9;
            padding: 3px 8px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
        }
        pre {
            background: #2d3436;
            color: #dfe6e9;
            padding: 20px;
            border-radius: 10px;
            overflow-x: auto;
            font-size: 1em;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        }
        img.banner {
            width: 100%;
            max-height: 250px;
            object-fit: cover;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            animation: fadeIn 2s ease-in-out;
        }
        .section-divider {
            border: 0;
            height: 2px;
            background: linear-gradient(to right, #00cec9, #e84393);
            margin: 40px 0;
            animation: expand 1s ease-in-out;
        }
        .team-list li::before {
            content: "👤";
            font-size: 1.5em;
        }
        .emoji {
            font-size: 1.5em;
            margin-right: 10px;
        }
        .footer {
            text-align: center;
            font-size: 1em;
            color: #636e72;
            margin-top: 50px;
            padding: 30px;
            background: #dfe6e9;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes slideIn {
            from { width: 0; }
            to { width: 50px; }
        }
        @keyframes expand {
            from { width: 0; }
            to { width: 100%; }
        }
        /* Responsive Design */
        @media (max-width: 768px) {
            .container {
                margin: 20px;
                padding: 20px;
            }
            h1 {
                font-size: 2.5em;
            }
            h2 {
                font-size: 1.8em;
            }
            img.banner {
                max-height: 200px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1><span class="emoji">🌟</span> TriNetraa: Contactless Heart-Rate Monitoring System <span class="emoji">🌟</span></h1>
        <img src="https://via.placeholder.com/800x200.png?text=TriNetraa+Heart+Rate+Monitor" alt="TriNetraa Banner" class="banner">
        <p><em>Non-invasive heart rate monitoring using advanced computer vision and AI techniques.</em></p>
        
        <hr class="section-divider">

        <h2><span class="emoji">📖</span> Overview</h2>
        <p><strong>TriNetraa</strong> is an innovative, contactless heart-rate monitoring system that leverages computer vision and AI to analyze micro-movements in the red and green color channels of video footage. By detecting subtle systolic and diastolic signals, TriNetraa provides reliable heart rate estimates, even at low frame rates. This project offers a cost-effective, scalable, and non-invasive alternative to traditional heart rate monitoring methods, making it suitable for remote healthcare, clinical environments, and personal wellness applications.</p>
        
        <h3><span class="emoji">🎯</span> Problem Statement</h3>
        <p>Traditional heart rate monitoring often requires physical contact (e.g., pulse oximeters, ECGs), which can be costly, uncomfortable, or impractical for continuous use. TriNetraa addresses these limitations by:</p>
        <ul>
            <li>Utilizing webcam-based video analysis for non-invasive monitoring.</li>
            <li>Employing advanced signal processing to detect heart rate from facial micro-movements.</li>
            <li>Providing a scalable solution for both remote and clinical settings.</li>
        </ul>

        <h3><span class="emoji">✨</span> Key Features</h3>
        <ul>
            <li><strong>Contactless Monitoring</strong>: Estimates heart rate without physical sensors using a standard webcam.</li>
            <li><strong>Advanced Signal Processing</strong>: Uses Eulerian Video Magnification and FFT to analyze red-green channel differences.</li>
            <li><strong>Real-Time Visualization</strong>: Displays ROIs, heart rate (bpm), and signal graphs in a user-friendly interface.</li>
            <li><strong>Robust Performance</strong>: Reliable at low frame rates and in stable lighting conditions.</li>
            <li><strong>Open-Source</strong>: Freely available for research, education, and personal use.</li>
        </ul>

        <hr class="section-divider">

        <h2><span class="emoji">👥</span> Team TriNetraa</h2>
        <p>We are a passionate group of innovators from VIT Bhopal University, working together to revolutionize health monitoring:</p>
        <ul class="team-list">
            <li><strong>Ujjwal Mishra</strong> (22BAI70666) - <em>Project Lead & Computer Vision Expert</em></li>
            <li><strong>Rishikesh Shukla</strong> (22BAI70612) - <em>Signal Processing Specialist</em></li>
            <li><strong>Purvansh Kaishtha</strong> (22BAI70621) - <em>AI Algorithm Developer</em></li>
            <li><strong>Shivam Mehta</strong> (22BAI70606) - <em>Frontend & Visualization Designer</em></li>
            <li><strong>Yuvraj Rana</strong> (22BAI706771) - <em>System Integration & Testing</em></li>
        </ul>

        <hr class="section-divider">

        <h2><span class="emoji">🛠️</span> Installation</h2>
        <p>Follow these steps to set up TriNetraa on your system.</p>

        <h3><span class="emoji">📋</span> Prerequisites</h3>
        <ul>
            <li><strong>Hardware</strong>: Computer with a 2.5 GHz dual-core CPU and 4 GB RAM, USB webcam (640x480, ~30 FPS), 1 GB free disk space.</li>
            <li><strong>Software</strong>: Python 3.8+, Windows 10/11, macOS 10.15+, or Ubuntu 20.04+, CMake, and a C++ compiler.</li>
        </ul>

        <h3><span class="emoji">📦</span> Dependencies</h3>
        <p>TriNetraa requires the following Python libraries (listed in <code>requirements.txt</code>):</p>
        <pre>
opencv-python>=4.5.5.64
dlib>=19.22.0
numpy>=1.19.5
scipy>=1.7.3
        </pre>

        <h3><span class="emoji">🚀</span> Installation Steps</h3>
        <ol>
            <li><strong>Clone the Repository</strong>:
                <pre>git clone https://github.com/TriNetraa/heart-rate-monitor.git
cd heart-rate-monitor</pre>
            </li>
            <li><strong>Set Up a Virtual Environment</strong>:
                <pre>python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate</pre>
            </li>
            <li><strong>Install Dependencies</strong>:
                <pre>pip install -r requirements.txt</pre>
                <p><strong>Note</strong>: dlib may require CMake and a C++ compiler. For GPU support, install CUDA/cuDNN and use <code>pip install dlib --verbose</code>.</p>
            </li>
            <li><strong>Download dlib Shape Predictor</strong>:
                <p>Download <a href="http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2">shape_predictor_68_face_landmarks.dat.bz2</a>, extract to <code>shape_predictor_68_face_landmarks.dat</code>, and place in the project directory.</p>
            </li>
            <li><strong>Verify Setup</strong>:
                <pre>python -c "import cv2, dlib, numpy, scipy.signal; print('All libraries imported successfully!')"</pre>
            </li>
        </ol>

        <h3><span class="emoji">📂</span> Project Structure</h3>
        <pre>
heart-rate-monitor/
├── heart_rate_monitor.py           # Main script
├── shape_predictor_68_face_landmarks.dat  # dlib model
├── requirements.txt                # Dependencies
├── README.md                       # Documentation
├── venv/                           # Virtual environment
        </pre>

        <hr class="section-divider">

        <h2><span class="emoji">🎮</span> Usage</h2>
        <h3><span class="emoji">🏃‍♂️</span> Running TriNetraa</h3>
        <ol>
            <li>Connect a webcam and ensure the shape predictor file is present.</li>
            <li>Activate the virtual environment:
                <pre>source venv/bin/activate  # On Windows: venv\Scripts\activate</pre>
            </li>
            <li>Run the script:
                <pre>python heart_rate_monitor.py</pre>
            </li>
            <li>Position your face in front of the webcam with stable lighting and minimal movement.</li>
            <li>Press <code>q</code> to exit.</li>
        </ol>

        <h3><span class="emoji">🖼️</span> Interface</h3>
        <ul>
            <li><strong>Video Feed</strong>:
                <ul>
                    <li><strong>Green Rectangle</strong>: Forehead ROI.</li>
                    <li><strong>Blue Rectangle</strong>: Combined ROI (forehead + cheeks).</li>
                    <li><strong>Top-Left</strong>: Green/red channel images (100x100 pixels).</li>
                    <li><strong>Top-Right</strong>: Heart rate (e.g., "Heart Rate: 72 bpm").</li>
                    <li><strong>Error Message</strong>: "No face detected" if no face is found.</li>
                </ul>
            </li>
            <li><strong>Bottom Strip</strong>:
                <ul>
                    <li><strong>Left</strong>: Heart rate history (60 seconds, 40–200 bpm).</li>
                    <li><strong>Right</strong>: Filtered green/red signal plots (200 frames).</li>
                </ul>
            </li>
            <li><strong>Window Title</strong>: "Heart Rate Monitor".</li>
        </ul>

        <h3><span class="emoji">⚙️</span> Configuration</h3>
        <ul>
            <li><strong>Camera Index</strong>: Edit <code>cv2.VideoCapture(1)</code> in <code>heart_rate_monitor.py</code> (try 0 or 1).</li>
            <li><strong>Amplification Factor</strong>: Adjust <code>alpha = 10</code> for signal amplification.</li>
            <li><strong>Frame Rate</strong>: Assumes 30 FPS (<code>fs = 30</code>); modify if needed.</li>
        </ul>

        <h3><span class="emoji">📊</span> Example Output</h3>
        <p>Heart rate updates every second, typically 60–100 bpm. Graphs show real-time trends.</p>

        <hr class="section-divider">

        <h2><span class="emoji">🔍</span> How It Works</h2>
        <p>TriNetraa uses remote photoplethysmography (rPPG) to estimate heart rate from video:</p>
        <ol>
            <li><strong>Face Detection</strong>: dlib’s HOG-based detector and 68 landmarks define ROIs.</li>
            <li><strong>Signal Extraction</strong>: Extracts green/red channel averages; difference signal captures blood volume changes.</li>
            <li><strong>Signal Processing</strong>:
                <ul>
                    <li><strong>Bandpass Filter</strong>: 4th-order Butterworth (0.7–3 Hz).</li>
                    <li><strong>Eulerian Video Magnification</strong>: Amplifies changes (alpha = 10).</li>
                    <li><strong>FFT</strong>: Computes heart rate from dominant frequency.</li>
                    <li><strong>Smoothing</strong>: Moving average over 10 estimates.</li>
                </ul>
            </li>
            <li><strong>Visualization</strong>: OpenCV renders ROIs, text, and graphs.</li>
        </ol>
        <p>Details in the <a href="docs/documentation.md">full documentation</a>.</p>

        <hr class="section-divider">

        <h2><span class="emoji">🧪</span> Limitations</h2>
        <ul>
            <li><strong>Lighting</strong>: Requires stable, even lighting.</li>
            <li><strong>Motion</strong>: Sensitive to head movements; users must remain still.</li>
            <li><strong>Frame Rate</strong>: Assumes ~30 FPS.</li>
            <li><strong>Single User</strong>: Supports one face at a time.</li>
            <li><strong>Non-Medical</strong>: Not for clinical diagnostics.</li>
        </ul>

        <hr class="section-divider">

        <h2><span class="emoji">🚀</span> Future Enhancements</h2>
        <ul>
            <li>Adaptive frame rate calculation.</li>
            <li>Motion compensation for ROI stabilization.</li>
            <li>Signal quality metrics for confidence scores.</li>
            <li>Data logging for heart rate history.</li>
            <li>GUI for user-friendly settings.</li>
            <li>Multi-user support for multiple faces.</li>
        </ul>

        <hr class="section-divider">

        <h2><span class="emoji">🤝</span> Contributing</h2>
        <p>We welcome contributions to TriNetraa! To contribute:</p>
        <ol>
            <li>Fork the repository.</li>
            <li>Create a feature branch: <code>git checkout -b feature/YourFeature</code>.</li>
            <li>Commit changes: <code>git commit -m 'Add YourFeature'</code>.</li>
            <li>Push to the branch: <code>git push origin feature/YourFeature</code>.</li>
            <li>Open a Pull Request.</li>
        </ol>
        <p>Follow our <a href="CODE_OF_CONDUCT.md">Code of Conduct</a> and report issues via <a href="https://github.com/TriNetraa/heart-rate-monitor/issues">GitHub Issues</a>.</p>

        <hr class="section-divider">

        <h2><span class="emoji">📚</span> References</h2>
        <ul>
            <li>dlib: <a href="http://dlib.net/">http://dlib.net/</a></li>
            <li>OpenCV: <a href="https://docs.opencv.org/">https://docs.opencv.org/</a></li>
            <li>SciPy Signal: <a href="https://docs.scipy.org/doc/scipy/reference/signal.html">https://docs.scipy.org/doc/scipy/reference/signal.html</a></li>
            <li>Eulerian Video Magnification: <a href="http://people.csail.mit.edu/mrub/vidmag/">http://people.csail.mit.edu/mrub/vidmag/</a></li>
        </ul>

        <hr class="section-divider">

        <h2><span class="emoji">📬</span> Contact</h2>
        <p>For questions or feedback, reach out to:</p>
        <ul>
            <li><strong>Team TriNetraa</strong>: <a href="mailto:trinetraa.team@gmail.com">trinetraa.team@gmail.com</a></li>
            <li><strong>GitHub</strong>: <a href="https://github.com/TriNetraa/heart-rate-monitor">TriNetraa/heart-rate-monitor</a></li>
        </ul>

        <hr class="section-divider">

        <h2><span class="emoji">🙏</span> Acknowledgments</h2>
        <p>Thanks to VIT Bhopal University for supporting this project, the open-source community for tools like OpenCV, dlib, and SciPy, and inspiration from advancements in rPPG and contactless vital sign monitoring.</p>

        <div class="footer">
            <p><span class="emoji">🌈</span> <em>TriNetraa: Empowering health monitoring, one heartbeat at a time.</em> <span class="emoji">🌈</span></p>
        </div>
    </div>
</body>
</html>
