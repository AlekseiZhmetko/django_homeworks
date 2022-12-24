from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100, blank=True)

class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, primary_key=True, on_delete=models.CASCADE, related_name='measurements')
    temperature = models.DecimalField(max_digits=5, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)

# с такой моделью Measurement получается, что каждый датчик может иметь только одно измерение температуры.
# нужно создавать отдельный объект - id конкретного измерения?
