from django.contrib import admin
from udyam_backend.models import Event, Team, Workshop, Content, BroadCast_Email, Team_List

from django.utils.safestring import mark_safe
from django.db import models
import threading
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import (send_mail, BadHeaderError, EmailMessage)
from authentication.models import User
from .sheets import addtosheet

class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        msg1 = EmailMessage(self.subject, self.html_content, settings.EMAIL_HOST_USER, self.recipient_list[:100])
        msg1.content_subtype = "html"
        msg2 = EmailMessage(self.subject, self.html_content, settings.EMAIL_HOST_USER, self.recipient_list[100:200])
        msg2.content_subtype = "html"
        msg3 = EmailMessage(self.subject, self.html_content, settings.EMAIL_HOST_USER, self.recipient_list[200:300])
        msg3.content_subtype = "html"
        msg4 = EmailMessage(self.subject, self.html_content, settings.EMAIL_HOST_USER, self.recipient_list[300:])
        msg4.content_subtype = "html"
        try:
            msg1.send()
            msg2.send()
            msg3.send()
            msg4.send()
        except BadHeaderError:
            return HttpResponse('Invalid header found.')

class BroadCast_Email_Admin(admin.ModelAdmin):
    model = BroadCast_Email

    def submit_email(self, request, obj): #`obj` is queryset, so there we only use first selection, exacly obj[0]
        list_email_user = [ p.email for p in User.objects.all() ] #: if p.email != settings.EMAIL_HOST_USER   #this for exception
        obj_selected = obj[0]
        EmailThread(obj_selected.subject, mark_safe(obj_selected.message), list_email_user).start()
    submit_email.short_description = 'Submit BroadCast (1 Select Only)'
    submit_email.allow_tags = True

    actions = [ 'submit_email' ]

    list_display = ("subject", "created")
    search_fields = ['subject',]

class Team_List_Admin(admin.ModelAdmin):
    model = Team_List

    def update_list(self, request, objects_selected):
        for obj in objects_selected:
            teamlist = Team.objects.filter(event = obj.event)
            sheetname = obj.event.eventname + " Teams"
            addtosheet(sheetname, teamlist)
    update_list.short_description = 'Update selected events team list'

    actions = [ 'update_list' ]
    list_display = ("event", )



admin.site.register(BroadCast_Email, BroadCast_Email_Admin)
admin.site.register(Team_List, Team_List_Admin)
admin.site.register(Event)
admin.site.register(Team)
admin.site.register(Workshop)
admin.site.register(Content)