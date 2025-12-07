

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt



from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
@csrf_exempt
def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Basic validation
        if password != password2:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Account created successfully")
            # return redirect('login')

    return render(request, 'register.html')

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('shops:home')  # redirect to a home page or dashboard
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('shops:map')













from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Shop, Category
from django.contrib.gis.geos import Point

# --------------------------
# Create Category (no forms)
# --------------------------
@login_required
def category_create(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()

        if not name:
            messages.error(request, "Category name is required.")
        elif Category.objects.filter(name=name, user=request.user).exists():
            messages.error(request, "Category already exists.")
        else:
            category = Category.objects.create(name=name, user=request.user)
            messages.success(request, f"Category '{name}' created successfully!")
            return redirect("shops:map")

    return render(request, "category_create.html")
    

# --------------------------
# Create Shop (no forms)
# --------------------------
# @login_required
@login_required
def shop_create(request):
    categories = Category.objects.filter(user=request.user)

    # Pre-fill lat/lng from GET params
    lat = request.GET.get("lat", "")
    lng = request.GET.get("lng", "")

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        category_id = request.POST.get("category")
        lat = request.POST.get("lat")
        lng = request.POST.get("lng")

        if not name or not category_id or not lat or not lng:
            messages.error(request, "All fields are required.")
        else:
            try:
                category = Category.objects.get(id=category_id, user=request.user)
                location = Point(float(lng), float(lat))  # GIS Point expects (lng, lat)
                shop = Shop.objects.create(
                    name=name,
                    category=category,
                    location=location,
                    user=request.user
                )
                messages.success(request, f"Shop '{name}' created successfully!")
                return redirect("shops:map")
            except Category.DoesNotExist:
                messages.error(request, "Invalid category selected.")
            except ValueError:
                messages.error(request, "Invalid coordinates.")

    return render(request, "shop_create.html", {
        "categories": categories,
        "lat": lat,
        "lng": lng
    })




from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D

def shops_map(request):
    if request.user.is_authenticated:
        shops = Shop.objects.filter(user=request.user)  # Only user's shops
    else:
        shops = Shop.objects.filter(is_active=True)  # Show all active shops for guests

        # Filter by search query
        query_name = request.GET.get('name')
        if query_name:
            shops = shops.filter(name__icontains=query_name)

        # Filter by category
        category_id = request.GET.get('category')
        if category_id:
            shops = shops.filter(category_id=category_id)

        # Nearby search
        # Nearby search
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        radius = request.GET.get('radius', 50)  # default 5 km

        if lat and lng:
            user_location = Point(float(lng), float(lat), srid=4326)

            shops = (
                shops
                .annotate(distance=Distance('location', user_location))
                .filter(location__distance_lte=(user_location, D(km=float(radius))))
                .order_by('distance')
            )
    categories = Category.objects.all()
    
    return render(request, "shops_map.html", {
        "shops": shops,
        "categories": categories,
        "query_name": request.GET.get('name', ''),
        "selected_category": int(request.GET.get('category')) if request.GET.get('category') else None,
        "lat": request.GET.get('lat', ''),
        "lng": request.GET.get('lng', ''),
        "radius": request.GET.get('radius', '')
    })



@login_required
def home(request):
    shops = Shop.objects.filter(user=request.user)
    print(shops,"===================")
    return render(request, "shops_map.html", {"shops": shops})




from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Shop
from .forms import ShopForm,ShopFormEdit  # Create a ModelForm for Shop
from django.http import JsonResponse

@login_required
def shop_update(request, pk):
    shop = get_object_or_404(Shop, pk=pk, user=request.user)

    if request.method == "POST":
        form = ShopFormEdit(request.POST, instance=shop)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": "Successfully updated"})
        return JsonResponse({"success": False, "errors": form.errors})

    else:
        form = ShopFormEdit(instance=shop)
        return render(request, "shop_edit_form.html", {
            "form": form,
            "shop": shop,
        })

@login_required
def shop_delete(request, pk):
    shop = get_object_or_404(Shop, pk=pk, user=request.user)  # Only allow owner
    shop.delete()
    messages.success(request, f"Shop '{shop.name}' has been deleted successfully.")
    return redirect('shops:home')  # Redirect back to user's shops map

@login_required
def shop_toggle_active(request, pk):
    """Enable/disable shop for other users"""
    shop = get_object_or_404(Shop, pk=pk, user=request.user)
    shop.is_active = not shop.is_active
    shop.save()
    return redirect('shops:myshops')




@login_required
def my_shops(request):
    shops = Shop.objects.filter(user=request.user)
    return render(request, "my_shops.html", {"shops": shops})