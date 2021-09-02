from django.contrib import admin
from .models import Users, Messages, Comments

# Register your models here.
admin.site.register(Users)
admin.site.register(Messages)
admin.site.register(Comments)
