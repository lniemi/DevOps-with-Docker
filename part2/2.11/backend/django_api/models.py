from django.contrib.gis.db import models

class UserGeoData(models.Model):
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(blank=True, null=True)
    geom = models.GeometryField()

    def __str__(self):
        return self.name
    
class BlackBirdGroup(models.Model):
    layer_id = models.IntegerField()
    category_id = models.IntegerField()
    layer_name = models.CharField(max_length=255)
    date = models.DateTimeField()
    description = models.TextField(default="Russian occupied area")
    geom = models.GeometryField()

    def __str__(self):
        return f"{self.layer_name} ({self.date.strftime('%d/%m/%Y %H:%M')})"