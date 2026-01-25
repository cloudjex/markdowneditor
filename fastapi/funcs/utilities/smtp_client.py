import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config

HTML = """
<!DOCTYPE html>
<html>
  <body style="background:#f7f7f7; padding:20px;">
    <div style="background:#fff; padding:20px; border-radius:6px;">
      <h3 style="margin:0 0 15px;">
        From <a href="https://www.cloudjex.com" style="color:#8eb8eb; text-decoration:none;">cloudjex.com</a>
      </h3>

      <p style="margin:0 0 20px; color:#555; font-size:15px;">
        {title}
      </p>

      <div style="padding:10px; background:#f7f7f7; border-left:4px solid #8eb8eb; margin-bottom:20px;">
        <p style="margin:0; color:#555;">{body}</p>
      </div>

      <p style="margin:0; color:#999; font-size:10px;">
        本メールは送信専用となります。
      </p>
    </div>
  </body>
</html>
"""


class SmtpClient:
    def __init__(self):
        self.smtp_host = config.SMTP_HOST
        self.smtp_port = config.SMTP_PORT
        self.smtp_user = config.SMTP_USER
        self.smtp_pass = config.SMTP_PASSWORD
        self.smtp_from = "cloudjex.com<auto@cloudjex.com>"

    def send(self, recipient: str, subject: str, body: str) -> None:
        if not (
            self.smtp_user and
            self.smtp_pass and
            self.smtp_host and
            self.smtp_port
        ):
            print(f"Warning: SMTP is not configured. Can't send email to {recipient}.")
            return

        html = HTML.format(title=subject, body=body)

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.smtp_from
        msg["To"] = recipient

        text_part = MIMEText(body, "plain", "utf-8")
        html_part = MIMEText(html, "html", "utf-8")
        msg.attach(text_part)
        msg.attach(html_part)

        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_user, self.smtp_pass)
            server.sendmail(self.smtp_from, recipient, msg.as_string())
