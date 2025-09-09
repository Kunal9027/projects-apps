# pdfapi/urls.py
from django.urls import path
from .views import PDFUploadView, ChatAPIView

urlpatterns = [
    path('upload/', PDFUploadView.as_view(), name='pdf-upload'),
    path('chatapi/', ChatAPIView.as_view(), name='chatapi'),
]
