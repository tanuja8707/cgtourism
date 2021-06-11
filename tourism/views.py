from django.http import JsonResponse
from django.shortcuts import render, redirect
from tourism.models import *
from django.contrib import messages
from django.db import IntegrityError
import random
from captcha.image import ImageCaptcha
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from cgtourism.settings import EMAIL_HOST_USER

scode = ""
def generate_captcha():
    global scode
    scode = random.randint(100000, 999999)
    ic = ImageCaptcha()
    ic.write(str(scode), "tourism/static/captcha/captcha.png")

OTP = ""
def otpGenete():
    otp = random.randint(100000,999999)
    return otp

def showIndex(request):
    return render(request,"index.html")


def about(request):
    return render(request, "aboutus.html")


def about_food(request):
    return render(request,"food.html")


def user_login(request):
    generate_captcha()
    return render(request,"user_login.html")


def validate_user(request):
    usr = request.POST.get("t1")
    pwd = request.POST.get("t2")
    if request.method == "POST":
        try:
            result = CustomerModel.objects.get(email=usr, password=pwd)
            request.session['user_id'] = result.cno
            request.session['user_name'] = result.name
            return render(request, "Welcome_user.html", {"data": result})
        except CustomerModel.DoesNotExist:
            return render(request, "user_login.html", {"error": "Invalid User"})
    else:
        del request.session['user_id']
        return redirect('user_login')


def new_user(request):
    generate_captcha()
    return render(request,"user_registration.html")

em = ""
def validate_newuser(request):
    global em
    nm = request.POST.get("t1")
    em = request.POST.get("t2")
    cn = request.POST.get("t3")
    pwd = request.POST.get("t4")
    im = request.FILES["t5"]
    global OTP
    OTP = otpGenete()
    send_to = em.split(",")
    send_to_subject = "Registration OTP"
    send_to_message = "Your CG-Tourism Registration OTP is : " + str(OTP)
    send_mail(send_to_subject, send_to_message, EMAIL_HOST_USER, send_to)
    CustomerModel(name=nm,email=em,contact=cn,password=pwd,photo=im).save()
    print(OTP)
    return render(request,"otp_validation.html",{"msg":"Otp Send Your Registered Email-Id"})


def validate_otp(request):
    otp = int(request.POST.get('t1'))
    if OTP == otp:
        send_to = em.split(",")
        send_to_subject = "Registration Confirmation"
        send_to_message = "Your CG-Tourism Registration is Completed"
        send_mail(send_to_subject, send_to_message, EMAIL_HOST_USER, send_to)
        return redirect('user_login')
    else:
        return render(request,"otp_validation.html",{"msg":"Invalid Otp! Please Enter Valid Otp"})


def forgot_pass_form(request):
    generate_captcha()
    return render(request,"forgot_pass_form.html")

def forgot_password(request):
    email = request.POST.get("t1")
    contact = request.POST.get("t2")
    try:
        res = CustomerModel.objects.get(email=email,contact=contact)
        send_to = res.email.split(",")
        send_to_subject = "Forgot Password"
        send_to_message = "Your CG-Tourism Registration Password id : "+str(res.password)
        send_mail(send_to_subject, send_to_message, EMAIL_HOST_USER, send_to)
        return render(request, "forgot_pass_form.html", {"msg":"Password Send Your Registered Email-Id"})
    except CustomerModel.DoesNotExist:
        return render(request,"forgot_pass_form.html",{"msg":"Invalid Details"})


def adminlogin(request):
    return render(request,'adminlogin.html')


def adminHome(request):
    return render(request,'welcomeAdmin.html')


def validate_Admin(request):
    username = request.POST.get("t1")
    password = request.POST.get("t2")
    if request.method == "POST":
        try:
            res = AdminModel.objects.get(username=username,password=password)
            request.session['admin_id'] = res.idno
            request.session['name'] = res.name
            return render(request,"welcomeAdmin.html")
        except CustomerModel.DoesNotExist:
            return render(request, 'adminlogin.html', {'message': 'User Name & Password incorrect !!!!'})
    else:
        del request.session['admin_id']
        del request.session['name']
        return redirect('adminlogin')


def tour_package(request):
    return render(request,"view_packages.html",{"data":PackageModel.objects.all()})


def add_package(request):
    return render(request,"addPackage.html")


def insert_package(request):
    nm = request.POST.get("p1")
    dura = request.POST.get("p2")
    desc = request.POST.get("p3")
    pr = request.POST.get("p4")
    rat = request.POST.get("p5")
    img = request.FILES["p6"]
    try:
        PackageModel(pname=nm, pduration=dura,pdescription=desc,price=pr,prating=rat,image=img).save()
        return redirect('add_package')
    except IntegrityError:
        return render(request,"addPackage.html",{"error":"Packege is Allready Added"})


def enquiry(request):
    generate_captcha()
    return render(request,"enquiry.html")


def save_enquiry(request):
    nm = request.POST.get("p1")
    em = request.POST.get("p2")
    cn = request.POST.get("p3")
    dt = request.POST.get("p4")
    np = request.POST.get("p5")
    msg = request.POST.get("p6")
    try:
        EnquiryModel(name=nm,email=em,phone=cn,date_of_travel=dt,no_of_people=np,message=msg).save()
        return redirect('tour_package')
    except IntegrityError:
        return render(request,"enquiry.html",{"error":"Your Enquiry Form is Allready Submitted" })


def viewall_tour(request):
    return render(request,"viewall_tour.html",{"data":PackageModel.objects.all()})


def delete_package(request):
    idno = request.GET.get("pckid")
    PackageModel.objects.filter(pid=idno).delete()
    messages.success(request, "File Deleted")
    return redirect('viewall_tour')


def update_package(request):
    idno = request.GET.get("pckid")
    result = PackageModel.objects.get(pid=idno)
    return render(request, "update_package.html", {"data": result})


def updated_package(request):
    idno = request.POST.get("p1")
    nm = request.POST.get("p2")
    dura = request.POST.get("p3")
    desc = request.POST.get("p4")
    rat = request.POST.get("p5")
    img = request.FILES["img"]
    try:
        PackageModel.objects.filter(pid=idno).update(pname=nm,pduration=dura,pdescription=desc,prating=rat,image=img)
        # result.pname = nm
        # result.pduration = dura
        # result.pdescription = desc
        # result.prating = rat
        # result.image = img
        # result.save()
        messages.success(request,"Package Updated")
        return redirect('viewall_tour')
    except PackageModel.DoesNotExist():
        return render(request, "viewall_tour.html", {"msg":"Package Does Not Exist!"})


# def package1(request):
#     return render(request, "package1.html")

def pack_details(request):
    pid = request.GET.get("pid")
    result = PackDetailsModel.objects.get(pid=pid)
    print(result)
    if pid == "1":
        return render(request,"package1.html",{"data":result})
    elif pid == "2":
        return render(request,"package2.html",{"data":result})
    elif pid == "3":
        return render(request,"package3.html",{"data":result})
    elif pid == "4":
        return render(request,"package4.html",{"data":result})
    elif pid == "5":
        return render(request,"package5.html",{"data":result})
    else:
        return render(request,"package6.html",{"data":result})




def places(request):
    return render(request,"places.html",{"data":PackageModel.objects.all()})


def book_now(request):
    idno = request.GET.get("bookid")
    result = PackageModel.objects.get(pid=idno)
    return render(request, "book_package.html", {"data": result})


# calling this function through javascript
@method_decorator(csrf_exempt,name='dispatch')
def refreshcode(request):
    generate_captcha()
    res = {"message": "Refresh Security Code"}
    return JsonResponse(res)


@method_decorator(csrf_exempt,name='dispatch')
def checkcode(request):
    code = int(request.POST.get("cname"))
    if scode != code:
        res = {"error": "Invalid Security Code"}
    else:
        res = {"message": "Valide Security Code"}
    return JsonResponse(res)


@method_decorator(csrf_exempt,name='dispatch')
def checkemail(request):
    email = (request.POST.get("cname"))
    try:
        CustomerModel.objects.get(email=email)
        res = {"error": "Email is Allready Registerd"}
    except CustomerModel.DoesNotExist:
        res = {"message": "Email is Available"}
    return JsonResponse(res)


@method_decorator(csrf_exempt,name='dispatch')
def checkcontact(request):
    contact = (request.POST.get("cname"))
    try:
        CustomerModel.objects.get(contact=contact)
        res = {"error": "Contact is Allready Registerd"}
    except CustomerModel.DoesNotExist:
        res = {"message": "Contact is Available"}
    return JsonResponse(res)


