from ultralytics import YOLO
import cv2
import os
import threading
from alert_service import send_emails
import webbrowser
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
app_path = os.path.join(SCRIPT_DIR, 'app.py')
flask_process = subprocess.Popen(
        [sys.executable, app_path],
        cwd=SCRIPT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

webbrowser.open(f'http://localhost:5000')
print(f"--->>> Flask Server Running on http://localhost:5000")
model = YOLO('best.pt')

batch = 0
img_cnt = 0
cooldown = 0
MAX_COOLDOWN = 3 
BATCH_SIZE = 5   

os.makedirs('batch', exist_ok=True)


results = model.predict(source='0', show=True, conf=0.50, stream=True)

for result in results:
    boxes = result.boxes
    

    if len(boxes) > 0:
        if cooldown >= MAX_COOLDOWN:
            cooldown = 0
            
            im_bgr = result.plot() 
            
            batch_dir = f'batch/{batch}'
            os.makedirs(batch_dir, exist_ok=True)
            
        
            cv2.imwrite(f'{batch_dir}/{img_cnt}.jpg', im_bgr)
            img_cnt += 1
            
            if img_cnt >= BATCH_SIZE:
                img_cnt = 0
                batch += 1

                threading.Thread(target=send_emails, args=(f'batch/{batch-1}',), daemon=True).start()
        else:
            cooldown += 1
    else:
        pass