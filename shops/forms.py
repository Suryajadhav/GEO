from django import forms
from .models import Category, Shop
from leaflet.forms.widgets import LeafletWidget

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ("name", "category", "location")
        widgets = {
            "location": LeafletWidget(),
        }

class ShopFormEdit(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ("name", "category")
        widgets = {
            "location": LeafletWidget(),
        }