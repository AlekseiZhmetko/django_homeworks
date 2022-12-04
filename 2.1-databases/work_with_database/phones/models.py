from django.db import models



class Phone(models.Model):
    id = models.IntegerField(default=None, primary_key=True)
    name = models.CharField(default=None, max_length=100)
    price = models.DecimalField(default=None, max_digits=18, decimal_places=1)
    image = models.ImageField(default=None, upload_to='phones/phone_images')
    release_date = models.DateField(default=None, auto_now=False, auto_now_add=False)
    lte_exists = models.BooleanField(default=False)
    slug = models.SlugField(default=None)


