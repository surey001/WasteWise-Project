import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import ssl
import os

def send_email_with_pdf(sender_email, password, receiver_email, pdf_path):
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Here is your PDF file"

    # Email body
    msg.attach(MIMEText("Hi,\n\nPlease find the attached PDF file.\n\nBest regards.", 'plain'))

    # Check if PDF exists
    if os.path.isfile(pdf_path):
        with open(pdf_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(pdf_path)}")
        msg.attach(part)
    else:
        print(f"❌ PDF not found at {pdf_path}")
        return

    # Connect to server (Gmail example)
    context = ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("✅ Email sent successfully!")

# Example usage
send_email_with_pdf(
    sender_email="anandhakumarrk21@gmail.com",
    password="bvdtrhsgypyrpraf",   # Not your normal Gmail password!
    receiver_email="anandhhari2103@gmail.com",
    pdf_path="weekly_report.pdf"
)
