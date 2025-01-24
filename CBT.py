import sys
import cv2
import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox
from PyQt5.QtGui import QImage, QPixmap
import requests
import youtube_dl
from pydub import AudioSegment
from pydub.playback import play

# Binaural Beat Generation Function
def generate_binaural_beat(frequency_left, frequency_right, duration=5, sampling_rate=44100):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    left_channel = np.sin(2 * np.pi * frequency_left * t)
    right_channel = np.sin(2 * np.pi * frequency_right * t)
    audio_data = np.array([left_channel, right_channel]).T
    return audio_data

# PyQt Window
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hearing and Eye Disorder Diagnosis")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        self.status_label = QLabel("Welcome! Please choose an action.", self)
        self.layout.addWidget(self.status_label)

        self.diagnose_button = QPushButton("Diagnose Hearing and Vision Disorders", self)
        self.diagnose_button.clicked.connect(self.diagnose_disorders)
        self.layout.addWidget(self.diagnose_button)

        self.play_binaural_button = QPushButton("Play Binaural Beat for Tinnitus", self)
        self.play_binaural_button.clicked.connect(self.play_binaural_beat)
        self.layout.addWidget(self.play_binaural_button)

        self.search_binaural_button = QPushButton("Search & Play Online Binaural Beats", self)
        self.search_binaural_button.clicked.connect(self.search_and_play_online_binaural_beat)
        self.layout.addWidget(self.search_binaural_button)

        self.setLayout(self.layout)

        self.capture = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_webcam)
        self.timer.start(20)

        self.webcam_label = QLabel(self)
        self.layout.addWidget(self.webcam_label)

        self.show()

    def diagnose_disorders(self):
        # Placeholder logic for diagnosis. This should integrate ML algorithms or medical diagnosis logic.
        self.status_label.setText("Diagnosis: Eye and Ear Disorders Detected. Recommending therapy.")
        # Suggest CBT and AI practices
        self.suggest_cbt_ai_practices()

    def play_binaural_beat(self):
        # Generate binaural beat for tinnitus treatment (use appropriate frequencies for condition)
        frequency_left = 440  # Hz for left ear
        frequency_right = 444  # Hz for right ear
        audio_data = generate_binaural_beat(frequency_left, frequency_right)
        self.status_label.setText("Binaural beat is playing for tinnitus treatment.")
        # Play the sound (this will require a library like pyaudio or sounddevice, not implemented here)

    def search_and_play_online_binaural_beat(self):
        # Search and play binaural beats music from YouTube or any other online source
        self.status_label.setText("Searching and playing online binaural beats...")

        # Example: Use youtube-dl to download binaural beat music from a URL or search
        video_url = 'https://www.youtube.com/watch?v=VideoID'  # Replace with actual search or URL
        self.play_binaural_from_youtube(video_url)

    def play_binaural_from_youtube(self, video_url):
        # Using youtube-dl to download the audio
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloaded_binaural_audio.%(ext)s',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            audio_file = ydl.prepare_filename(info_dict)

        # Play the downloaded binaural beat
        self.status_label.setText(f"Playing: {audio_file}")
        audio = AudioSegment.from_file(audio_file)
        play(audio)

    def suggest_cbt_ai_practices(self):
        # Example CBT practice suggestion
        self.status_label.setText("Recommendation: Try mindfulness, focus exercises, and AI-driven cognitive tools.")
        # Implement AI practices like virtual coaching, relaxation techniques, etc.

    def update_webcam(self):
        # Capture frame from webcam
        ret, frame = self.capture.read()
        if ret:
            # Display the frame in PyQt window
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channels = frame_rgb.shape
            bytes_per_line = channels * width
            q_image = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.webcam_label.setPixmap(QPixmap(q_image))

    def closeEvent(self, event):
        self.capture.release()

# Running the Application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
