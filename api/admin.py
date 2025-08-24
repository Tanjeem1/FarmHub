from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Farm, Cow, Activity, MilkProduction

# creating inline with tabulerinline so that can easily see the field objects inide the choosen model in admin panel with table style



# it will give Inline for Farmers inside Farm model
class FarmerInline(admin.TabularInline):
    model = User
    extra = 1
    fields = ['username', 'email', 'password', 'role']
    show_change_link = True
    verbose_name = "Farmer"
    verbose_name_plural = "Farmers"

    def get_queryset(self, request):
        return super().get_queryset(request).filter(role='farmer')

# will give Inline for Cows inside User model
class CowInline(admin.TabularInline):
    model = Cow
    extra = 1
    fields = ['tag', 'breed', 'owner']
    show_change_link = True

# will give Inline for Activities and MilkProduction model  inside Cow in admin panel
class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 1
    fields = ['type', 'date', 'details']

class MilkProductionInline(admin.TabularInline):
    model = MilkProduction
    extra = 1
    fields = ['date', 'amount']


# registering all the model


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'farm', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('FarmHub', {'fields': ('role', 'farm')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'role', 'farm', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    inlines = [CowInline]
    list_per_page = 25


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ('name', 'agent', 'farmer')
    list_filter = ('agent',)
    search_fields = ('name', 'agent__username')
    inlines = [FarmerInline]
    list_per_page = 25

    def farmer(self, obj):
        farmer = obj.farmers.first()
        return farmer.username if farmer else 'None'

@admin.register(Cow)
class CowAdmin(admin.ModelAdmin):
    list_display = ('tag', 'breed', 'owner', 'farm')
    list_filter = ('breed', 'owner__farm')
    search_fields = ('tag', 'owner__username')
    inlines = [ActivityInline, MilkProductionInline]
    list_per_page = 25

    def farm(self, obj):
        return obj.owner.farm.name if obj.owner.farm else 'None'


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('cow', 'type', 'date', 'details')
    list_filter = ('type', 'date', 'cow__owner__farm')
    search_fields = ('cow__tag', 'details')
    list_per_page = 25


@admin.register(MilkProduction)
class MilkProductionAdmin(admin.ModelAdmin):
    list_display = ('cow', 'date', 'amount', 'farm')
    list_filter = ('date', 'cow__owner__farm')
    search_fields = ('cow__tag',)
    list_per_page = 25

    def farm(self, obj):
        return obj.cow.owner.farm.name if obj.cow.owner.farm else 'None'
