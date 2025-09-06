from django.urls import path
from .views import CVDownloadView, VisitorMailView

urlpatterns = [
    path('cv/download/', CVDownloadView.as_view(), name='cv-download'),
    path('visitorMail/', VisitorMailView.as_view(), name='visitor-mail'),
]
