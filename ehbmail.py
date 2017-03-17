from datetime import datetime

import config
import smtplib
from email.mime.text import MIMEText
from config import conf
from helpers import lp
from tables import Participant, Email
from __init__ import *


def log_email(recipient, subject, body, replyto, sent_from, dryrun=False): # dryrun=True => don't actually log this email, just construct the object
    em = Email(timestamp=datetime.now(), recipient=recipient, subject=subject, body=body, replyto=replyto, sent_from=sent_from)

    if not dryrun:
        session.add(em)
        session.commit()

    return em


def send(recipients, subject, bodies, sent_from, replyto=None, dryrun=False, charset="iso-8859-15"):
    """
    Sends an email using the connection specified in ehb.conf.

    :param recipients: list of participant IDs of the recipients
    :param subject: email subject
    :param bodies: list of email bodies, one for each recipient
    :param sent_from: specification of where this email originated (e.g. through mail tool, as automatic confirmation of application, etc.)
    :param replyto: (optional) specify a reply-to address which differs from the sender in the config file
    :param dryrun: generate email, but do not send it
    :param charset: charset in which the email body will be encoded
    :return: the list of email messages that were generated, as tables.Email objects
    """

    server = conf.get("email", "server")
    sender = conf.get("email", "sender")
    name = conf.get("email", "name")
    password = conf.get("email", "password")
    shortname = conf.get("application", "shortname")

    sent_emails = []

    if not dryrun:
        server = smtplib.SMTP(server)
        server.starttls()
        server.login(sender, password)

    for recipient, body in zip(recipients, bodies):
        prt = lp(recipient)  # type: Participant

        if not prt:
            raise Exception("Could not find participant for ID %d" % recipient)

        encoded = body.encode(charset)
        full_subject = "[%s] %s" % (shortname, subject)

        msg = MIMEText(encoded, _charset=charset)
        msg["Subject"] = full_subject
        msg["From"] = "%s <%s>" % (name, sender)
        msg["To"] = prt.email

        if replyto:
            msg.add_header('reply-to', replyto)

        if not dryrun:
            server.sendmail(sender, prt.email, msg.as_string())

        em = log_email(recipient, full_subject, body, replyto or None, sent_from, dryrun=dryrun)
        sent_emails.append(em)


    if not dryrun:
        server.quit()

    return sent_emails
