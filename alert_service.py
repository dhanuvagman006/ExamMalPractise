import smtplib
import imghdr  
from email.message import EmailMessage
import os
sender = "dhanuvagman69@gmail.com"
password = "azbqclhyzkegpifv"
receiver = "dhanushinsit@gmail.com"

def send_image_email(image_list):
    msg = EmailMessage()
    msg['Subject'] = "Evidence: Malpractice Image"
    msg['From'] = sender
    msg['To'] = receiver
    msg.set_content("Please find the attached image regarding the detected incident.")
    for image_path in image_list:
        try:
            with open(image_path, 'rb') as f:
                file_data = f.read()
                file_type = imghdr.what(f.name)
                file_name = os.path.basename(f.name) # Get just the filename, not the full path

            msg.add_attachment(
                file_data,
                maintype='image',
                subtype=file_type,
                filename=file_name
            )
            print(f"Attached: {file_name}")
        except Exception as e:
            print(f"Could not attach {image_path}: {e}")
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
        print("Email with image sent successfully!")

    except FileNotFoundError:
        print("Error: The image file was not found.")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    send_image_email()