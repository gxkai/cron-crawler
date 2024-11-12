import os
import ssl
import jinja2
import logging
import smtplib
from typing import List, Union
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.util import loadenv

logger = logging.Logger(name="Cron Job")
loadenv()


FROM_EMAIL_ADDRESS = os.environ.get("FROM_EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
MAIL_SERVER = os.environ.get("MAIL_SERVER")
MAIL_SERVER_ADDR = MAIL_SERVER.split(':')[0]
MAIL_SERVER_PORT = int(MAIL_SERVER.split(':')[1])
context = ssl.create_default_context()
templateLoader = jinja2.FileSystemLoader(searchpath="./src/templates")
templateEnv = jinja2.Environment(loader=templateLoader)


def send_email(msg: str, to_email: Union[str, List] = FROM_EMAIL_ADDRESS):
    try:
        with smtplib.SMTP(MAIL_SERVER_ADDR, MAIL_SERVER_PORT) as server:
            server.starttls(context=context)
            server.login(FROM_EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(FROM_EMAIL_ADDRESS, to_email, msg)
            server.quit()
            logger.info("Success: Email sent!")
            return True
    except Exception as e:
        logger.error(e)
        logger.error("Email failed to send.")
        return False


def send_code_template(subject: str, code: str, to_email: Union[str, List[str]]):
    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = subject
    MESSAGE['To'] = to_email
    MESSAGE['From'] = FROM_EMAIL_ADDRESS
    MESSAGE.preamble = """
    Your mail reader does not support the report format.
    Please visit us online!"""
    TEMPLATE_FILE = "code.html"
    template = templateEnv.get_template(TEMPLATE_FILE)
    body = template.render(code=code)
    HTML_BODY = MIMEText(body, 'html')
    MESSAGE.attach(HTML_BODY)
    send_email(MESSAGE.as_string(), to_email)


def send_error(subject: str, msg: str, to_email: Union[str, List[str]]):
    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = subject
    MESSAGE['To'] = to_email
    MESSAGE['From'] = FROM_EMAIL_ADDRESS
    MESSAGE.preamble = "Error"
    MESSAGE.attach(MIMEText(msg))
    send_email(MESSAGE.as_string(), to_email)


