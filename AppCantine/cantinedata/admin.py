from django.contrib import admin

# Register your models here.

from .models import Fréquentation
from .models import Prediction

admin.site.register(Fréquentation)
admin.site.register(Prediction)