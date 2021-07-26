"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .utils.healthz import healthz
from Modules.MenuOrdersApp.views import IndexView, FormCreateMenuView, SaveMenu, SaveMeal, SendMenu, DeleteMenu, CreateReminderSlack, ReplyMessage

urlpatterns = [
    path("healthz", healthz, name="healthz"),
    path("", IndexView, name="Index"),                                              ## Principal page of the app
    path("createMenu", FormCreateMenuView, name="createMenu"),                      ## Create Form page of the app
    path("saveMenu", SaveMenu, name="SaveMenu"),                                    ## Endpoint to save the initial menu and retreive id 
    path("deleteMenu", DeleteMenu, name="DeleteMenu"),                              ## Endpoint to delete a menu and dependencies
    path("saveMeal", SaveMeal, name="SaveMeal"),                                    ## Endpoint to save a meal of created menu
    path("sendMenu", SendMenu, name="SendMenu"),                                    ## Endpoint to send the whatsapp message to all users registered in the database with the specified permissions
    path("createReminerSlack", CreateReminderSlack, name="CreateReminerSlack"),     ## Endpoint to send a manual remember for slack: UN USED
    path("message", ReplyMessage, name="ReplyMessage")                              ## Optional endpoint to reply messages in whatsapp chat(Webhook Twilio)

]
