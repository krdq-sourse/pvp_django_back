from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from back.views import *
from back import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('', views.home, name='home'),

    path("api_game_start/", StartGameView.as_view()),
    path("api_buy_item/", BuyItemView.as_view()),
    path("api_add_point/", AddPointView.as_view()),
    path("api_set_default_effect/", SetDefaultEffectView.as_view()),
    path("api_set_default_spray/", SetDefaultSprayView.as_view()),
    path("api_set_default_highfive/", SetDefaultHighfiveView.as_view()),
    path("api_statistic_request/", SetStatisticView.as_view()),
    path("api_buy_account_exp/", BuyAccountExpView.as_view()),
    path("api_save_rating_game/", SaveRatingGame.as_view()),
    path("api_add_hero/", AddHero.as_view()),

    path("api_telegram/", TemegramView.as_view()),

    path("pay_alert/", free_kassa_alert, name='free_kassa_alert'),
    path("pay_success/", free_kassa_success, name='free_kassa_success'),
    path("pay_rejects/", free_kassa_error, name='free_kassa_error'),

    path("callback/", UserProfileView.as_view()),
    path('login/', views.login),
    path('accounts/', include('allauth.urls')),

    path('dev/', DevView.as_view(), name='dev'),
    path('profile/', views.profile, name='profile'),
    path('payments/', views.payments, name='payments'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)