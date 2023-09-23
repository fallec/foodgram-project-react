from django.contrib import admin

from .models import ShoppingList, Subscription, Favorite


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
    search_fields = ('user__username',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
    search_fields = ('user__username',)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'author',)
    search_fields = ('follower__username',)


admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
