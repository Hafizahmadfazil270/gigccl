from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ocrapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.login_page, name="login_page"),
    path("login_page", views.login_page, name="login_page"),
    
    path("register/", views.signup_page, name="register"),
    path("profile/", views.profile, name="profile"),
    path("logout/", views.logout_user, name="logout"),
    path("upload/", views.upload_page, name="upload"),
    path("__reload__/", include("django_browser_reload.urls")),
    path('home/',views.home,name='home'),
    path('dark_img_save/',views.dark_img_save,name='dark_img_save'),
    
    path('home/show_results', views.show_result, name = 'show_result/'),
    path('bright_image', views.bright_image, name = 'bright_image')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
