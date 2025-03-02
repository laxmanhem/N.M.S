from django.core.mail import send_mail
from celery import shared_task
import socket
import random
from scapy.all import sniff, IP
from .models import NetworkLog
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@shared_task
def start_sniffing():
    def process_packet(packet):
        if packet.haslayer(IP):
            source_ip = packet[IP].src
            dest_ip = packet[IP].dst
            protocol = packet[IP].proto
            length = len(packet)
            latency = round(random.uniform(10, 100), 2)
            jitter = round(random.uniform(1, 10), 2)
            packet_loss = round(random.uniform(0, 5), 2)
            bandwidth = round(random.uniform(1, 50), 2)
            anomaly = packet_loss > 3 or latency > 80

            NetworkLog.objects.create(
                source_ip=source_ip,
                destination_ip=dest_ip,
                protocol=protocol,
                length=length,
                latency=latency,
                jitter=jitter,
                packet_loss=packet_loss,
                bandwidth=bandwidth,
                anomaly_detected=anomaly
            )

    sniff(filter="ip", prn=process_packet, store=False)


@shared_task
def check_anomalies():
    logs = NetworkLog.objects.filter(anomaly_detected=True)
    if logs.exists():
        send_mail(
            "Network Anomaly Detected!",
            "A potential anomaly has been detected. Check your network dashboard for details.",
            "admin@example.com",
            ["admin@example.com"],
            fail_silently=False,
        )

@shared_task
def capture_packets():
    def process_packet(packet):
        if IP in packet:
            packet_info = {
                "src": packet[IP].src,
                "dst": packet[IP].dst,
                "protocol": packet[IP].proto,
                "length": len(packet)
            }
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "network_packets",
                {"type": "send_packet", "data": packet_info}
            )
    sniff(prn=process_packet, store=False, count=100)
