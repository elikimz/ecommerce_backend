
# from datetime import datetime, timedelta
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import os
# import random
# import smtplib
# from dotenv import load_dotenv
# from jose import jwt
# from passlib.context import CryptContext
# from typing import Optional


# load_dotenv()


# SECRET_KEY = "your-secret-key" 
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password: str) -> str:
#     return pwd_context.hash(password)

# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# # --- 📧 SMTP Config ---
# SMTP_SERVER = os.getenv("SMTP_SERVER")
# SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
# SMTP_USERNAME = os.getenv("SMTP_USERNAME")
# SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
# SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL")

# # --- 🔢 OTP Generator ---
# def generate_otp(length: int = 6) -> str:
#     return ''.join([str(random.randint(0, 9)) for _ in range(length)])

# # --- ✉️ Styled OTP Email Sender ---
# def send_otp_email(to_email: str, otp: str):
#     html_content = f"""
#     <html>
#     <head>
#         <style>
#             body {{
#                 font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#                 background-color: #f5f9fc;
#                 padding: 30px;
#                 color: #2d2d2d;
#             }}
#             .container {{
#                 max-width: 500px;
#                 margin: auto;
#                 background: white;
#                 border-radius: 10px;
#                 padding: 20px;
#                 box-shadow: 0 4px 12px rgba(0,0,0,0.08);
#             }}
#             h2 {{
#                 color: #007acc;
#                 margin-bottom: 10px;
#             }}
#             .otp-box {{
#                 background-color: #eaf4ff;
#                 color: #007acc;
#                 font-size: 26px;
#                 font-weight: bold;
#                 padding: 15px 25px;
#                 border-radius: 8px;
#                 display: inline-block;
#                 margin-top: 15px;
#                 border: 1px solid #cbe6ff;
#             }}
#             .copy-button {{
#                 margin-top: 10px;
#                 background-color: #007acc;
#                 color: white;
#                 border: none;
#                 padding: 10px 16px;
#                 font-size: 14px;
#                 border-radius: 4px;
#                 cursor: pointer;
#             }}
#             p {{
#                 margin-top: 20px;
#                 font-size: 14px;
#                 color: #666;
#             }}
#         </style>
#     </head>
#     <body>
#         <div class="container">
#             <h2>Password Reset OTP</h2>
#             <p>Use the OTP below to reset your password:</p>
#             <div class="otp-box" id="otp">{otp}</div><br/>
#             <button class="copy-button" onclick="copyOTP()">Copy OTP</button>
#             <p>This OTP will expire in 10 minutes. If you didn’t request a password reset, you can safely ignore this email.</p>
#         </div>
#         <script>
#             function copyOTP() {{
#                 var otp = document.getElementById("otp").innerText;
#                 navigator.clipboard.writeText(otp).then(function() {{
#                     alert("OTP copied to clipboard!");
#                 }}, function(err) {{
#                     alert("Failed to copy OTP: " + err);
#                 }});
#             }}
#         </script>
#     </body>
#     </html>
#     """

#     msg = MIMEMultipart("alternative")
#     msg['Subject'] = "Your OTP for Password Reset"
#     msg['From'] = SMTP_FROM_EMAIL
#     msg['To'] = to_email

#     msg.attach(MIMEText(html_content, "html"))

#     try:
#         with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#             server.starttls()
#             server.login(SMTP_USERNAME, SMTP_PASSWORD)
#             server.send_message(msg)
#             print(f"✅ OTP email sent to {to_email}")
#     except Exception as e:
#         print(f"❌ Error sending OTP email: {e}")
#         raise




from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import random
import smtplib
from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext
from typing import Optional

# Load environment variables from .env
load_dotenv()

# Load secret key and JWT config from environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")  # fallback if missing
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- SMTP Config loaded from environment variables ---
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL")

# --- OTP Generator ---
def generate_otp(length: int = 6) -> str:
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

# --- Send OTP Email with styled HTML ---
def send_otp_email(to_email: str, otp: str):
    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f5f9fc;
                padding: 30px;
                color: #2d2d2d;
            }}
            .container {{
                max-width: 500px;
                margin: auto;
                background: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            }}
            h2 {{
                color: #007acc;
                margin-bottom: 10px;
            }}
            .otp-box {{
                background-color: #eaf4ff;
                color: #007acc;
                font-size: 26px;
                font-weight: bold;
                padding: 15px 25px;
                border-radius: 8px;
                display: inline-block;
                margin-top: 15px;
                border: 1px solid #cbe6ff;
            }}
            .copy-button {{
                margin-top: 10px;
                background-color: #007acc;
                color: white;
                border: none;
                padding: 10px 16px;
                font-size: 14px;
                border-radius: 4px;
                cursor: pointer;
            }}
            p {{
                margin-top: 20px;
                font-size: 14px;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Password Reset OTP</h2>
            <p>Use the OTP below to reset your password:</p>
            <div class="otp-box" id="otp">{otp}</div><br/>
            <button class="copy-button" onclick="copyOTP()">Copy OTP</button>
            <p>This OTP will expire in 10 minutes. If you didn’t request a password reset, you can safely ignore this email.</p>
        </div>
        <script>
            function copyOTP() {{
                var otp = document.getElementById("otp").innerText;
                navigator.clipboard.writeText(otp).then(function() {{
                    alert("OTP copied to clipboard!");
                }}, function(err) {{
                    alert("Failed to copy OTP: " + err);
                }});
            }}
        </script>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg['Subject'] = "Your OTP for Password Reset"
    msg['From'] = SMTP_FROM_EMAIL
    msg['To'] = to_email

    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
            print(f"✅ OTP email sent to {to_email}")
    except Exception as e:
        print(f"❌ Error sending OTP email: {e}")
        raise
