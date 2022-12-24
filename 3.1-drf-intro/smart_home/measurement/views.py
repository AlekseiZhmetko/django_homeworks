from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Sensor, Measurement
from .serializers import SensorSerializer, MeasurementSerializer, SensorDetailSerializer

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.views import APIView
from django.forms.models import model_to_dict


# @api_view(['GET', 'POST'])
# def test(request):
#     sensors = Sensor.objects.all()
#     ser = SensorSerializer(sensors, many=True)
#     return Response(ser.data)


# class SensorView(APIView):
#     def get(self, request):
#         sensors = Sensor.objects.all()
#         ser = SensorSerializer(sensors, many=True)
#         return Response(ser.data)
#
#     def post(self, request):
#         post_new = Sensor.objects.create(
#             name=request.data['name'],
#             description=request.data['description'],
#         )
#         return Response({'post': model_to_dict(post_new)})


class SensorListCreate(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorRetrieveUpdate(RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer

# class MeasurementListCreate(ListCreateAPIView):
#     queryset = Measurement.objects.all()
#     serializer_class = MeasurementSerializer
## А как реализовать через ListCreateAPIView, если необходимо образаться к объекту Sensor.id,
## иначе получается ошибка?


class MeasurementCreate(APIView):
    def post(self, request):
        post_new = Measurement.objects.create(
            sensor=Sensor.objects.get(id=request.data['id']),
            temperature=request.data['temperature']
        )
        return Response({'post': model_to_dict(post_new)})


# class SensorView(ListCreateAPIView):
#     queryset = Sensor.objects.all()
#     serializer_class = SensorDetailSerializer
