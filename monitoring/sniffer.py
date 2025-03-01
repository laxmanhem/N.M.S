import socket
import time
from scapy.all import sniff, IP
from .models import NetworkLog
import random

def get_local_ip():
    """ Get the local IP address of the machine. """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return "127.0.0.1"
    finally:
        s.close()

local_ip = get_local_ip()

def process_packet(packet):
    """ Process captured packets and store in the database. """
    if packet.haslayer(IP):
        source_ip = packet[IP].src
        dest_ip = packet[IP].dst
        protocol = packet[IP].proto
        length = len(packet)

        # Simulated metrics
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

def start_sniffing():
    sniff(filter=f"ip and (src host {local_ip} or dst host {local_ip})", prn=process_packet, store=False)
