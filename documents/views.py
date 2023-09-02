from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView,
)
from users.crypto_utils import (
    sign_message,
    generate_hash,
    load_private_key_from_pem,
)
from .forms import DocumentForm
from .models import Document


class DocumentCreateView(LoginRequiredMixin, CreateView):
    model = Document
    form_class = DocumentForm
    template_name = "create_document.html"
    success_url = reverse_lazy("list_documents")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DocumentListView(LoginRequiredMixin, ListView):
    model = Document
    template_name = "list_documents.html"
    context_object_name = "documents"

    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user)


class DocumentUpdateView(LoginRequiredMixin, UpdateView):
    model = Document
    form_class = DocumentForm
    template_name = "edit_document.html"
    success_url = reverse_lazy("list_documents")

    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user)


class DocumentDeleteView(LoginRequiredMixin, DeleteView):
    model = Document
    template_name = "delete_document.html"
    success_url = reverse_lazy("list_documents")

    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user)


class DocumentDetailView(LoginRequiredMixin, DetailView):
    model = Document
    template_name = "view_document.html"

    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user)


class SignDocumentView(View):
    def get(self, request, pk):
        document = get_object_or_404(Document, id=pk)

        private_key_pem = document.owner.private_key

        try:
            private_key = load_private_key_from_pem(private_key_pem)
        except Exception as e:
            print("Erro ao carregar a chave:", e)

        hash = generate_hash(document.content)
        document.hash = hash
        concat = document.content + hash
        new_signature = sign_message(concat, private_key)
        document.signature = new_signature
        document.save()
        return redirect("list_documents")


class VerifySignatureView(View):
    def get(self, request, pk):
        if pk:
            document = get_object_or_404(Document, id=pk)
            is_valid_signature = document.verify_signature()

            context = {
                "document": document,
                "is_valid_signature": is_valid_signature,
            }

            return render(request, "verify_signature.html", context)
        else:
            return redirect("list_documents")


class VerifyHashView(View):
    def get(self, request):
        return render(request, "verify_hash.html")

    def post(self, request):
        hash = request.POST.get("hash_code")
        user = request.user
        document = Document.objects.filter(hash=hash).first()

        is_valid_hash = True if document else False
        is_user_owner = True if document.owner == user else False

        return render(
            request,
            "verify_hash.html",
            {
                "document": document,
                "hash": hash,
                "is_valid_hash": is_valid_hash,
                "is_user_owner": is_user_owner,
            },
        )
