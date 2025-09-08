import os
from django.conf import settings
from django.http import FileResponse, Http404
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CV, SendMail
from .serializers import SendMailSerializer


class CVDownloadView(APIView):
    def get(self, request, *args, **kwargs):
        file_path = os.path.join(settings.STATIC_ROOT, "cv", "CV.pdf")
        if not os.path.exists(file_path):
            raise Http404("CV not found")
        return FileResponse(open(file_path, "rb"), as_attachment=True, filename="CV.pdf")




class VisitorMailView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SendMailSerializer(data=request.data)
        if serializer.is_valid():
            send_mail_obj = serializer.save()

            subject = f"Portfolio Contact: {serializer.validated_data['subject']}"
            message = (
                f"From: {serializer.validated_data['full_name']} <{serializer.validated_data['email']}>\n\n"
                f"Message:\n{serializer.validated_data['message']}"
            )
            from_email = serializer.validated_data['email']
            recipient_list = ["abdellahsaidi310309@gmail.com"]

            try:
                send_mail(subject, message, from_email, recipient_list)
                return Response({"success": "Email sent successfully"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.core.cache import cache
from django.utils import timezone


class NotifyVisitView(APIView):
    def get(self, request, *args, **kwargs):
        subject = "New Visitor Alert"
        message = "A new visitor has just accessed your website."
        from_email = "smtp.gmail.com"  
        recipient_list = ["abdellahsaidi310309@gmail.com"]

        last_notified = cache.get("last_notify_time")

        if not last_notified or (timezone.now() - last_notified).total_seconds() > 60:
            try:
                send_mail(subject, message, from_email, recipient_list)
                cache.set("last_notify_time", timezone.now(), timeout=60)  # store for 1 min
                return Response({"success": "Notification sent"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"info": "Notification already sent recently"}, status=status.HTTP_200_OK)
