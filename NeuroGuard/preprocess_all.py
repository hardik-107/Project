import cv2
import mediapipe as mp
import os
from tqdm import tqdm

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Force clean paths
RAW_DATA_DIR = os.path.normpath(os.path.join(BASE_DIR, "../data/raw_videos"))
PROCESSED_DIR = os.path.normpath(os.path.join(BASE_DIR, "../data/processed_faces"))

FRAME_SKIP = 15  # Har 15th frame save karenge (taaki photos alag dikhein)
IMG_SIZE = (224, 224)

# Init MediaPipe
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

def process_one_video(video_path, output_folder, video_name):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return 0
    
    count = 0
    frame_idx = 0
    
    while True:
        success, frame = cap.read()
        if not success:
            break
            
        frame_idx += 1
        
        # SKIP FRAMES (Space bachane ke liye)
        if frame_idx % FRAME_SKIP != 0:
            continue
            
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(rgb)
        
        if results.detections:
            for i, detection in enumerate(results.detections):
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                
                # Thoda padding
                x, y = max(0, x - 20), max(0, y - 20)
                w, h = min(iw, w + 40), min(ih, h + 40)
                
                face = frame[y:y+h, x:x+w]
                
                if face.size > 0:
                    try:
                        face = cv2.resize(face, IMG_SIZE)
                        # Save with unique name
                        fname = f"{video_name}_f{frame_idx}_{i}.jpg"
                        cv2.imwrite(os.path.join(output_folder, fname), face)
                        count += 1
                    except:
                        pass
    cap.release()
    return count

def run():
    print(f"--- FINAL PROCESSING ---")
    print(f"Reading from: {RAW_DATA_DIR}")
    print(f"Saving to: {PROCESSED_DIR}")
    
    for category in ["real", "fake"]:
        src_path = os.path.join(RAW_DATA_DIR, category)
        dst_path = os.path.join(PROCESSED_DIR, category)
        os.makedirs(dst_path, exist_ok=True)
        
        if not os.path.exists(src_path):
            print(f"Skipping {category}: Folder not found.")
            continue
            
        videos = [f for f in os.listdir(src_path) if f.lower().endswith(('.mp4', '.avi', '.mov'))]
        print(f"\nProcessing {len(videos)} videos in '{category}'...")
        
        total_faces = 0
        # Progress Bar
        for v in tqdm(videos):
            path = os.path.join(src_path, v)
            name = v.split('.')[0]
            total_faces += process_one_video(path, dst_path, name)
            
        print(f"✅ Finished {category}. Total faces saved: {total_faces}")

if __name__ == "__main__":
    run()