from django.contrib import admin
from authentication.models import User, Query

class User_Admin(admin.ModelAdmin):
    model = User
    search_fields = ['user__phone']
    list_display = ("username", "College_name", "Year")

admin.site.register(User, User_Admin)
admin.site.register(Query)