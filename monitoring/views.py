from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import NetworkLog
from .serializers import NetworkLogSerializer
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    return HttpResponse("Welcome to the Network Monitoring System!")

@csrf_exempt
def trigger_sniffer(request):
    from monitoring.tasks import capture_packets
    capture_packets.delay()
    return JsonResponse({"status": "Packet capture started."})

def dashboard(request):
    return render(request, "monitoring/dashboard.html")

def monitoring_home(request):
    return HttpResponse("Welcome to the Network Monitoring Home")


@api_view(['GET'])
def get_network_logs(request):
    logs = NetworkLog.objects.order_by('-timestamp')[:50]
    serializer = NetworkLogSerializer(logs, many=True)
    return Response(serializer.data)

def dashboard(request):
    return render(request, 'monitoring/dashboard.html')

def historical_logs(request):
    logs = NetworkLog.objects.filter(archived=True)
    return render(request, "monitoring/historical_logs.html", {"logs": logs})


def generate_pdf_report(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="network_report.pdf"'
    p = canvas.Canvas(response)
    p.drawString(100, 800, "Network Monitoring Report")

    logs = NetworkLog.objects.all()
    y = 780
    for log in logs:
        p.drawString(100, y, f"{log.timestamp} - {log.source_ip} -> {log.destination_ip} - {log.protocol}")
        y -= 20

    p.save()
    return response

