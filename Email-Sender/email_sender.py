import os
import smtplib, ssl
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import credentials

def create_image_attachment(path: str) -> MIMEImage:
    with open(path, "rb") as image_file:
        mime_image = MIMEImage(image_file.read())
        mime_image.add_header('Content-Disposition', f'attachment; filename={path}')
        return mime_image

def send_mail(to_email: str, subject: str, body: str, image: str):
    host: str = "smtp-mail.outlook.com"
    port: int = 587

    context = ssl.create_default_context()

    with smtplib.SMTP(host, port) as server:
        print("Logging in...")
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(credentials.EMAIL, credentials.PASSWORD)

        print("Attempting to send message...")

        message = MIMEMultipart()
        message["From"] = credentials.EMAIL
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, 'plain'))

        if image:
            file: MIMEImage = create_image_attachment(image)
            message.attach(file)

        server.sendmail(from_addr=credentials.EMAIL, to_addrs=to_email, msg=message.as_string())

        print("Email sent!")

if __name__ == '__main__':
    send_mail(to_email="gideonadurota@gmail.com",
              subject="Test Mail",
              body="I sent you an image of a cute cat",
              image="cat.jpg")