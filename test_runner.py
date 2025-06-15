# test_runner.py
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, to_email, from_email, password):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    # Run pytest on test_cases.py
    result_file = "result.txt"
    with open(result_file, "w") as f:
        subprocess.run(["python3", "-m", "pytest", "test.py"], stdout=f, text=True)

    # Read the result
    with open(result_file, "r") as f:
        result_content = f.read()

    # Send the email
    sender_email = "jawadidrees822@gmail.com"
    sender_password = "auvd ywth flzk uguu"
    recipient_email = "qasimalik@gmail.com"

    send_email(
        subject="Automated Test Report",
        body=result_content,
        to_email=recipient_email,
        from_email=sender_email,
        password=sender_password
    )
