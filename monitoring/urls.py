from django.urls import path
from .views import get_network_logs
from .views import generate_pdf_report
from django.shortcuts import redirect
from . import views
from .views import trigger_sniffer
from monitoring.views import dashboard

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('start-sniffer/', trigger_sniffer, name='start_sniffer'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('monitoring/', lambda request: redirect('monitoring/logs/')),  # Redirect to /logs
    path('logs/', get_network_logs, name='logs'),
    path('dashboard/', dashboard, name='dashboard'),
    path("export-pdf/", generate_pdf_report, name="export_pdf"),
]
