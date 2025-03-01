from django.urls import path
from .views import get_network_logs
from .views import dashboard
from .views import generate_pdf_report
from django.urls import path, redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/monitoring/', lambda request: redirect('api/monitoring/logs/')),  # Redirect to /logs
    path('api/monitoring/logs/', include('monitoring .urls')),
    path('api/monitoring/dashboard/', include('monitoring .urls')),
    path('api/monitoring/export-pdf/', include('monitoring .urls')),



    path('logs/', get_network_logs, name='logs'),
    path('dashboard/', dashboard, name='dashboard'),
    path("export-pdf/", generate_pdf_report, name="export_pdf"),

]
