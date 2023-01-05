from django.contrib import admin

# Register your models here.
from .models import LoginModel,Client,project
# Register your models here.
admin.site.register(LoginModel)
admin.site.register(Client)
admin.site.register(project)
