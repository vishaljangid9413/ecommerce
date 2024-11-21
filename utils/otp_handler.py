from django.utils.crypto import get_random_string
import re
from logs.models import OTPLog
from django.core.mail import send_mail
import environ
env = environ.Env()


def isValidEmail(email):
    if(email == None):
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return True if re.search(pattern, email) else False


def sendEmailOTP(email, otp):
    subject = 'OTP Verification From Ecommerce Platform'
    content = f"Here is Your OTP: {otp}"
    send_mail(
        subject, 
        content, 
        env('ENV_EMAIL_HOST_USER'),
        [email],    
    )         
    otp_log = OTPLog.objects.create(otp=otp, email=email,)
    otp_log.save()
    return "OTP email sent successfully."


# ** OTP HANDLER CLASS 
class OTPHandler:
    
    @staticmethod
    def generate_otp(email):
        # Generate 6-digit OTP
        otp = get_random_string(length=6, allowed_chars='1234567890')
        if not isValidEmail(email):
            raise ValueError("Invalid Email")
        sendEmailOTP(email, otp)
        return {'OTP': otp}

    @staticmethod
    def verifyOTP(email, otp): 
        db_otp = OTPLog.objects.filter(email=email, otp=otp, status='generated')
        if not db_otp:   
            raise ValueError("Invalid OTP")
        db_otp.update(status='verified')
        return True 




