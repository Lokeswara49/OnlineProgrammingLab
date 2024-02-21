from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth.models import User  # pre defined models package
from django.contrib import messages, auth
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from OnlineProgrammingLab import settings
from .tokens import generate_token


# Create your views here.
def index(request):
    return render(request, "auth/index.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')  # name of element in form
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            firstname = user.first_name
            return redirect("home")
        else:
            messages.error(request, "Credentials Mismatch")
            return redirect('login')

    return render(request, "auth/login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')  # name of element in form
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if User.objects.filter(username=username):
            messages.error(request, "USERNAME ALREADY EXISTS!!!")
            return redirect('register')

        if User.objects.filter(email=email):
            messages.error(request, "EMAIL ALREADY EXISTS!!!")
            return redirect('register')

        if password != cpassword:
            messages.error(request, "PASSWORD MISMATCH...")
            return redirect('register')

        # we collected data from form now we make a model using contrib.auth.models User
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.is_active = False
        myuser.save()

        # now to notify user about successful registration we use django messages

        messages.success(request, "A VERIFICATION LINK HAS BEEN SENT TO YOUR MAIL. PLEASE CONFIRM IT ")

        """
        # welcome mail
        subject = "Welcome to SAY-Online Programming Platform"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to ONLINE PROGRAMMING PLATFORM"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        """
        # Confirmation Email

        current_site = get_current_site(request)
        subject = "Welcome to SAY-Online Programming Platform -- CONFIRM EMAIL"
        message = render_to_string('auth/email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser),
        })
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )

        email.fail_silently = True
        email.send()

        return redirect("login")

    return render(request, "auth/register.html")


def logout(request):
    auth.logout(request)
    messages.success(request, "LOGGED OUT SUCCESSFULLY")
    return redirect('index')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        auth.login(request, myuser)
        context={'user':myuser}
        return render(request,'auth/verified.html',context)
    else:
        return render(request, 'auth/activation_fail.html')
