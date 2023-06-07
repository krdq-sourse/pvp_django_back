from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class ProductCategory(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name='Категория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категория товаров'


class Product(models.Model):
    name = models.CharField(max_length=64, default=None, verbose_name="Товар")
    price = models.IntegerField(default=0, verbose_name="Цена")
    upgrade_price = models.IntegerField(default=0, verbose_name="Цена улучшения")
    rp_price = models.IntegerField(default=0, verbose_name="Цена в РП")
    rp_upgrade_price = models.IntegerField(default=0, verbose_name="Цена улучшения в РП")
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name="Категория")
    can_upgrade = models.BooleanField(default=False, verbose_name='Улучшаемый')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class User(models.Model):
    steamID = models.BigIntegerField(verbose_name='Пользователь')
    coins = models.IntegerField(verbose_name='Монет', default=0)
    rp = models.IntegerField(verbose_name='РП', default=0)
    total_rp = models.IntegerField(verbose_name='Тотал РП', default=0)
    total_coins = models.IntegerField(verbose_name='Суммарный донат', default=0)
    ban_status = models.BooleanField(default=False, verbose_name='Бан')
    add_hero = models.BooleanField(default=False, verbose_name='Анаким')

    def __str__(self):
        return str(self.steamID)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name='profile', on_delete=models.CASCADE, verbose_name='Профиль')
    difficulty = models.IntegerField(default=1, verbose_name="Сложность")
    level = models.IntegerField(default=1, verbose_name="Уровень")
    player_exp = models.IntegerField(default=0, verbose_name="Опыт")
    skill_points = models.IntegerField(default=0, verbose_name="Поинтов")
    str = models.IntegerField(default=0, verbose_name="Сила")
    agi = models.IntegerField(default=0, verbose_name="Ловкость")
    int = models.IntegerField(default=0, verbose_name="Интеллект")
    hpr = models.IntegerField(default=0, verbose_name="Реген ХП")
    mpr = models.IntegerField(default=0, verbose_name="Реген МП")
    movespeed = models.IntegerField(default=0, verbose_name="Скорость передвижения")
    armor = models.IntegerField(default=0, verbose_name="Броня")
    mresist = models.IntegerField(default=0, verbose_name="Резист магии")
    exp = models.IntegerField(default=0, verbose_name="Опыт за крипа")
    cooldown = models.IntegerField(default=0, verbose_name="Перезарядка")
    damage = models.IntegerField(default=0, verbose_name="Урон")
    attack_speed = models.IntegerField(default=0, verbose_name="Скорость атаки")
    evasion = models.IntegerField(default=0, verbose_name="Уклонение")
    spellamp = models.IntegerField(default=0, verbose_name="Усиление заклинаний")

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профиль'       


class UserStatistic(models.Model):
    user = models.ForeignKey(User, related_name='statistic', on_delete=models.CASCADE, verbose_name='Статистика')
    rating = models.IntegerField(default=0, verbose_name="Рейтинг")
    games = models.IntegerField(default=0, verbose_name="Игр") 
    win_games = models.IntegerField(default=0, verbose_name="Побед") 
    simple_game = models.IntegerField(default=0, verbose_name="Обычный мод")
    ability_game = models.IntegerField(default=0, verbose_name="Абилити мод")
    damage_deal = models.BigIntegerField(default=0, verbose_name='Нанес урон')
    damage_take = models.BigIntegerField(default=0, verbose_name='Получил урон')
    creeps = models.BigIntegerField(default=0, verbose_name='Крипов')
    bosses = models.BigIntegerField(default=0, verbose_name='Боссов')
    golden_creeps = models.BigIntegerField(default=0, verbose_name='Золотых крипов')
    min_time = models.BigIntegerField(default=0, verbose_name='Минут в игре')


    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'             


class UserItems(models.Model):
    user = models.ForeignKey(User, related_name='product', on_delete=models.CASCADE,  default=None, verbose_name='Items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None, verbose_name='Предмет')
    count = models.IntegerField(default=1, verbose_name='Уровень/Кол-во')
    active = models.BooleanField(default=False, verbose_name='Активность')

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'    


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance
        )
        UserStatistic.objects.create(
            user=instance
        )


class ShopHistory(models.Model):
    steamID = models.BigIntegerField(verbose_name='Пользователь')
    coins = models.IntegerField(verbose_name='Монет', default=0)
    item = models.CharField(max_length=64, default=None, verbose_name="Предмет")
    date = models.DateTimeField(default=timezone.now(), blank=True)

    class Meta:
        verbose_name = 'История покупок'
        verbose_name_plural = 'История покупок'   


class GameHistory(models.Model):
    game_time = models.IntegerField(verbose_name='Время игры')
    game_difficulty = models.IntegerField(verbose_name='Номер сложности')

    def __str__(self):
        return str(self.game_time)
    
    class Meta:
        verbose_name = 'История игр'
        verbose_name_plural = 'История игр'      


class Player(models.Model):
    game = models.ForeignKey(GameHistory, on_delete=models.CASCADE)
    player_id = models.CharField(max_length=50, verbose_name='Пользователь')
    player_level = models.IntegerField(verbose_name='Уровень аккаунта игрока')
    player_rating = models.IntegerField(verbose_name='Рейтинг аккаунта игрока')
    hero = models.CharField(max_length=50, null=True, verbose_name="Герой")
    item1 = models.CharField(max_length=50, null=True, verbose_name="Предмет 1")
    item2 = models.CharField(max_length=50, null=True, verbose_name="Предмет 2")
    item3 = models.CharField(max_length=50, null=True, verbose_name="Предмет 3")
    item4 = models.CharField(max_length=50, null=True, verbose_name="Предмет 4")
    item5 = models.CharField(max_length=50, null=True, verbose_name="Предмет 5")
    item6 = models.CharField(max_length=50, null=True, verbose_name="Предмет 6")

    def __str__(self):
        return str(self.player_id)