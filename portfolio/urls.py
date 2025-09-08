from django.urls import path
from .views import CVDownloadView, NotifyVisitView, VisitorMailView

urlpatterns = [
    path('cv/download/', CVDownloadView.as_view(), name='cv-download'),
    path('visitorMail/', VisitorMailView.as_view(), name='visitor-mail'),
    path('notify-visit/', NotifyVisitView.as_view(), name='notify-visit'),
]
