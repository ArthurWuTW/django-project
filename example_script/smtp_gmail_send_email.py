import sys
sys.path.append("..")

from secure_data.secure_data_loader import SecureDataLoader
secure_data_loader = SecureDataLoader()

if __name__ == '__main__':
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    content = MIMEMultipart()
    content["subject"] = "Learn Code With Mike"
    content["from"] = secure_data_loader.secure_data['SMTP_ACCOUNT']
    content["to"] = "lion811004@gmail.com"
    content.attach(MIMEText("Demo python send email\nasasdfas"))

    import smtplib
    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:
        try:
            smtp.ehlo()
            smtp.starttls()
            smtp.login( secure_data_loader.secure_data['SMTP_ACCOUNT'],  secure_data_loader.secure_data['SMTP_PASSWORD'])
            smtp.send_message(content)
            print("Complete!")
        except Exception as e:
            print("Error message: ", e)
