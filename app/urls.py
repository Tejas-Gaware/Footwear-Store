from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetFrom, MyPasswordChangeForm, MySetPasswordForm


urlpatterns = [
    
    # home, products, contact us
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('products/<int:pk>', views.product_view, name='product-view'),
    path('contact-us/', views.contact_us, name="contact"),
    
    # Cart
    path('cart/', views.show_cart, name='cart'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('plus_cart/', views.plus_cart),
    path('minus_cart/', views.minus_cart),
    path('remove_cart/', views.remove_cart),
    
    # Purchase - checkout, payment success, orders, view order, generate receipt
    path('checkout/', views.checkout.as_view(), name='checkout'),
    path('paymentDone/', views.payment_done, name='paymentDone'),
    path('orders/', views.orders, name='orders'),
    path('orders/<int:pk>', views.qr_generator, name='orders'),
    path('receipt/<int:i>/<int:pk>/', views.receipt, name='receipt'),
    
    # Profile - User login, register, view profile, user logout
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('register/', views.CustomerRegistrationView.as_view(), name='register'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Address - delete, update
    path('account/<int:pk>', views.delete_address, name='deleteAddress'),
    path('updateAddress/<int:pk>',views.updateAddress.as_view(), name='updateAddress'),
    
    
    # Password Change
    path('changePassword/', auth_view.PasswordChangeView.as_view(template_name='app/password_reset.html', form_class=MyPasswordChangeForm, success_url='/password_changed'), name='changePassword'),
    path('password_changed/', auth_view.PasswordChangeDoneView.as_view(template_name='app/success.html'), name='password_changed'),
    
    
    # Forgot password
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/forgot-password.html', form_class=MyPasswordResetFrom), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/email_sent.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/forgot-password-confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/success.html'), name='password_reset_complete'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)