import base64

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from itsdangerous import URLSafeTimedSerializer
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password

import AlbumApp.models
import ImageApp.models
import MusicApp.models
import PoemApp.models
import SpeechApp.models
import VideoApp.models
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


def set_user_session(request, user):
    request.session['user_id'] = str(user.id)
    request.session['user_name'] = str(user.username)
    request.session['user_email'] = str(user.email)
    if user.image:
        image = user.image.read()
        img_str = base64.b64encode(image).decode('utf-8')
        request.session['profile_image'] = f"data:image/jpeg;base64,{img_str}"


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        skip = request.POST.get('skip')
        user = User.objects(email=email).first()
        if user and check_password(password, user.password):
            if skip or user.verified:
                set_user_session(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect('userInfo')
            else:
                user.token = create_token(user.email, "mail")
                user.save()
                sendVerifyEmail(user.email)
                messages.error(request, "You need to verify your email!")
        else:
            messages.error(request, "Invalid email or password.")
        return redirect('login')
    return render(request, 'login.html')


@custom_login_required
def profile(request):
    return render(request, 'profile.html', {})


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
            user.token = None
            user.save()
            messages.success(request, "Your email has been verified! You can now log in.")
            return redirect('login')
        messages.error(request, "Token Expired.")
        return redirect('login')


def create_token(email, type_mail):
    return serializer.dumps((email, type_mail), salt='email-confirmation-salt')


def verify_token(token, expiration=3600):
    try:
        email, type_mail = serializer.loads(token, salt='email-confirmation-salt', max_age=expiration)
        return email, type_mail
    except Exception as e:
        return None


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects(email=email).first()
        if user:
            user.token = create_token(user.email, 'password')
            sendRestPassword(user.email)
            user.save()
            messages.success(request, "A Reset Password Email Was Sent!")
            return redirect('login')
        messages.success(request, "Email Does Not Exist!")
        return redirect('resetPassword')
    return render(request, 'resetPassword.html')


def sendRestPassword(email):
    user = User.objects(email=email).first()
    subject = 'Reset Password!'
    link = "http://127.0.0.1:8000/users/reset_password?token=" + user.token
    html_message = render_to_string('resetpasswordmail.html', {'name': user.username, 'link': link})
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    email = EmailMultiAlternatives(subject, '', from_email, recipient_list)
    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)


def reset_password_view(request):
    token = request.GET.get('token')
    result = verify_token(token)

    if result:  # Check if result is not None
        email, type_mail = result
    else:
        messages.error(request, "Token Expired or Invalid!")
        return redirect('login')

    if request.method == 'POST':
        password = request.POST.get('password')
        checkPassword = request.POST.get('checkPassword')

        if password == checkPassword:
            user = User.objects(email=email).first()
            if user:
                user.password = make_password(password)
                user.token = None
                user.save()
                messages.success(request, "Password Changed!")
                return redirect('login')
            else:
                messages.error(request, "User not found!")
        else:
            messages.error(request, "Passwords don't match!")

        return render(request, 'resetPassword2.html', {'token': token})

    else:
        if type_mail == 'password' and email:
            return render(request, 'resetPassword2.html', {'token': token})
        else:
            messages.error(request, "Invalid token or request type!")
            return redirect('login')


def home(request):
    return render(request, 'home.html')


def editProfile(request):
    email = request.session.get('user_email')
    user = User.objects(email=email).first()
    if request.method == 'POST':
        name = request.POST.get('name')
        new_email = request.POST.get('email')
        password = request.POST.get('password')
        profile_image = request.FILES.get('profile_image')
        if check_password(password, user.password):
            user.username = name
            user.email = new_email
            if profile_image:
                if user.image:
                    user.image.replace(profile_image, content_type=profile_image.content_type)
                else:
                    user.image.put(profile_image, content_type=profile_image.content_type)
            user.save()
            request.session['user_email'] = new_email
            request.session['user_name'] = name
            if profile_image:
                image = user.image.read()
                img_str = base64.b64encode(image).decode('utf-8')
                request.session['profile_image'] = f"data:image/jpeg;base64,{img_str}"
            messages.success(request, "Profile updated successfully!")
            return redirect('userInfo')
        else:
            messages.error(request, "Invalid password. Please enter the correct password to update your profile.")
    return render(request, 'editProfile.html', {'user': user})


def gallery(request):
    data = None
    category = request.POST.get('category')
    sort = request.POST.get('sort')
    if sort is None:
        sort = 'created_at'
    if category is None:
        category = 'Images'
    albums = None
    match category:
        case "Images":
            data = ImageApp.models.ImageArt.objects.all().order_by(f"-{sort}")
        case "Music":
            data = MusicApp.models.MusicArt.objects.all().order_by(f"-{sort}")
            albums = AlbumApp.models.MusicAlbum.objects.all()
        case "Video":
            data = VideoApp.models.VideoArt.objects.all().order_by(f"-{sort}")
        case "Poem":
            data = PoemApp.models.PoemArt.objects.all().order_by(f"-{sort}")
        case "Speech":
            data = SpeechApp.models.Speech.objects.all().order_by(f"-{sort}")
    # match category:
    #     case "Images":
    #         data = ImageApp.models.ImageArt.objects(user=user).all().order_by(f"-{sort}")
    #     case "Music":
    #         data = MusicApp.models.MusicArt.objects(user=user).all().order_by(f"-{sort}")
    #         albums = AlbumApp.models.MusicAlbum.objects(user=user).all()
    #     case "Video":
    #         data = VideoApp.models.VideoArt.objects(user=user).all().order_by(f"-{sort}")
    #     case "Poem":
    #         data = PoemApp.models.PoemArt.objects(user=user).all().order_by(f"-{sort}")
    #     case "Speech":
    #         data = SpeechApp.models.Speech.objects(user=user).all().order_by(f"-{sort}")
    return render(request, 'gallery.html',
                  {'category': category, 'data': data, 'sort': sort, 'albums': albums})

