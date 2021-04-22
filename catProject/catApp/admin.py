from django.contrib import admin
from .models import Cat, Hunting, Loot


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ("name", "bodyColor", "gender", "owner")
    readonly_fields = ('gender',)
    
    def gender(self, obj):
        from django.utils.html import format_html
        if obj.gender:
            return format_html("✅")
        return format_html("❌")

@admin.register(Hunting)
class HuntingAdmin(admin.ModelAdmin):
    list_display = ("dateStart", "dateEnd", "hunter")

@admin.register(Loot)
class LootAdmin(admin.ModelAdmin):
    list_display = ("lootType", "hunting")
