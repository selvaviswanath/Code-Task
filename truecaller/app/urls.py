from django.urls import path

from app.views import GlobalContactViewSet, UserViewSet, ContactViewSet

urlpatterns = [
    path('users/<int:pk>/global-contacts', GlobalContactViewSet.as_view({'get': 'getGCList'}), name='global-contact-list'),
    path('users/<int:pk>/global-contacts/search-name', GlobalContactViewSet.as_view({'get': 'search_name'}), name='global-contact-search-name'),
    path('users/<int:pk>/global-contacts/search-phone-number', GlobalContactViewSet.as_view({'get': 'search_phone_number'}), name='global-contact-search-phone-number'),
    path('users/<int:pk>/mark_contact_as_spam', UserViewSet.as_view({'post': 'mark_contact_as_spam'}), name='user-mark-contact-as-spam'),
    path('users/', UserViewSet.as_view({'post': 'addUser'}), name='user-list'),
    path('users/<int:pk>/list_my_contacts', ContactViewSet.as_view({'get': 'getContacts'}), name='contact-list'),
    path('users/<int:pk>/add_contacts', UserViewSet.as_view({'post': 'add_contacts'}), name='user-add-contacts'),
]
