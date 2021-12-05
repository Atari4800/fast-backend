from django.http import Http404
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models import RouteList
from backend.serializers import RouteListSerializer


class RouteListView(APIView):

    def get_object(self, pk):
        try:
            return RouteList.objects.get(pk=pk)
        except RouteList.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        route_list = self.get_object(pk)
        serializer = RouteListSerializer(route_list)
        return Response(serializer.data)
