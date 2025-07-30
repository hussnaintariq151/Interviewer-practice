# utils/webcam_emotion.py

import cv2
from fer import FER
import time

def start_emotion_stream(emotion_log: list, stop_flag):
    """
    Continuously captures webcam frames, detects emotion using FER,
    and stores the dominant emotion in emotion_log list.

    Args:
        emotion_log (list): Shared list to append detected emotions.
        stop_flag (threading.Event): Used to signal when to stop the stream.
    """
    detector = FER(mtcnn=True)
    cap = cv2.VideoCapture(0)

    print("📷 Starting webcam for emotion detection...")

    try:
        while not stop_flag.is_set():
            ret, frame = cap.read()
            if not ret:
                continue

            emotions = detector.detect_emotions(frame)
            if emotions:
                # FER returns a list of faces with emotions
                dominant_emotion = max(emotions[0]["emotions"], key=emotions[0]["emotions"].get)
                emotion_log.append(dominant_emotion)

                # Draw box and text
                (x, y, w, h) = emotions[0]["box"]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, dominant_emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.9, (36, 255, 12), 2)

            # Show live feed (optional: comment out for headless)
            cv2.imshow('🎭 Emotion Detection', frame)

            # Break on 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(0.2)  # Slight delay to ease CPU

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("📷 Webcam stream stopped.")
