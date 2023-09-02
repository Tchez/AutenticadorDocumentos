from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .crypto_utils import generate_keypair_pem
from .forms import UserRegisterForm


def index(request):
    return render(request, "index.html")


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


@login_required
def generate_keys(request):
    if request.method == "POST":
        private_key, public_key = generate_keypair_pem()
        request.user.private_key = private_key
        request.user.public_key = public_key
        request.user.save()
        return redirect("show_my_keys")
    return render(request, "generate_keys.html")


@login_required
def show_my_keys(request):
    public_key = request.user.public_key

    context = {
        "public_key": public_key,
    }

    return render(request, "show_my_keys.html", context)
