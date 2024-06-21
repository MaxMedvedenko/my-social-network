from django.contrib import admin

from network.models import *
from user.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Post)