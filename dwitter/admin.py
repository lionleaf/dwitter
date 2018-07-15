from django.contrib import admin
from .models import Comment
from .models import Dweet


admin.site.register(Dweet)
admin.site.register(Comment)
