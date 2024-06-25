from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views
from app.chat.views import ChatView, MessageListView, ConversationsView, DeleteConversationView

urlpatterns = [
    path('', views.ProductListView.product_list, name= 'product_list'),
    path('create_product/', views.ProductCreateView.as_view(), name= 'create_product'),
    path('product_detail/<slug:pk>/', views.ProductDetailView.product_detail, name= 'product_detail'),
    path('cart/<int:pk>/', views.CartView.cart_view, name= 'cart_views'),
    path('checkout/<int:pk>/', views.CheckoutView.check_out, name= 'checkout'),
    path('delete/<int:pk>/', views.DeleteProductView.delete_product_from_model, name='delete_product'),
    path('product/<int:pk>/edit/', views.EditProductView.edit_product, name='edit_product'),
    path('search/', views.SearchProductView.search_view, name='search'),
    path('category/<int:pk>/', views.CategoryView.category, name='category'),


    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('edit_account/', views.EditAccountView.edit_account, name='edit_account'),

    # Chat
    path('conversations/', ConversationsView.conversations, name='conversations'),
    path('chat/<int:pk>/', ChatView.chat, name='chat'),
    path('api/messages/', MessageListView.as_view(), name='message_sender'),
    path('api/messages/<int:sender>/<int:receiver>/', MessageListView.as_view(), name='message_receiver'),
    path('delete_conversation/<int:pk>/', DeleteConversationView.delete_conversation, name='delete_conversation'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)