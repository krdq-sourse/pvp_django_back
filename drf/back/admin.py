from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *


class ProfileInlime(admin.StackedInline):
    model = UserProfile
    fields=[field.name for field in UserProfile._meta.get_fields()]
    extra = 0  


class StatisticInlime(admin.StackedInline):
    model = UserStatistic
    fields=[field.name for field in UserStatistic._meta.get_fields()]
    extra = 0      
    

class UserItemsInline(admin.TabularInline):
    model = UserItems
    fields=['product', 'count', 'active']
    extra = 0

class PlayerInlime(admin.StackedInline):
    model = Player
    fields=[field.name for field in Player._meta.get_fields()]
    extra = 0  

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('steamID', 'coins', 'rp', 'total_coins', 'ban_status', 'add_hero')
    list_display_links = ('steamID', )
    search_fields = ['steamID']
    inlines = [UserItemsInline, ProfileInlime, StatisticInlime]


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',) 


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'can_upgrade')
    list_display_links = ('name', )


@admin.register(ShopHistory)
class ShopHistory(admin.ModelAdmin):
    list_display = ('steamID', "coins", "item", "date")
    search_fields = ['steamID']


@admin.register(UserStatistic)
class UserStatistic(admin.ModelAdmin):
    list_display = ('user', 'rating', 'games', 'win_games', 'simple_game', 'ability_game', 
                    'damage_deal', 'damage_take', 'creeps', 'bosses', 'golden_creeps', 'min_time')

@admin.register(GameHistory)
class GameHistory(admin.ModelAdmin):
    list_display = ('id','game_time','game_difficulty')
    inlines = [PlayerInlime]


@admin.register(UserProfile)
class UserProfile(admin.ModelAdmin):
    list_display = ('user','difficulty','level','player_exp','skill_points',
                    'str','agi','int','hpr','mpr','movespeed','armor','mresist',
                    'exp','cooldown','damage','attack_speed','evasion','spellamp')