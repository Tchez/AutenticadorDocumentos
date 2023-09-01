from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .crypto_utils import generate_keypair


@login_required
def generate_keys(request):
    if request.method == "POST":
        private_key, public_key = generate_keypair()
        request.user.private_key = private_key
        request.user.public_key = public_key
        request.user.save()
        return redirect("show_my_keys")
    return render(request, "generate_keys.html")


@login_required
def show_my_keys(request):
    public_key = request.user.public_key
    private_key = request.user.private_key

    context = {
        "public_key": public_key,
        "private_key": private_key,
    }

    return render(request, "show_my_keys.html", context)
