import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
import smtplib
import os



def send_email(
        sender: str,
        receiver: str,
        subject: str,
        body: str | None = None,
        cc: list[str] | None = None,
        bcc: list[str] | None = None,
        attachments: list[str] | None = None,
        **extra_headers
        ):

    password = os.environ.get("SMTP_PASSWORD")
    if not password:
        raise RuntimeError("SMTP_PASSWORD environment variable is not set!")
    
    base_dir = os.path.dirname(__file__)

    def _to_list(val):
        if val is None:
            return []
        if isinstance(val, str):
            return [v.strip() for v in val.split(",") if v.strip()]
        return list(val)
    to_list = _to_list(receiver)
    cc_list = _to_list(cc)
    bcc_list = _to_list(bcc)
    recipients = to_list + cc_list + bcc_list
    with smtplib.SMTP("smtp-relay.brevo.com", 587) as server:
        server.starttls()
        server.login("9b5f90001@smtp-brevo.com", password)


        msg = MIMEMultipart("mixed")
        msg["Subject"] = f"{subject}"
        msg["From"] = sender
        msg["To"]  = ", ".join(to_list)
        if cc_list:
            msg["Cc"] = ", ".join(cc_list)
        #msg["BCc"] = bcc

        if body is not None:
            html = f"""
        <html>
            <body>
                <p>{body}</p>
                <hr>
                <p>
                    Regards,<br><br>

                    <img src="cid:Peterma-Ag.png" width="120" /><br>
                    <b>Obed Adu-Gyamfi</b> | Administrator<br>
                    <b>Peterma-Ag Enterprise</b><br>
                    P.O.Box 97, Sefwi Bekwai<br>
                    Email: obed.adu-gyamfi@peterma-ag.com<br>
                    Mobile: +233 595652459
                </p>
            </body>
        </html>
        """
            plain = body
        else:
            html_path = os.path.join(base_dir, "body.html")
            try:
                with open(html_path, "r", encoding="utf-8") as msb:
                    html = msb.read()
                plain = ""
            except Exception as e:
                print("[{}]{}".format(e.__class__.__name__, e))
                html = ""
                plain = ""

        #creating the related container for HTML + inline image
        msg_related = MIMEMultipart("related")
        msg_alternative = MIMEMultipart("alternative")
        msg_related.attach(msg_alternative)
        if plain:
            msg_alternative.attach(MIMEText(plain, "plain"))
        msg_alternative.attach(MIMEText(html, "html"))
        msg.attach(msg_related)

        #attaching an inline logo


        logo_path = os.path.join(base_dir, "Peterma-Ag.png")
        try:
            with open(logo_path, "rb") as lg:
                img = MIMEImage(lg.read())
                img.add_header("Content-ID", "<Peterma-Ag.png>")
                img.add_header("Content-Disposition", "inline", filename="Peterma-Ag.png")
                msg_related.attach(img)
        except Exception as e:
            print("[{}]{}".format(e.__class__.__name__, e))


        
        if attachments:
            attach_list = _to_list(attachments)
            for path in attach_list:
                try:
                    
                    with open(path, "rb") as attachment:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header("Content-Disposition", f'attachment; filename="{path}"')
                        msg.attach(part)
                except FileNotFoundError as e:
                    print(f"{path} not Found!")
                except Exception as e:
                    print("[{}]{}".format(e.__class__.__name__, e))
        
        
       
        server.send_message(msg, from_addr=sender, to_addrs=recipients)
        print(f"Email sent successfully to {recipients}")
