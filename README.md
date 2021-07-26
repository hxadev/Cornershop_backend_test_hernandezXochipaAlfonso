# Backend test - Hernandez Xochipa Alfonso

This project contains other third party dependencies to deploy the project.

## Whatsapp Broker
Twilio was used to integrate with automate message whatsapp.

There are two projects in the "Modules" folder.

- ApiWebhookWhatsapp
    - Api Developed in flask to receive and send responses by whatsapp Twilio 
- MenuOrdersApp
    - Django app developed under the MTV pattern.

## Expose the port to setup the webhook in Twilio console.
- To send and receive whatsapp messages, is necesary expose the port app.(In  the development process __ngrok__ was used to expose the port )

## Dump Data to database

The Data folder includes the necesary sql scripts to dump necesary data.

## QR Code 

The QR Folder includes the follow files:
- SCANME_FOR_SUBSCRIBE.png
    - QR code to scan and subscribe the Twilio service whatsapp of this app.
- whatsapp_subscription.txt
    - Link to open web whatsapp in the device and subscribe te Twilio service whatsapp

## Celery Tasks and Slack Reminder
The tasks.py file include the slack_reminder task that is executed daily checking if a menu of the day has been registered, if it exists the the reminder is sent to the slack group #cornershop
