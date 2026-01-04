import cv2
import os
import shutil

class VideoProcessor:
    def __init__(self, frame_interval=30):
        # frame_interval=30 ka matlab: Har 30th frame ko pakdenge (Approx 1 sec)
        self.frame_interval = frame_interval

    def extract_keyframes(self, video_path: str):
        """
        Video se frames nikal kar return karta hai.
        Input: Video File Path
        Output: List of (timestamp, image_object)
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS) # Video ki speed (e.g., 30 fps)
        
        frames = []
        frame_count = 0
        
        print(f"🎬 Processing Video... FPS: {fps}")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break  # Video khatam

            # Optimization: Har frame mat lo, sirf specific interval pe lo
            if frame_count % self.frame_interval == 0:
                # Timestamp calculate karo (Seconds mein)
                timestamp = frame_count / fps
                
                # Frame ko BGR (OpenCV) se RGB (Pillow/CLIP) mein convert karo
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # List mein save karo
                frames.append({
                    "timestamp": round(timestamp, 2),
                    "frame": frame_rgb
                })
                
            frame_count += 1

        cap.release()
        print(f"✅ Extraction Complete. Total Keyframes: {len(frames)}")
        return frames

    def cleanup(self, path: str):
        """Temp video delete karne ke liye"""
        if os.path.exists(path):
            os.remove(path)
            print(f"🧹 Cleaned up: {path}")

# Global instance
video_engine = VideoProcessor(frame_interval=30)