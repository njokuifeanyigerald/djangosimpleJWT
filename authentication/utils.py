from django.core.mail import EmailMessage, send_mail


class Util:
    @staticmethod
    def sendEmail(data):
        send_mail( subject=data['subject'], message=data['message'], email_from= data['email_from'], recipient_list=data['recipient_list'] )
