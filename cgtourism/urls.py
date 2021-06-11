"""cgtourism URL Configuration

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
from django.contrib import admin
from django.urls import path
from tourism import views
from django.conf.urls.static import static
from cgtourism import settings


urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.showIndex,name="main"),
    path('about/',views.about,name="about"),
    path('about_food/',views.about_food,name="about_food"),
    path('user_login/',views.user_login,name="user_login"),
    path('validate_user/',views.validate_user,name="validate_user"),
    path('validate_newuser/',views.validate_newuser,name="validate_newuser"),
    path('new_user/',views.new_user,name="new_user"),
    path('validate_otp/',views.validate_otp,name="validate_otp"),
    path('forgot_pass_form/',views.forgot_pass_form,name="forgot_pass_form"),
    path('forgot_password/',views.forgot_password,name="forgot_password"),

    path('adminlogin/',views.adminlogin,name="adminlogin"),
    path('validate_Admin/',views.validate_Admin,name="validate_Admin"),
    path('adminHome/',views.adminHome,name="adminHome"),

    path('tour_package/',views.tour_package,name="tour_package"),
    path('add_package/',views.add_package,name="add_package"),
    path('insert_package/',views.insert_package,name="insert_package"),
    path('save_enquiry/',views.save_enquiry,name="save_enquiry"),
    path('enquiry/',views.enquiry,name="enquiry"),
    path('viewall_tour/',views.viewall_tour,name="viewall_tour"),
    path('delete_package/',views.delete_package,name="delete_package"),
    path('update_package/',views.update_package,name="update_package"),
    path('updated_package/',views.updated_package,name="updated_package"),
    # path('package1/',views.package1,name="package1"),
    path('places/',views.places,name="places"),
    path('book_now/',views.book_now,name="book_now"),

    path('pack_details/',views.pack_details,name="pack_details"),

    path('refreshcode/',views.refreshcode,name="refreshcode"),
    path('checkcode/',views.checkcode,name="checkcode"),
    path('checkemail/',views.checkemail,name="checkemail"),
    path('checkcontact/',views.checkcontact,name="checkcontact")


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)