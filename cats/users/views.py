from django.shortcuts import render, redirect
from .utils import optimize_image
from .forms import CustomUserCreationForm
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.email = form.cleaned_data['email']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                if 'image' in request.FILES:
                    # optimized_image, new_name = optimize_image(request.FILES['image'], max_size=(300, 300))
                    # user.image_small.save(new_name, optimized_image, save=False)
                    # optimized_image, new_name = optimize_image(request.FILES['image'], max_size=(600, 600))
                    # user.image_medium.save(new_name, optimized_image, save=False)
                    optimized_image, new_name = optimize_image(request.FILES['image'], max_size=(1200, 1200))
                    user.image.save(new_name, optimized_image, save=False)
                user.save()
                return redirect('users:index')
            except Exception as e:
                messages.error(request, f'Помилка при реєстрації: {str(e)}')
        else:
            messages.success(request, 'Виправте помилки в формі')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def index(request):
    form = CustomUser.objects.all()
    return render(request, 'home.html', {'form': form})

def users(request):
    users = CustomUser.objects.all()
    return render(request, 'users.html', {'users': users})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        username = request.POST['username']  # або як називається поле у формі
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # або інша сторінка після входу
        else:
            messages.error(request, 'Невірний логін або пароль')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('users:index')  # або на головну, якщо хочеш