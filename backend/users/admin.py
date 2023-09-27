from django.contrib import admin

from .models import User, Subscription


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username',
        'email', 'first_name',
        'last_name', 'subs_count',
        'recipe_count')
    search_fields = ('username', 'email',)
    empty_value_display = '-пусто-'

    @admin.display(description='Количество подписчиков')
    def subs_count(self, obj):
        return obj.followers.count()

    @admin.display(description='Количество рецептов')
    def recipe_count(self, obj):
        return obj.recipes.count()


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('follower', 'author',)
    search_fields = ('author',)


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
