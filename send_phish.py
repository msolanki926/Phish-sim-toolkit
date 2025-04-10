import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

# SETTINGS
sender_email = "youremail@example.com"
sender_password = "yourpassword"  # For Gmail, use App Password if 2FA is enabled
smtp_server = "smtp.gmail.com"
smtp_port = 587

recipient_email = "target@example.com"  # Use your own test email
phishing_link = "http://localhost:5000"  # Or your ngrok link

# Load HTML template
html_template = Path("emails/phishing_template.html").read_text()
html_content = html_template.replace("{{ phishing_link }}", phishing_link)

# Compose email
msg = MIMEMultipart("alternative")
msg["Subject"] = "Suspicious Activity Detected"
msg["From"] = sender_email
msg["To"] = recipient_email

mime_html = MIMEText(html_content, "html")
msg.attach(mime_html)

# Send it
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, msg.as_string())

print("Email sent!")
