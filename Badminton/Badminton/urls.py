"""
URL configuration for Badminton project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from SwapVenues.views import views, user_account, user_list

urlpatterns = [
    # index
    path('', views.index),

    # account
    path('login/', user_account.login),
    path('register/', user_account.register),
    path('logout/', user_account.logout),

    # swap venues
    path('siping/', views.show_siping),
    path('jiading/', views.show_jiading),

    # add info
    path('siping/addinfo/', user_list.addvenu_siping),
    path('jiading/addinfo/', user_list.addvenu_jiading),

    # delete and edit
    path('<path:prefix>/addinfo/<int:nid>/delete/', user_list.delete_info),
    path('<path:prefix>/addinfo/<int:nid>/edit/', user_list.edit_info),
]
