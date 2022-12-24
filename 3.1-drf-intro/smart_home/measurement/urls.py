from django.urls import path
from measurement.views import SensorListCreate, MeasurementCreate, SensorRetrieveUpdate
# from measurement.views import SensorView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('sensors/', SensorListCreate.as_view()),
    path('sensors/<pk>/', SensorRetrieveUpdate.as_view()),
    path('measurements/', MeasurementCreate.as_view()),
    # path('sensors/<pk>/', SensorView.as_view()),
]

