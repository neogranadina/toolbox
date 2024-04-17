# pages/urls.py
from django.urls import path
from .views import home
from .views import (BautismoCreateView, MatrimonioCreateView, EntierroCreateView )
from .views import (PersonaCreateView, DocumentoCreateView, LugarCreateView, RelationshipCreateView)
from .views import (BautismoBrowse, MatrimonioBrowse, EntierroBrowse, PersonaBrowse, LugarBrowse,
                    DocumentoBrowse)
from .views import (BautismoDetailView, MatrimonioDetailView, EntierroDetailView, PersonaDetailView, 
                    LugarDetailView, DocumentoDetailView)
from .views import (BautismoUpdateView, MatrimonioUpdateView, EntierroUpdateView, PersonaUpdateView)
from .views import (BautismoDeleteView, MatrimonioDeleteView, EntierroDeleteView, PersonaDeleteView)
from .views import (PersonaAutocomplete, LugarAutocomplete, DocumentoAutocomplete)

urlpatterns = [
    path("", home, name="home_parroquia"),
    # create
    path('Form/new/persona/', PersonaCreateView.as_view(), name='persona-new'),
    path('Form/new/documento/', DocumentoCreateView.as_view(), name='documento-new'),
    path('Form/new/lugar/', LugarCreateView.as_view(), name='lugar-new'),
    path('Form/new/relationship', RelationshipCreateView.as_view(), name='relationship-new'),
    path('Form/new/bautismo', BautismoCreateView.as_view(), name='bautismo-new'),
    path('Form/new/matrimonio', MatrimonioCreateView.as_view(), name='matrimonio-new'),
    path('Form/new/entierro', EntierroCreateView.as_view(), name='entierro-new'),
    # update
    path("Form/update/bautismo/<int:pk>/", BautismoUpdateView.as_view(), name="bautismo-update"),
    path("Form/update/matrimonio/<int:pk>/", MatrimonioUpdateView.as_view(), name="matrimonio-update"),
    path("Form/update/entierro/<int:pk>/", EntierroUpdateView.as_view(), name="entierro-update"),
    path("Form/update/persona/<int:pk>/", PersonaUpdateView.as_view(), name="persona-update"),
    # delete
    path('bautismo/<int:pk>/delete/', BautismoDeleteView.as_view(), name='bautismo-delete'),
    path('matrimonio/<int:pk>/delete/', MatrimonioDeleteView.as_view(), name='matrimonio-delete'),
    path('entierro/<int:pk>/delete/', EntierroDeleteView.as_view(), name='entierro-delete'),
    path('persona/<int:pk>/delete/', PersonaDeleteView.as_view(), name='persona-delete'),
    # Detail
    path('Detail/bautismo/<int:pk>', BautismoDetailView.as_view(), name='bautismo-detail'),
    path("Detail/matrimonio/<int:pk>/", MatrimonioDetailView.as_view(), name='matrimonio-detail'),
    path("Detail/entierro/<int:pk>/", EntierroDetailView.as_view(), name="entierro-detail"),
    path("Detail/persona/<int:pk>/", PersonaDetailView.as_view(), name="persona-detail"),
    path("Detail/lugar/<int:pk>/", LugarDetailView.as_view(), name="lugar-detail"),
    path("Detail/documento/<int:pk>/", DocumentoDetailView.as_view(), name="documento-detail"),
    # Browse
    path('Browse/bautismos', BautismoBrowse.as_view(), name="bautismo-browse"),
    path('Browse/matrimonios', MatrimonioBrowse.as_view(), name="matrimonio-browse"),
    path('Browse/entierros', EntierroBrowse.as_view(), name="entierro-browse"),
    path('Browse/personas', PersonaBrowse.as_view(), name="persona-browse"),
    path('Browse/lugares', LugarBrowse.as_view(), name="lugares-browse"),
    path('Browse/documentos', DocumentoBrowse.as_view(), name="documentos-browse"),
    # autocompleters
    path('lugar-autocomplete/', LugarAutocomplete.as_view(), name='lugar-autocomplete'),
    path('persona-autocomplete/', PersonaAutocomplete.as_view(), name='persona-autocomplete'),
    path('documento-autocomplete/', DocumentoAutocomplete.as_view(), name='documento-autocomplete')
]