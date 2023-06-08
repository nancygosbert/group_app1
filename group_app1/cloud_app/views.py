from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Car, Member
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordResetView

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Perform any necessary validation on the form data
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'signup.html')

        # Check if the email already exists
        if Member.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, 'signup.html')

        # Save the data to the database
        member = Member.objects.create_member(email=email, password=password, first_name=first_name, last_name=last_name)

        # Redirect the user to a success page or any other desired page
        return redirect('login')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me', False)

        # Authenticate user
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Login the user
            login(request, user)
            # Redirect the user to the desired page
            return redirect('index')
        else:
            # Invalid credentials, show error message
            user_exists = User.objects.filter(email=email).exists()
            if user_exists:
                messages.error(request, 'Invalid password.')
            else:
                messages.error(request, 'Invalid email or username.')

    return render(request, 'login.html', {'messages': messages.get_messages(request)})


@login_required
def register_car(request):
    if request.method == 'POST':
        owner_name = request.POST.get('owner_name')
        country = request.POST.get('country')
        plate_number = request.POST.get('plate_number')
        color = request.POST.get('color')
        model = request.POST.get('model')

        # Create a new Car object and save it to the database
        car = Car(owner_name=owner_name, country=country, plate_number=plate_number, color=color, model=model)
        car.save()

        # Redirect to a success page or any other desired URL
        return redirect('index')

    # If the request method is not POST, render the form template
    return render(request, 'register_car.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def view_all_cars(request):
    cars = Car.objects.all()
    return render(request, 'view_all_cars.html', {'cars': cars})


def forgot(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Check if the email exists in the database
        try:
            user = Member.objects.get(email=email)
        except Member.DoesNotExist:
            # Email does not exist, handle the error gracefully
            return render(request, 'forgot.html', {'error': 'Email not found'})

        # Generate a password reset token
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)

        # Build the password reset link
        current_site = get_current_site(request)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://{current_site.domain}/reset-password/{uid}/{token}"

        # Send the password reset link to the user's email
        subject = "Reset Your Password"
        message = render_to_string('reset_password_email.html', {
            'user': user,
            'reset_link': reset_link,
        })
        send_mail(subject, message, 'noreply@example.com', [email])

        # Return a success message to the user
        return render(request, 'forgot.html', {'success': 'Reset password link has been sent to your email'})

    return render(request, 'forgot.html')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'cloud_app/reset_password_email.html'
    email_template_name = 'cloud_app/reset_password_email.html'
    success_url = reverse_lazy('cloud_app:password_reset_done')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            self.send_password_reset_email(user)
            # Optionally, you can add any additional logic here
            # such as setting a success message or redirecting the user
            # to a different page.
        except User.DoesNotExist:
            # Handle the case when the user with the given email doesn't exist
            # For example, you can display an error message to the user.
            pass

    def send_password_reset_email(self, user):
        # Implement your email sending logic here
        # You can use Django's built-in EmailMessage or any third-party library
        # to send the password reset email to the user.
        # Make sure to include the reset password link in the email.
        pass
