from ultralytics import YOLO
import cv2
model = YOLO('best.pt')

cooldown=2

def send_alert():
    print("Sent alert to Email")

results = model.predict(source='0', show=False, conf=0.50, stream=True)

for result in results:
    boxes = result.boxes
    for box in boxes:
        conf = box.conf[0].item()
        
        if conf >= 0.50:
            cls = int(box.cls[0].item())
            class_name = result.names[cls]
            im_bgr = result.plot() 
            cooldown+=1
            if(cooldown==3):
                cooldown=0
                cv2.imwrite(f'latest.jpg',im_bgr)
                send_alert()


