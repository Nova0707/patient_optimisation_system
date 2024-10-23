from django.urls import path
from .views import signup, signin, logout_view, add_shift, receptionist_panel, book_slot, doctor_panel, user_panel

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('logout/', logout_view, name='logout'),
    path('user-panel/', user_panel, name='user_panel'),
    path('add_shift/', add_shift, name='add_shift'),
    path('receptionist/', receptionist_panel, name='receptionist_panel'),
    path('book_slot/<int:slot_id>/', book_slot, name='book_slot'),
    path('doctor_panel/', doctor_panel, name='doctor_panel'),
]
