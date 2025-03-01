from django.http import HttpResponse


def monitoring_home(request):
    return HttpResponse("Welcome to the Network Monitoring Home")
