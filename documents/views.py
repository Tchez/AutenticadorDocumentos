from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
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
    load_public_key_from_pem,
    verify_signature,
    verify_integrity,
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

        private_key_pem = request.user.private_key

        try:
            private_key = load_private_key_from_pem(private_key_pem)
        except Exception as e:
            print("Erro ao carregar a chave:", e)

        # private_key = load_private_key_from_pem(private_key_pem)

        new_signature = sign_message(document.content, private_key)
        document.signature = new_signature
        document.signed_hash = generate_hash(document.content)
        document.save()

        return redirect("list_documents")


class VerifySignatureView(View):
    def get(self, request, pk):
        document = get_object_or_404(Document, id=pk)

        public_key_pem = document.owner.public_key

        try:
            public_key = load_public_key_from_pem(public_key_pem)
        except Exception as e:
            print("Erro ao carregar a chave:", e)

        is_signature_valid = verify_signature(
            document.content,
            document.signature.encode("utf-8"),
            public_key,
        )

        is_hash_valid = verify_integrity(document.content, document.signed_hash)

        if is_signature_valid and is_hash_valid:
            print("Documento e assinatura são válidos!")
            # Aqui você pode redirecionar para uma página de sucesso ou atualizar o modelo TODO: Criar pagina para sucesso
        else:
            print("Documento ou assinatura são inválidos!")
            # Aqui você pode redirecionar para uma página de erro ou atualizar o modelo

        return redirect("list_documents")
