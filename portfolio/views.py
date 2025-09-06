from django.http import FileResponse, Http404
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CV, SendMail
from .serializers import SendMailSerializer

class CVDownloadView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            cv = CV.objects.first()  
            if not cv:
                return Response({"error": "No CV found"}, status=status.HTTP_404_NOT_FOUND)

            return FileResponse(cv.file.open(), as_attachment=True, filename="CV.pdf")

        except CV.DoesNotExist:
            raise Http404("CV not found")




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
