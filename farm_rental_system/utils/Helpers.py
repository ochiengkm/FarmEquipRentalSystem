import os
import smtplib
import random
from datetime import timedelta, datetime

from django.core.mail import send_mail
from django.utils import timezone

from authuser.models import OTP

from farm_rental_system.settings import BASE_DIR


class Helpers():
    def __init__(self):
        self.libraries_counter = {}

    def generateLibraryCode(self, name):
        while True:
            splitted_name = name.split(' ')
            initials = ''.join([n[0] for n in splitted_name]).upper()

            if initials not in self.libraries_counter:
                self.libraries_counter[initials] = 1

            primary_key = str(self.libraries_counter[initials]).zfill(3)
            self.libraries_counter[initials] += 1

            library_code = f"{initials}-{primary_key}"

            # Check if the generated code already exists in the database
            if not Libraries.objects.filter(library_code=library_code).exists():
                return library_code

    def otp(self, name, otp, email, *args, **kwargs):
        try:
            email_content = f"""
            <html>
                <head>
                    <style>
                        p {{
                            font-size: 12px;
                        }}
                        span {{
                            font-size: 20px;
                            color: black;
                        }}
                    </style>
                </head>
                <body>
                   <p>Hello {name},</p>
                    <p>Use: <span class="otp"><p{otp}</span></p>
                    <p>If you did not request this, please ignore. Do not share OTP with anyone.</p>
                </body>
            </html>
            """
            sent = send_mail(
                'Verification OTP',
                '',
                'no-reply@gmail.com',
                [email],
                fail_silently=False,
                html_message=email_content,
            )
            return sent

        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return 0

    def generateotp(self):
        characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz"
        otp = ''.join(random.choice(characters) for _ in range(6))  # Generate 6-digit OTP
        return otp

    def saveotp(self, otp, email):
        expiry_time = timezone.now() + timedelta(minutes=5)
        otpData = OTP(
            otp=otp,
            email=email,
            expirydate=expiry_time
        )
        otpData.save()
        return None

    def send_generated_password(self, name, username, password, email):
        try:
            email_content = f"""
            <html>
                <head>
                    <style>
                        font-size: 12px;
                    </style>
                </head>
                <body>
                    <p>Hello {name},</p> <p>Welcome to LibraTech Library Management System! We are delighted to have you 
                    join our community of librarians, administrators, and patrons.</p> <p>Your account has been 
                    created successfully!</p> <p>Please use the information below to log in to your account.</p>
                    
                    <p>Your username: {username}</p>
                    <p>Your new password: {password}</p>
                    
                    <p>Best regards,</p>
                    <p>Elimu Library Management System Team</p>


                </body>
            </html>
            """
            sent = send_mail(
                'Your New Account Credentials',
                '',
                'no-reply@gmail.com',
                [email],
                fail_silently=False,
                html_message=email_content,
            )
            return sent

        except Exception as e:
            sent = 0
            print(f"Error sending email: {str(e)}")
        return sent

    def log(self, request):
        current_date = datetime.now().strftime('%Y.%m.%d')
        log_file_name = f"{current_date}-request.log"
        log_directory = os.path.join(BASE_DIR, 'utils', 'logs')
        log_file_path = os.path.join(log_directory, log_file_name)
        log_string = f"[{datetime.now().strftime('%Y.%m.%d %I.%M.%S %p')}] => method: {request.method} uri: {request.path} queryString: {request.GET.urlencode()} protocol: {request.scheme} remoteAddr: {request.META.get('REMOTE_ADDR')} remotePort: {request.META.get('REMOTE_PORT')} userAgent: {request.META.get('HTTP_USER_AGENT')}"

        # Create the directory if it doesn't exist
        os.makedirs(log_directory, exist_ok=True)

        mode = 'a' if os.path.exists(log_file_path) else 'w'
        with open(log_file_path, mode) as log_file:
            log_file.write(log_string + '\n')


def is_eligible_for_renewal(borrowing_date):
    renewal_period = timedelta(days=7)  # Adjust as needed
    today = timezone.now().date()
    return borrowing_date + renewal_period >= today


def calculate_fine(borrowing_date, return_date):
    overdue_days = (return_date - borrowing_date).days
    fine_per_day = 0.5
    fine_amount = max(0, overdue_days) * fine_per_day
    return fine_amount
