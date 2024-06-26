import smtplib
from email.mime.text import MIMEText
from database import Database

class Mail:
    def __init__(self, sender, password):
        self.sender = sender
        self.password = password

    def __send_email(self, subject, body, recipients):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = ', '.join(recipients)

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                smtp_server.login(self.sender, self.password)
                smtp_server.sendmail(self.sender, recipients, msg.as_string())
            print("Message sent!")
        except Exception as e:
            print(f"Failed to send email: {e}")
    
    def send_email_from(self, user_id: str):
        database = Database()
        for user_data in database.get_emails_by_user_id(user_id=user_id):
            subject = user_data.Subject
            body = user_data.Body
            recipients = [user_data.Email]
            self.__send_email(subject=subject, body=body, recipients=recipients)

if __name__ == "__main__":
    database = Database()
    for i in database.get_emails_by_user_id("1031729548"):
        subject = "Email Subject"
        body = "This is the body of the email"
        sender = "yugrana854@gmail.com"
        recipients = ["yugrana853@gmail.com"]

        # mail = Mail(sender)
        # mail.send_email(subject, body, recipients)