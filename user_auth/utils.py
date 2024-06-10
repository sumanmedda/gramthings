from django.core.mail import send_mail
from django.conf import settings
from .models import User
import datetime

def send_email_to_client(otp,client_email):
    subject = "OTP"
    message = f"Please verify your account. Your otp is : {otp}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [client_email]

    send_mail(subject, message, from_email, recipient_list)

    user_obj = User.objects.get(email=client_email)
    user_obj.otp = otp
    user_obj.save()


def send_feedback_to_client(client_name,client_title,client_about,client_desc,client_email):
    subject = f"{client_name} - Feedback"
    message = f"{client_name}\n{client_email}\n\n{client_title}\n{client_about}\n\n{client_desc}. Time is : {datetime.datetime.now()}"
    from_email = client_email
    recipient_list = [settings.EMAIL_HOST_USER]
    send_mail(subject, message, from_email, recipient_list)

def send_password_change_to_client(passw,client_email):
    subject = "Password Changed"
    message = f"Your New Pass is: {passw} \n\n If You Have Not Changed Your Password Please Contact Us Immediately.\n Thanks and Regards GramThings"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [client_email]
    send_mail(subject, message, from_email, recipient_list)