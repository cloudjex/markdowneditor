import boto3
from mypy_boto3_ses.client import SESClient

HTML = """
<!DOCTYPE html>
<html>
  <body background-color: #f7f7f7; padding: 20px;">
    <div style="max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 8px;">

      <h3 style="color: #333;">
        From <a href="https://www.cloudjex.com" style="color: #8eb8eb; text-decoration: none;">cloudjex.com</a>
      </h3>
      <p style="font-size: 15px; color: #555;">
        {{ title }}
      </p>

      <div style="margin-top: 20px; padding: 15px; background: #f7f7f7; border-left: 4px solid #8eb8eb;">
        <p style="margin: 0; color: #555;">{{ body }}</p>
      </div>

      <p style="margin-top: 30px; font-size: 10px; color: #999;">
        このメールは自動送信されています。送信専用のため、返信できません。
      </p>
    </div>
  </body>
</html>
"""


def send_mail(recipient: str, subject: str, body: str) -> None:
    ses: SESClient = boto3.client("ses")

    body = HTML.replace("{{ title }}", subject).replace("{{ body }}", body)

    ses.send_email(
        Source="info@cloudjex.com",
        Destination={
            "ToAddresses": [recipient],
        },
        Message={
            "Subject": {"Data": subject, "Charset": "UTF-8"},
            "Body": {"Html": {"Data": body, "Charset": "UTF-8"}}
        }
    )
