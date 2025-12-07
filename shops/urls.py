from django.urls import path
from . import views

app_name = "shops"

urlpatterns = [
    # Map views
    path("", views.shops_map, name="map"),                  # All shops map
    path("my/", views.my_shops, name="myshops"),
    path("home/", views.home, name="home"),           # User's shops
               # User's shops

    # Category & Shop creation (no forms)
    path("category/add/", views.category_create, name="category_add"),
    path("shop/add/", views.shop_create, name="shop_add"),

    # Authentication (no forms)
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    
    path("update/<int:pk>/", views.shop_update, name="shop_update"),
    path("delete/<int:pk>/", views.shop_delete, name="shop_delete"),
    path("toggle/<int:pk>/", views.shop_toggle_active, name="shop_toggle"),
    path('toggle/<int:pk>/', views.shop_toggle_active, name='shop_toggle_active'),  # <- this must exist

    # path("myshop/", views.api_my_shops, name="myshop"),

]
