from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.core import serializers
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from celery import current_app
from datetime import datetime, timedelta, date
from django.utils.dateparse import parse_datetime
from Modules.MenuOrdersApp.models import *
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from .tasks import slack_reminder
import pytz

import json

# Index View


def IndexView(request):
    menus = Menus.objects.all()
    meals = Meals.objects.all()
    orders = Orders.objects.all()

    context = {
        "menus": menus,
        "meals": meals,
        "orders": orders
    }
    return render(request, 'IndexTemplate.html', context)

# Form To create a new menu


def FormCreateMenuView(request):
    if(request.method == "GET" and "id" in request.GET):
        id = request.GET["id"]
        if(id != None):
            menus = Menus.objects.get(pk=id)
            meals = Meals.objects.all()

        context = {
            "menu": menus,
            "meals": meals
        }
        return render(request, "CreateMenuTemplate.html", context)
    else:
        return render(request, "CreateMenuTemplate.html")


# Endpoint to save a new menu
@csrf_exempt
def SaveMenu(request):
    if(request.is_ajax and request.method == 'POST'):
        requestData = json.loads(request.body)
        today = datetime.now().date()
        # requestData["fecha"]
        regDate = datetime.strptime(requestData["fecha"], "%Y-%m-%d").date()

        if(regDate < today):
            return JsonResponse({
                "status": "error",
                "message": "Selecciona una fecha de hoy en adelante"}, status=400)

        menu = Menus(publisheddate=regDate, createdat=today)
        menu.save()

        menuSerialized = serializers.serialize("json", [menu, ])

        print(menuSerialized)

    return JsonResponse({"status": "ok", "data": menuSerialized}, status=200)


# Endpoint to save a new meal
@csrf_exempt
def SaveMeal(request):
    if(request.is_ajax and request.method == 'POST'):
        requestData = json.loads(request.body)
        today = datetime.now().date()

        meal = Meals(
            key=requestData["key"], description=requestData["description"], idmenu=Menus(id=int(requestData["idMenu"])))
        meal.save()

        mealSerialized = serializers.serialize("json", [meal, ])

        print(mealSerialized)

    return JsonResponse({"status": "ok", "data": mealSerialized}, status=200)

# Endpoint to send a menu
# Update the last changes on the menu, and send message to all users with the correct permissions on whatsapp


@csrf_exempt
def SendMenu(request):
    if(request.is_ajax and request.method == 'POST'):
        requestData = json.loads(request.body)
        today = date.today().strftime("%Y-%m-%d")
        # Save Menu
        menu = Menus(
            id=requestData["menu"]["id"],
            publisheddate=requestData["menu"]["publisheddate"])
        menu.save()

        # Get Meals of Request
        meals = requestData["meals"]

        # Loop meals to persist data
        for obj in meals:
            meal = Meals(
                id=obj["id"], key=obj["key"], description=obj["description"], idmenu=Menus(id=int(menu.id)))
            meal.save()

        if(today == requestData["menu"]["publisheddate"]):
            if(whatsapp_manager(menu.id)):
                return JsonResponse({"status": "ok", "message": "Menu enviado correctamente"}, status=200)
            else:
                return JsonResponse({"status": "error", "message": "No se pudo enviar el mensaje"}, status=500)
        return JsonResponse({"status": "ok", "message": "Menu programado correctamente"}, status=200)

# Endpoint to delete a new menu


@csrf_exempt
def DeleteMenu(request):
    if(request.method == "GET" and "id" in request.GET):
        menu = Menus.objects.get(pk=request.GET["id"])
        meals = Meals.objects.all()
        menus = Menus.objects.all()
        orders = Orders.objects.filter(idmenu=menu)

        orders.delete()

        for meal in meals:
            if meal.idmenu == menu:
                meal.delete()
            else:
                pass

        menu.delete()

        context = {
            "menus": menus,
            "meals": meals
        }
        return render(request, 'IndexTemplate.html', context)

    return render(request, 'IndexTemplate.html')

# Function that execute the Twilio client and send whatsapp message


def whatsapp_manager(menuId):
    try:
        # Get All Users to send Message and only broker user with the correct permissions
        users = get_users_to_send_message()

        # Get the message template with the menu created by id passed
        templateMessage = create_menu_message(menuId)

        # Get the first user(the broker message) to send whatsapp message
        brokerPhone = "whatsapp:+1{0}".format(users[0].phone)

        client = Client("AC0bddd51fb86522fdabd77a3bec1b6aaa",
                        "42d41973aa30ac9a6309054c39006403")
        from_number = brokerPhone

        usersToOrder = users[1]

        # All Numbers of the users
        for to in usersToOrder:
            user = to.iduser
            to_number = "whatsapp:{0}".format(user.phone)
            message = client.messages.create(body=templateMessage,
                                             from_=from_number, to=to_number)
        if message.sid != None:
            return True
        return False
    except ValueError:
        return False

# Create a message menu for send to slack and whatsapp


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

# Get All users with the correct permissions to create order via whatsapp


def get_users_to_send_message():
    # Brokers Users
    sendMessageGrant = Permissions.objects.get(pk=1)
    # Create Order Users
    createOrderGrant = Permissions.objects.get(pk=7)
    usersToSend = UsersPermissions.objects.filter(
        idpermission=sendMessageGrant)[0].iduser
    usersToOrder = UsersPermissions.objects.filter(
        idpermission=createOrderGrant)

    return [usersToSend, usersToOrder]


# Actions for the slack reminder

# Creation of the asychronous task for save the reminder for slack
@csrf_exempt
def CreateReminderSlack(request):
    if(request.is_ajax and request.method == 'POST'):
        requestData = json.loads(request.body)

        id = requestData["id"]
        menuRequested = Menus.objects.get(pk=id)

        if menuRequested.id != None:
            delta = timedelta(minutes=1)
            slack_reminder.apply_async(
                args=(menuRequested.id,), eta=menuRequested.publisheddate + delta)
        return JsonResponse({"status": "ok", "message": menuRequested.publisheddate}, status=200)
    else:
        return JsonResponse({"status": "error", "message": "Datos enviados invalidos"}, status=500)

# Create a new MessageResponse instance to reply where a user send message in whatsapp chat


def response_whatsapp(message):
    response = MessagingResponse()
    response.message(message)
    return str(response)

# Reply messages to user where send a whatsapp chat


@csrf_exempt
def ReplyMessage(request):
    # Get User Phone
    userPhone = request.POST.get('From')
    # Get User Message
    message = request.POST.get('Body').lower()
    # Get Todays Menu
    menuToday = Menus.objects.get(
        publisheddate=datetime.today().strftime('%Y-%m-%d'))
    # Get Meals of Todays Menu
    mealsMenuToday = list(Meals.objects.filter(idmenu=menuToday))

    # Get The user phone to filter in models
    if(userPhone != None):
        userPhone = userPhone.replace("whatsapp:", "")

    # Retrieve USer MOdel by phone
    userModel = Users.objects.get(phone=userPhone)

    # Constaint until 11 AM CLT
    now = datetime.now().time().hour

    if(now > 11):
        return HttpResponse(response_whatsapp("Until 11 AM CLT!😉😉"))

    if(userModel.id != None):
        if message:
            try:
                order = Orders.objects.get(
                    idmenu=menuToday, iduser=userModel)

                if order.status == "O":
                    return HttpResponse(response_whatsapp("Your ordered today was registered!😉😉\n\n{} - {}".format(order.idmeal.key, order.comments)))

            except Orders.DoesNotExist:
                order = Orders()

            if message.isnumeric():
                orderMeal = int(message)
                mealSelected = mealsMenuToday[int(orderMeal) - 1]
                order.idmeal = mealSelected
                order.iduser = userModel
                order.idmenu = menuToday
                order.save()

                return HttpResponse(response_whatsapp("""
Perfect!! Your meal {} is to order

Do you want agree any customization (YES|NO)?
                """.format(mealSelected.key)))

            elif message == "yes":
                return HttpResponse(response_whatsapp(
                    "What more do you agree to your meal (start with the sentence 'I Want'?"))
            elif message == "no":
                order.status = "O"
                order.iduser = userModel
                order.idmeal = mealSelected
                order.save()
                return HttpResponse(response_whatsapp("Perfect!! You meal is completed! =)"))
            elif message.startswith("i want"):
                order.status = "O"
                order.iduser = userModel
                order.comments = message
                order.save()
                return HttpResponse(response_whatsapp("Good decision! You meal is completed! =)"))
            else:
                return HttpResponse(response_whatsapp("I'm sorry, i can not understand you "))
