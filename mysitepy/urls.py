"""mysitepy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
import main.views as main_views
import user.views as user_views
import guestbook.views as guestbook_views
import board.views as board_views

urlpatterns = [
    path('', main_views.index),
    path('admin/', admin.site.urls),

    path('user/joinform', user_views.joinform),
    path('user/join', user_views.join),
    path('user/joinsuccess', user_views.joinsuccess),
    path('user/modifyform',user_views.modifyform),
    path('user/modify', user_views.modify),

    path('user/checkemail', user_views.checkemail),

    path('user/loginform', user_views.loginform),
    path('user/login', user_views.login),
    path('user/logout', user_views.logout),

    path('guestbook/', guestbook_views.index),
    path('guestbook/add', guestbook_views.add),
    path('guestbook/delete', guestbook_views.delete),
    path('guestbook/deleteform', guestbook_views.deleteform),

    path('board/', board_views.list),
    path('board/view', board_views.view),
    path('board/modifyform', board_views.modifyform),
    path('board/modify', board_views.modify),
    path('board/writeform', board_views.writeform),
    path('board/deleteform', board_views.deleteform),
    path('board/delete', board_views.delete),
    path('board/add', board_views.add),
    path('board/search', board_views.search),

]
