# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ActivityForm
from .models import Activity
from django.contrib.auth.decorators import login_required
import matplotlib.pyplot as plt
import os
import io
from django.conf import settings
from django.core.files.base import ContentFile
from project27.settings import MEDIA_ROOT


def home(request):
    signup_form = CustomUserCreationForm()
    login_form = CustomAuthenticationForm()
    return render(
        request, "home.html", {"signup_form": signup_form, "login_form": login_form}
    )


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "signup.html", {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    form = CustomAuthenticationForm()
    signup_form = CustomUserCreationForm()
    return render(request, 'home.html', {'login_form': form, 'signup_form': signup_form})



@login_required
def dashboard(request):
    try:
        activity = Activity.objects.get(user=request.user)
        initial_data = {
            "study_hours": activity.study_hours,
            "play_hours": activity.play_hours,
            "sleep_hours": activity.sleep_hours,
            "tv_hours": activity.tv_hours,
        }
    except Activity.DoesNotExist:
        activity = None
        initial_data = None

    if request.method == "POST":
        form = ActivityForm(request.POST, initial=initial_data)
        if form.is_valid():
            if activity:
                activity.study_hours = form.cleaned_data["study_hours"]
                activity.play_hours = form.cleaned_data["play_hours"]
                activity.sleep_hours = form.cleaned_data["sleep_hours"]
                activity.tv_hours = form.cleaned_data["tv_hours"]
                activity.save()
            else:
                activity = Activity.objects.create(
                    user=request.user,
                    study_hours=form.cleaned_data["study_hours"],
                    play_hours=form.cleaned_data["play_hours"],
                    sleep_hours=form.cleaned_data["sleep_hours"],
                    tv_hours=form.cleaned_data["tv_hours"],
                )
            return redirect("dashboard")
    else:
        form = ActivityForm(initial=initial_data)

    # Generate the chart image path
    state=generate_bar_graph(request.user)
    graph_image_path=None
    if state:
        graph_image_path = f"/media/chart/{request.user.username}_chart.png"

    # Assign the chart image path to activity.image
    # if activity is not None:
    #     activity.image = graph_image_path
    #     activity.save()
    # print(MEDIA_ROOT)
    print("Activity image", graph_image_path)

    return render(
        request, "dashboard.html", {"form": form, "graph_image_path": graph_image_path}
    )


def generate_bar_graph(user):
    try:
        activity_instance = Activity.objects.get(user=user)
    except Activity.DoesNotExist:
        return None

    chart_dir = os.path.join(settings.MEDIA_ROOT, "chart")
    if not os.path.exists(chart_dir):
        os.makedirs(chart_dir)

    # Your code to generate the chart image using Matplotlib
    # For demonstration purposes, let's create a simple example
    colors = ["#FF5733", "#33FF57", "#3357FF", "#F4FF33"]
    plt.bar(
        ["Study", "Play", "Sleep", "TV"],
        [
            activity_instance.study_hours,
            activity_instance.play_hours,
            activity_instance.sleep_hours,
            activity_instance.tv_hours,
        ],
        color=colors,
    )
    plt.xlabel("Activity")
    plt.ylabel("Hours")
    plt.title("Activity vs Hours")

    # Save the chart image to a file
    image_path = os.path.join(chart_dir, f"{user.username}_chart.png")
    plt.savefig(image_path)

    # Close the Matplotlib plot to free up resources
    plt.close()

    # Update the Activity instance's image field with the path to the saved image
    activity_instance.image = image_path
    activity_instance.save()

    return image_path
