from Modules.MenuOrdersApp.models import *
from datetime import datetime, date, timedelta, time
import requests
import json
import os
from slack import WebClient
from slack.errors import SlackApiError


## Alfonso Hernandez Slack token
slack_token = "xoxb-1474977575873-2323245919889-xKIccSvaU5qIooU5sjZQHCUb"

## WebHook to #cornershop group
slack_hook = (
    "https://hooks.slack.com/services/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")

client = WebClient(token=slack_token)

# Helper create and send a reminder by slack
def sendReminder():
    tomorrow = findMenuToday[1]
    scheduled_time = time(hour=10, minute=1)
    schedule_timestamp = datetime.combine(
        tomorrow, scheduled_time).strftime('%s')

    # Channel you want to post message to
    channel_id = "cornershop"

    try:
        # Call the chat.scheduleMessage method using the WebClient
        result = client.chat_scheduleMessage(
            channel=channel_id,
            text=findMenuToday()[0],
            post_at=schedule_timestamp
        )

    except SlackApiError as e:
        print("Error scheduling message: {}".format(e))

## Helper that find the menu today and retrieve message and published date
def findMenuToday():
    menuToday = Menus.objects.get(
        publisheddate=datetime.today().strftime('%Y-%m-%d'))

    return [create_menu_message(menuToday.id), menuToday.publisheddate]

## Create a message for reminder
def create_menu_message(menuId):
    message = """Hello!! 😀\n\nI share with you today's menu 😋🤩\n\n"""
    menu = Menus.objects.get(pk=menuId)
    meals = Meals.objects.filter(idmenu=menu)

    mealsstr = ""
    number = 1
    for meal in meals:
        mealsstr += "Option {0}: ".format(number) + meal.key + " - " + \
            meal.description + " 😋 " + "\n"
        number += 1

    message += mealsstr

    message += "\n Have a nice day!"

    return message
