# import smtplib
import asyncio
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

import aiosmtplib

from tgbot import config


class MailSender:

    def __init__(self, cfg):
        self.host = cfg.smtp_server
        self.from_addr = cfg.from_addr
        self.to_addr = cfg.to_addr
        # self.subject = ""
        # self.body_text = ""
        self.user = cfg.mail_user
        self.password = cfg.mail_password

    async def send_email(self,  mail_subject="", mail_body=""):
        # create the message
        msg = MIMEMultipart()
        msg["From"] = self.from_addr
        msg["Subject"] = mail_subject
        msg["Date"] = formatdate(localtime=True)

        # if self.body_text:
        msg.attach(MIMEText(mail_body))

        msg["To"] = self.to_addr
        emails = self.to_addr
        server = aiosmtplib.SMTP(hostname=self.host, use_tls=True) # username=self.user,
        # password=self.password,
        await server.connect()
        await server.login(self.user, self.password)
        await server.sendmail(self.from_addr, emails, msg.as_string())
        await server.quit()

    # def send_email_with_attachment(self, data_to_attach, file_name='file.png', mail_subject=""):
    #     # create the message
    #     msg = MIMEMultipart()
    #     msg["From"] = self.from_addr
    #     msg["Subject"] = mail_subject
    #     msg["Date"] = formatdate(localtime=True)
    #
    #     if self.body_text:
    #         msg.attach(MIMEText(self.body_text))
    #
    #     msg["To"] = self.to_addr
    #
    #     attachment = MIMEBase('application', "octet-stream")
    #
    #     try:
    #
    #         attachment.set_payload(data_to_attach)
    #         encoders.encode_base64(attachment)
    #         header = 'Content-Disposition', 'attachment; filename="%s"' % file_name
    #         attachment.add_header(*header)
    #         msg.attach(attachment)
    #     except IOError:
    #         msg = "Error opening attachment file "  # % file_to_attach
    #         print(msg)
    #         # sys.exit(1)
    #
    #     emails = self.to_addr
    #     server = smtplib.SMTP_SSL(self.host)
    #     server.login(self.user, self.password)
    #     server.sendmail(self.from_addr, emails, msg.as_string())
    #     server.quit()

async def send_email(mail_subject, mail_body):
    cfg = config.load_config('.env').mail
    mail = MailSender(cfg)
    await mail.send_email(mail_subject=mail_subject, mail_body=mail_body)
    # await asyncio.sleep(0)
    #print(f'send_email dp=')
    # asyncio.create_task(mail.send_email(mail_subject = mail_subject))
    # m = mail.send_email(mail_subject=mail_subject)
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(asyncio.gather(m))
    # loop.close()