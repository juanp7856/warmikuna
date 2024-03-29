from django.core.mail import send_mail
import re
from django.conf import settings 

def send_forget_password_mail(email , token ):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if not re.match(patron, email):
        return False
    
    if len(token) < 36:
        return False
    
    subject = 'Link para reestablecer tu contraseña'
    message = f'En link para reestablecer la contraseña es este: http://127.0.0.1:8000/password-reset/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True