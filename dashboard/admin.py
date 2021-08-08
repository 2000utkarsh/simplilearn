from django.contrib import admin
from .import models

admin.site.register(models.OrderID)
admin.site.register(models.CardDetails)
admin.site.register(models.BoughtCourses)
