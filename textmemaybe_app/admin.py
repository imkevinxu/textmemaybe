from textmemaybe_app.models import *
from django.contrib import admin

class NumberAdmin(admin.ModelAdmin):
    list_display = ('user', 'number', 'name', 'message', 'created_at')
    list_filter = ('created_at', 'user', 'number', 'name',)
    ordering = ['-created_at', 'user']
    search_fields = ['user', 'number', 'name']

admin.site.register(Number, NumberAdmin)