import logging
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser


logger = logging.getLogger(__name__)


@api_view(["GET"])
def view_status(request):
    # logger.critical("Critical!")
    # logger.error("Error!")
    # logger.warning("Warning!")
    # logger.info("Info OK")
    # logger.debug("Debug OK")
    return Response({"status": "OK"}, status=status.HTTP_200_OK)


@permission_classes([IsAdminUser])
def view_status_authorized(request):
    return Response({"status": "OK"}, status=status.HTTP_200_OK)
