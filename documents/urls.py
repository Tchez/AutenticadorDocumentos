from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.DocumentCreateView.as_view(), name="create_document"),
    path("list/", views.DocumentListView.as_view(), name="list_documents"),
    path("edit/<int:pk>/", views.DocumentUpdateView.as_view(), name="edit_document"),
    path(
        "delete/<int:pk>/", views.DocumentDeleteView.as_view(), name="delete_document"
    ),
    path("view/<int:pk>/", views.DocumentDetailView.as_view(), name="view_document"),
    path("sign/<int:pk>/", views.SignDocumentView.as_view(), name="sign_document"),
    path(
        "verify/<int:pk>/", views.VerifySignatureView.as_view(), name="verify_document"
    ),
]
