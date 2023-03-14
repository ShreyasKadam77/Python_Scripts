import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_mail(attachment, mail_id, start_time, files_deleted):

    """
    function sends email with attachment to given mail id.
    It takes 4 parameters as :
    :param attachment: file to be attached with mail.
    :param mail_id: receiver's mail id.
    :param start_time: Execution start time of script.
    :param files_deleted: Total number of files deleted.

    """

    mail_content = f'''Starting time of Scanning : {start_time}
                    Number of Duplicate Files : {files_deleted}'''

    sender_mail_id = "email"
    sender_pass = "password"
    receiver_mail_id = mail_id

    message = MIMEMultipart()
    message['From'] = sender_mail_id
    message['To'] = receiver_mail_id
    message['Subject'] = " This mail contains log of duplicate files."

    message.attach(MIMEText(mail_content, 'plain'))
    attach_file_name = attachment
    attach_file = open(attach_file_name, "rb")

    payload = MIMEBase("application", "octate-stream")
    payload.set_payload(attach_file.read())

    encoders.encode_base64(payload)

    payload.add_header("Content-Disposition", "attachment", filename="duplicate_files")
    message.attach(payload)

    session = smtplib.SMTP("smtp.gmail.com", 587)
    session.starttls()
    session.login(sender_mail_id, sender_pass)
    text = message.as_string()
    session.sendmail(sender_mail_id, receiver_mail_id, text)
    session.quit()
