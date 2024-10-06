import base64

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from itsdangerous import URLSafeTimedSerializer
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password

from EpicAiDesign import settings
from .decorator import custom_login_required
from .models import User

serializer = URLSafeTimedSerializer(settings.SECRET_KEY)


def user_list(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('name')
        password = request.POST.get('password')
        checkPassword = request.POST.get('check_password')

        if request.FILES.get('profile_image') is not None:
            profile_image = request.FILES.get('profile_image')
        else:
            profile_image = None

        if password != checkPassword:
            messages.error(request, "Passwords don't match.")
            return redirect('signup')

        if User.objects(email=email).first() is not None:
            messages.error(request, "User with this email already exists.")
            return redirect('signup')

        user = User(
            username=username,
            email=email,
            password=make_password(password),
            image=profile_image
        )

        user.save()
        messages.success(request, "User created successfully!")
        return redirect('login')

    return render(request, 'signup.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects(email=email).first()
        if user and check_password(password, user.password):
            request.session['user_id'] = str(user.id)
            request.session['user_name'] = str(user.username)
            request.session['user_email'] = str(user.email)
            if user.image:
                image = user.image.read()
                img_str = base64.b64encode(image).decode('utf-8')
                request.session['profile_image'] = f"data:image/jpeg;base64,{img_str}"
            if user.verified:
                messages.success(request, "Logged in successfully!")
                return redirect('login')
            else:
                user.token = create_token(user.email)
                user.save()
                sendVerifyEmail(user.email)
                messages.error(request, "You need to verify your email!")
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')
    return render(request, 'login.html')


@custom_login_required
def profile(request):
    nom = "nejd"
    return render(request, 'profile.html', {'user_name': nom})


@custom_login_required
def personalInfo(request):
    return render(request, 'userDetails.html')


def logout_user(request):
    request.session.clear()
    return redirect('login')


def sendVerifyEmail(email):
    user = User.objects(email=email).first()
    subject = 'Verify Email!'
    link = "http://127.0.0.1:8000/users/verifyEmail?token=" + user.token
    html_message = render_to_string('verifyemail.html', {'name': user.username, 'link': link})
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    email = EmailMultiAlternatives(subject, '', from_email, recipient_list)
    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)


def verifyEmail(request):
    token = request.GET.get('token')
    if token:
        user = User.objects(token=token).first()
        if user and verify_token(user.token):
            user.verified = True
            user.save()
            messages.success(request, "Your email has been verified! You can now log in.")
            return redirect('login')
        messages.error(request, "Token Expired.")
        return redirect('login')


def create_token(email):
    return serializer.dumps(email, salt='email-confirmation-salt')


def verify_token(token, expiration=3600):
    try:
        email = serializer.loads(token, salt='email-confirmation-salt', max_age=expiration)
    except Exception as e:
        return None
    return email
