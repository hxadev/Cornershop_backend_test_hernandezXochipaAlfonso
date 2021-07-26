# from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery import shared_task
from Modules.MenuOrdersApp.helpers import SlackHelper

# Task that send a reminder to slack group #cornershop
@shared_task(name="slack_reminder")
def slack_reminder(menuid):
    SlackHelper.sendReminder()
    
    
