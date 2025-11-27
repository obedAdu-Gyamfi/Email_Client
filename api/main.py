from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from Modules.email_smtp import send_email
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import os


app = FastAPI(title= "SMTP Email Client")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#app.add_middleware()

class EmailRequest(BaseModel):
    sender: EmailStr
    receiver: List[str]
    subject: str
    body: Optional[str] = None
    cc: Optional[List[str]] = None
    bcc: Optional[List[str]] = None
    #attachments: Optional[UploadFile] = None


@app.post("/send-email")
async def api_send_email(
    sender: str = Form(...),
    receiver: str = Form(...),  #comma-separated emails
    subject: str = Form(...),
    body: Optional[str] = Form(None),
    cc: Optional[str] = Form(None),
    bcc: Optional[str] = Form(None),
    attachments: Optional[List[UploadFile]] = File(None)
):
    attachment_paths = []
    if attachments:
        for file in attachments:
            temp_path = f"/tmp/{file.filename}"
            with open(temp_path, "wb") as f:
                f.write(await file.read())
            attachment_paths.append(temp_path)

    try:
        send_email(
            sender=sender,
            receiver=receiver,
            subject=subject,
            body=body,
            cc=cc,
            bcc=bcc,
            attachments=attachment_paths
        )
        return JSONResponse(status_code=200, content={"status": "success", "message": f"Email sent to {receiver}"})
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")