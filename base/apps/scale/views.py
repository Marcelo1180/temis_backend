import time
from threading import Thread
from django.shortcuts import render
from .driver import ScaleFinder
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from .driver import ScaleConfig
from .driver import Scale
from django.http import JsonResponse


def scaleDaemonGetValue():
    while True:
        config = ScaleConfig()
        systel = Scale(config)
        systel.readValueDaemon()
        time.sleep(0.5)


scale_daemon_value = Thread(target=scaleDaemonGetValue, daemon=True)
ScaleFinder().start()
scale_daemon_value.start()


@api_view(["GET"])
@permission_classes([AllowAny])
def scale_weight(request):
    config = ScaleConfig()
    systel = Scale(config)
    weight = systel.readValue()
    # Response with kilograms
    return JsonResponse(round(weight/1000,3), safe=False, status=200)
