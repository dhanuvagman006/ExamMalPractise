import smtplib
import imghdr
import os
from email.message import EmailMessage

SENDER = "dhanuvagman69@gmail.com"
PASSWORD = ""
RECEIVER = "dhanushinsit@gmail.com"

def send_images_from_folder(folder_path):
    msg = EmailMessage()
    msg['Subject'] = f"Evidence Folder: {os.path.basename(folder_path)}"
    msg['From'] = SENDER
    msg['To'] = RECEIVER
    msg.set_content(f"Malpractise alert: Attaching all images found in '{folder_path}'")

    valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')


    files_found = 0
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(valid_extensions):
            file_path = os.path.join(folder_path, filename)
            
            try:
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                    file_type = imghdr.what(f.name) or filename.split('.')[-1]    
                msg.add_attachment(
                    file_data,
                    maintype='image',
                    subtype=file_type,
                    filename=filename
                )
                files_found += 1
                print(f"Attached: {filename}")
            except Exception as e:
                print(f"Error attaching {filename}: {e}")

    if files_found == 0:
        print("No valid images found in the folder.")
        return

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER, PASSWORD)
            smtp.send_message(msg)
        print(f"\nSuccess! Sent {files_found} images.")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    my_folder = "./batch_1" 
    send_images_from_folder(my_folder)