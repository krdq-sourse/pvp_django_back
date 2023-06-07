from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from django.views.generic import View
from .models import *
from .forms import UserOpenProfile, UserDonate
from .serializers import *
from allauth.socialaccount.models import SocialAccount
from django.db.models import F
from itertools import groupby
import logging
import json
from datetime import datetime
from django.http import HttpResponse
import hashlib


logger = logging.getLogger(__name__)
KEY_VALID = ''
RDA_KEY_VALID = ''
KEY_TELEGRAM = ''
SHOP_ID = ''
SHOP_WORD = ''
MY_ID = 7

class Test(APIView):
    def get(self, request):
        Users = User.objects.filter(steamID=MY_ID)
        serializer = UserSerializer(Users, many=True)
        return Response(serializer.data)
    

# /////////////////////////////////////////////////////////

def payments(request):
    try:
        id = request.user.id
        if request.user.first_name:
            social_account = SocialAccount.objects.get(uid=request.user.first_name)
            merchant_id = SHOP_ID
            secret_word = SHOP_WORD
            order_id = social_account.uid
            currency = 'RUB'

            prices = [
                {'gems': '50', 'amount': '350'},
                {'gems': '100', 'amount': '700'},
                {'gems': '200', 'amount': '1400'},
                {'gems': '500', 'amount': '3500'},
                {'gems': '1000', 'amount': '7000'},
            ]

            items = []
            for price in prices:
                sign = hashlib.md5(f'{merchant_id}:{price["amount"]}:{secret_word}:{currency}:{order_id}'.encode('utf-8')).hexdigest()
                item = {
                    'm': merchant_id,
                    'oa': price['amount'],
                    'o': order_id,
                    's': sign,
                    'currency': currency,
                    'us_gem': price['gems']
                }
                items.append(item)

            context = {'items': items}
            return render(request, 'payments.html', context=context)
    except:
        return render(request, 'payments.html')

def free_kassa_alert(request):
    gems = request.GET.get("us_gem")
    sid = request.GET.get("MERCHANT_ORDER_ID")
    logging.basicConfig(filename='server.log', level=logging.INFO)
    logging.info(f'Received key telegram: {gems} - {sid}')
    if sid and gems:
        ShopHistory.objects.create(steamID=sid, coins=gems, item="FreeKassa", date=datetime.now()) 
        user = User.objects.filter(steamID=sid).first()    
        user.coins = user.coins + int(gems)
        user.total_coins = user.total_coins + int(gems)
        user.save()
        return HttpResponse()
    return Response({"Error": "Error"})

def free_kassa_success(request):
    context = {'status': 'Успешно!'}
    return render(request, 'payments_result.html', context=context)
    
def free_kassa_error(request):
    context = {'status': 'Неудача!'}
    return render(request, 'payments_result.html', context=context)  
    
# /////////////////////////////////////////////////////////    

def index(request):
    return render(request, 'index.html')

def home(request):
    id = request.user.id
    social_account = SocialAccount.objects.get(id=id)
    user_data = UserProfile.objects.filter(user__steamID=social_account.uid)
    return render(request, 'index.html', context={'sid':user_data})

def profile(request):
    id = request.user.id
    if request.user.first_name:
        social_account = SocialAccount.objects.get(uid=request.user.first_name)
        try:
            user_profile = UserProfile.objects.get(user__steamID=social_account.uid)
            user_user = User.objects.get(steamID=social_account.uid)
            user_statistic = UserStatistic.objects.get(user__steamID=social_account.uid)

            try:
                winrate = round(user_statistic.win_games / user_statistic.games * 100)
            except:
                winrate = 0

            if user_statistic.simple_game > user_statistic.ability_game:
                game_rate = 100 - (round(user_statistic.ability_game / user_statistic.simple_game * 100))
            elif user_statistic.simple_game < user_statistic.ability_game:
                game_rate = 100 - (round(user_statistic.simple_game / user_statistic.ability_game * 100))
            else:    
                game_rate = 50

            if user_statistic.damage_deal == 0:
                user_statistic.damage_deal = 1
            if user_statistic.damage_take == 0:
                user_statistic.damage_deal = 1

            if user_statistic.damage_deal > user_statistic.damage_take:
                damage_rate = 100 - (round(user_statistic.damage_take / user_statistic.damage_deal * 100))
            elif user_statistic.damage_deal < user_statistic.damage_take:
                damage_rate = 100 - (round(user_statistic.damage_deal / user_statistic.damage_take * 100))
            else:    
                damage_rate = 50    

            context = {
            'profile': user_profile,
            'user_user': user_user,
            'statistic': user_statistic,
            'extra':social_account.extra_data,
            'winrate':winrate,
            'game_rate':game_rate,
            'damage_rate':damage_rate
            }
            return render(request, 'profile.html', context=context)
        except:
            return render(request, 'profile.html', context={})
        

class DevView(View):
    def get(self, request):
        form = UserOpenProfile(request.POST or None)
        history = ShopHistory.objects.order_by('-date')[:300]
        id = request.GET.get('id')
        if id:
            history = ShopHistory.objects.filter(steamID=id).order_by('-date')[:300]
            info = User.objects.filter(steamID=id)
            social_account = SocialAccount.objects.filter(uid=id).first()
            context = {'form': form,
                       'history': history,
                       'id': id,
                       "info": info,
                        }
            if social_account:
                context['extra'] = social_account.extra_data
            form = UserDonate(initial={'id': id})
            return render(request, 'dev.html', context=context)
        return render(request, 'dev.html', context={"history":history, "form":form})

    
    def post(self, request):
        id_form = UserOpenProfile(request.POST)
        if id_form.is_valid():
            id = id_form.cleaned_data['steamID']
            history = ShopHistory.objects.filter(steamID=id).order_by('-date')[:300]
            info = User.objects.filter(steamID=id).first()
            if not info:
                return render(request, 'dev.html', {'history': history})
            social_account = SocialAccount.objects.filter(uid=id).first()
            form = UserDonate(initial={'id': id})
            context = {'form': form,
                       'history': history,
                       'id': id,
                       "info": info,
            }
            if social_account:
                context['extra'] = social_account.extra_data
            return render(request, 'dev.html', context=context)
        number_form = UserDonate(request.POST)
        if number_form.is_valid():
            coins = number_form.cleaned_data['coins']
            id = request.POST.get('id')
            user = User.objects.filter(steamID=id).first()   
            if user: 
                ShopHistory.objects.create(steamID=id, coins=coins, item="Add Donate", date=datetime.now()) 
                user.coins = user.coins + coins
                user.total_coins = user.total_coins + coins
                user.save()

                history = ShopHistory.objects.filter(steamID=id).order_by('-date')[:300]
                info = User.objects.filter(steamID=id).first()
                if not info:
                    return render(request, 'dev.html', {'history': history})
                social_account = SocialAccount.objects.filter(uid=id).first()
                form = UserDonate(initial={'id': id})
                context = {'form': form,
                        'history': history,
                        'id': id,
                        "info": info,
                }
                if social_account:
                    context['extra'] = social_account.extra_data
                return render(request, 'dev.html', context=context)
        return render(request, 'dev.html', {'form': id_form})


# ///////////////////////////////////////////////// USER PROFILE //////////////////////////////


class UserProfileView(APIView):
    def get(self, request):
        sid = get_uid(request.GET)
        user = User.objects.filter(steamID=sid).first()
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response({"error": "User not found"}, status=404)


# ///////////////////////////////////////////////// START GAME //////////////////////////////


class StartGameView(APIView):
    renderer_classes = (JSONRenderer, )
    
    def get(self, request):
        Users = User.objects.all()
        serializer = UserSerializer(Users, many=True)
        return Response(serializer.data)

    def post(self, request):
        key = request.GET.get('key')
        logging.basicConfig(filename='server.log', level=logging.INFO)
        logging.info('Received key start game: %s', key)
        if key != KEY_VALID:
            return Response({"status": "False"})          
        results = []
        try:
            arr = json.loads(request.POST.get('arr'))
        except (json.JSONDecodeError, TypeError):
            return Response({"error": "Invalid JSON in arr"})

        players = arr['players']
        ability_game = arr['mode_map_ability']
        simple_game = arr['mode_map_simple']

        for k, v in players.items():
            sid = v['sid']
            logging.info('Received key start game: %s', sid, "players")
            user, created = User.objects.get_or_create(steamID=sid)
            serializer = UserSerializer(user)
            statistic = UserStatistic.objects.get(user=user)
            statistic.ability_game = statistic.ability_game + ability_game
            statistic.simple_game = statistic.simple_game + simple_game
            statistic.games += 1
            statistic.save()
            results.append(serializer.data)
        logging.info('Received key start game: %s', results)
        return Response(results)


# /////////////////////////////////////////// BUY ITEM ///////////////////////////////////////////////


class BuyItemView(APIView):
    renderer_classes = (JSONRenderer, )

    def post(self, request):
        key = request.GET.get('key')
        logging.basicConfig(filename='server.log', level=logging.INFO)
        logger.info('Received key buy item: %s', key)
        if key != KEY_VALID:
            return Response({"status": "False"})
        try:
            arr = json.loads(request.POST.get('arr'))
        except (json.JSONDecodeError, TypeError):
            return Response({"error": "Invalid JSON in arr"})
        sid, name, price, currency = arr.get('sid'), arr.get('name'), arr.get('price'), arr.get('currency')
        user = User.objects.filter(steamID=sid).first()
        if currency == 'don':
            if (user.coins - price) >= 0:
                user.coins -= price
                ShopHistory.objects.create(steamID=sid, coins=-price, item=name, date=datetime.now())
            else:  
                user.ban_status = True
                return Response({"!!!!":"???"})  
        else:
            if (user.rp - price) >= 0:
                user.rp -= price
            else:
                user.ban_status = True
                return Response({"!!!!":"???"})      
        user.save()
        product = Product.objects.get(name=name)
        user_item, _ = UserItems.objects.get_or_create(user=user, product=product, defaults={'count': 0})
        user_item.count += 1
        user_item.save()
        return Response({"status": "OK"})


# /////////////////////////////////////////// ADD SKILL POINT ///////////////////////////////////////////////


class AddPointView(APIView):
    renderer_classes = (JSONRenderer, )

    def post(self, request):
        key = request.GET.get('key')
        logging.basicConfig(filename='server.log', level=logging.INFO)
        if key != KEY_VALID:
            return Response({"status": "False"})
        try:
            arr = json.loads(request.POST.get('arr'))
        except (json.JSONDecodeError, TypeError):
            return Response({"error": "Invalid JSON in arr"})
        sid, name = arr.get('sid'), arr.get('name')
        logging.info(f'Received key points: {key} - {sid}')
        user_profile = UserProfile.objects.filter(user__steamID=sid).first()
        if user_profile:
            try:
                setattr(user_profile, name, F(name) + 1)
                user_profile.skill_points -= 1
                user_profile.save()
                return Response({"status": "OK"})
            except AttributeError:
                return Response({"error": "Invalid field name"})
        return Response({"status": "fail"})
    

# /////////////////////////////////////////// SET DEFAULT EFFECT ///////////////////////////////////////////////


class SetDefaultEffectView(APIView):
    renderer_classes = (JSONRenderer, )

    def post(self, request):
        key = request.GET.get('key')
        logging.basicConfig(filename='server.log', level=logging.INFO)
        logger.info('Received key set default effect: %s', key)
        if key != KEY_VALID:
            return Response({"status": "False"})
        try:
            arr = json.loads(request.POST.get('arr'))
        except (json.JSONDecodeError, TypeError):
            return Response({"error": "Invalid JSON in arr"})
        sid, name, status = arr.get('sid'), arr.get('name'), arr.get('status')
        user_items = UserItems.objects.filter(user__steamID=sid, product__category=3)
        if user_items:
            user_items.update(active=False)
            user_item = UserItems.objects.filter(user__steamID=sid, product__name=name).first()
            if user_item:
                if status:
                    user_item.active = True
                    user_item.save()
                    return Response({"status": "set"})  
                user_item.active = False  
                user_item.save()
                return Response({"status": "unset"})       
        return Response({"status": "fail"})      

# /////////////////////////////////////////// SET DEFAULT SPRAY ///////////////////////////////////////////////


class SetDefaultSprayView(APIView):
    renderer_classes = (JSONRenderer, )

    def post(self, request):
        key = request.GET.get('key')
        logging.basicConfig(filename='server.log', level=logging.INFO)
        logger.info('Received key set default effect: %s', key)
        if key != KEY_VALID:
            return Response({"status": "False"})
        try:
            arr = json.loads(request.POST.get('arr'))
        except (json.JSONDecodeError, TypeError):
            return Response({"error": "Invalid JSON in arr"})
        sid, name, status = arr.get('sid'), arr.get('name'), arr.get('status')
        user_items = UserItems.objects.filter(user__steamID=sid, product__category=5)
        if user_items:
            user_items.update(active=False)
            user_item = UserItems.objects.filter(user__steamID=sid, product__name=name).first()
            if user_item:
                if status:
                    user_item.active = True
                    user_item.save()
                    return Response({"status": "set"})  
                user_item.active = False  
                user_item.save()
                return Response({"status": "unset"})       
        return Response({"status": "fail"})             

# /////////////////////////////////////////// SET DEFAULT HIGHFIVE ///////////////////////////////////////////////


class SetDefaultHighfiveView(APIView):
    renderer_classes = (JSONRenderer, )

    def post(self, request):
        key = request.GET.get('key')
        logging.basicConfig(filename='server.log', level=logging.INFO)
        logger.info('Received key set default effect: %s', key)
        if key != KEY_VALID:
            return Response({"status": "False"})
        try:
            arr = json.loads(request.POST.get('arr'))
        except (json.JSONDecodeError, TypeError):
            return Response({"error": "Invalid JSON in arr"})
        sid, name, status = arr.get('sid'), arr.get('name'), arr.get('status')
        user_items = UserItems.objects.filter(user__steamID=sid, product__category=6)
        if user_items:
            user_items.update(active=False)
            user_item = UserItems.objects.filter(user__steamID=sid, product__name=name).first()
            if user_item:
                if status:
                    user_item.active = True
                    user_item.save()
                    return Response({"status": "set"})  
                user_item.active = False  
                user_item.save()
                return Response({"status": "unset"})       
        return Response({"status": "fail"})        
    

# /////////////////////////////////////////// BUY ACCOUNT EXP ///////////////////////////////////////////////


class BuyAccountExpView(APIView):
    renderer_classes = (JSONRenderer, )

    def post(self, request):
        key = request.GET.get('key')
        logging.basicConfig(filename='server.log', level=logging.INFO)
        logger.info('Received key add points: %s', key)
        if key != KEY_VALID:
            return Response({"status": "False"})
        try:
            arr = json.loads(request.POST.get('arr'))
        except (json.JSONDecodeError, TypeError):
            return Response({"error": "Invalid JSON in arr"})
        sid, add_exp, player_level, point = arr.get('sid'), arr.get('add_exp'), arr.get('player_level'), arr.get('point')
        user = User.objects.get(steamID=sid)   
        user_profile = UserProfile.objects.filter(user__steamID=sid).first()
        product = Product.objects.get(name='item_account_exp')
        user_item = UserItems.objects.get(user=user, product=product)
        user_item.count -= 1
        user_item.save()
        if user:
            user_profile.player_exp = add_exp
            user_profile.level = player_level
            user_profile.skill_points = point
            user_profile.save()
            return Response({"status": "OK"})
        return Response({"status": "fail"})
            
# /////////////////////////////////////////// ADD STATISTIC ///////////////////////////////////////////////


class SetStatisticView(APIView):
    renderer_classes = (JSONRenderer, )

    def post(self, request):
        key = request.GET.get('key')
        logging.basicConfig(filename='server.log', level=logging.INFO)
        logger.info('Received key set statistic: %s', key)
        if key != KEY_VALID:
            return Response({"status": "False"})
        try:
            arr = json.loads(request.POST.get('arr'))
        except (json.JSONDecodeError, TypeError):
            return Response({"error": "Invalid JSON in arr"})
        sid = arr.get('sid')
        rp = arr.get('rp')  #User
        total_rp = arr.get('total_rp')  #User

        player_exp = arr.get('expa') #UserProfile
        level = arr.get('player_level') #UserProfile
        skill_points = arr.get('point') #UserProfile

        rating = arr.get('rating') #UserStatistic
        damage_deal = arr.get('damage_deal') #UserStatistic +
        damage_take = arr.get('damage_take') #UserStatistic +
        creeps = arr.get('creeps_kill') #UserStatistic +
        bosses = arr.get('boss') #UserStatistic +
        golden_creeps = arr.get('golden') #UserStatistic +
        min_time = arr.get('time_min') #UserStatistic +
        win_games = arr.get('win') #UserStatistic +
        difficulty = arr.get('difficulty') #UserStatistic +

        user = User.objects.get(steamID=sid)   
        user_profile = UserProfile.objects.filter(user__steamID=sid).first()
        user_statistic = UserStatistic.objects.filter(user__steamID=sid).first()
        if user:
            user.rp = rp
            user.total_rp = user.total_rp + total_rp
            user.save()

            user_profile.player_exp = player_exp
            user_profile.level = level
            user_profile.skill_points = skill_points
            user_profile.difficulty = difficulty
            user_profile.save()

            user_statistic.rating = rating
            user_statistic.damage_deal = user_statistic.damage_deal + damage_deal
            user_statistic.damage_take = user_statistic.damage_take + damage_take
            user_statistic.creeps = user_statistic.creeps + creeps
            user_statistic.bosses = user_statistic.bosses + bosses
            user_statistic.golden_creeps = user_statistic.golden_creeps + golden_creeps
            user_statistic.min_time =  user_statistic.min_time + min_time
            user_statistic.win_games = user_statistic.win_games + win_games
            user_statistic.save()
            return Response({"status": "OK"})     
        return Response({"status": "fail"})     


# /////////////////////////////////////////// GET and POST GAME RATING ////////////////////////////////////////////


class SaveRatingGame(APIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request):
        games = GameHistory.objects.order_by('game_difficulty', 'game_time')
        grouped_games = groupby(games, key=lambda game: game.game_difficulty)
        result = []
        for difficulty, games in grouped_games:
            game_data = {'game_difficulty': difficulty, 'game_time': []}
            for game in games:
                players = Player.objects.filter(game=game).values('player_id', 'player_level', 'player_rating', 'hero', 'item1', 'item2', 'item3', 'item4', 'item5', 'item6')
                players_list = []
                for player in players:
                    items = [player[f'item{i}'] for i in range(1, 7) if player[f'item{i}'] is not None]
                    players_list.append({'player_id': player['player_id'], 'player_level': player['player_level'],
                                        'player_rating': player['player_rating'], 'hero': player['hero'], 'items': items})
                if len(game_data['game_time']) >= 10:
                    break
                game_data['game_time'].append({'game_time': game.game_time, 'players': players_list})
            result.append(game_data)
        return Response(result)

    def post(self, request):
        key = request.GET.get('key')
        logging.basicConfig(filename='server.log', level=logging.INFO)
        logger.info('Received key save rating game: %s', key)
        if key != KEY_VALID:
            return Response({"status": "False"})
        try:
            arr = json.loads(request.POST.get('arr'))
        except (json.JSONDecodeError, TypeError):
            return Response({"error": "Invalid JSON in arr"})

        game_time = arr.get('game_time')
        game_difficulty = arr.get('game_difficulty')
        players = arr.get('players')
        game = GameHistory.objects.create(game_time=game_time, game_difficulty=game_difficulty)
        for player_data in players.values():
            items = player_data['items']
            player_items = [items[i] if i < len(items) else None for i in range(6)]
            player = Player.objects.create(game=game, player_id=int(player_data['sid']), hero=player_data['hero'], 
                                                    player_level=int(player_data['player_level']), 
                                                    player_rating=int(player_data['player_rating']), 
                                                    item1=player_items[0], item2=player_items[1],
                                                    item3=player_items[2], item4=player_items[3],
                                                    item5=player_items[4], item6=player_items[5])
        return Response({"status": "OK Save rating"})


# /////////////////////////////////////////// ADD ATATISTIC ///////////////////////////////////////////////        


class TemegramView(APIView):
    def post(self, request):
        key = request.GET.get('key')
        if key != KEY_TELEGRAM:
            return Response({"status": "telegram invalid"})
        sid = request.GET.get('sid') 
        logging.info(f'Received key telegram: {key} - {sid}')
        ShopHistory.objects.create(steamID=sid, coins=10, item="Telegram", date=datetime.now())
        user = User.objects.get(steamID=sid)       
        user.coins = user.coins + 10
        user.total_coins = user.total_coins + 10
        user.save()
        return Response({"status": "telegram valid"})
        

def login(request):
    return auth('/callback/', use_ssl=False)

# //////////////////////////////////////////////// ADD HERO ///////////////////////////

class AddHero(APIView):
    def post(self, request):
        key = request.GET.get('key')
        logging.basicConfig(filename='server.log', level=logging.INFO)
        if key != RDA_KEY_VALID:
            return Response({"status": "False"})          
        try:
            arr = json.loads(request.POST.get('arr'))
        except (json.JSONDecodeError, TypeError):
            return Response({"error": "Invalid JSON in arr"})
        players = arr['players']
        for k, v in players.items():
            sid = v['sid']
            try:
                user = User.objects.filter(steamID=sid).first()
                user.add_hero = True
                user.save()
            except:
                logging.info(f'Addhero error, no id: {sid}')
        return Response({"status": "hero add valid"})
    
# ///////////////////////////////////////////////////// OTHER //////////////////////

# import os

# def get_unit_info(request):
#     for i in range(2, 13):
#         Product.objects.create(
#             name=f"highfive_{i}",
#             price=10,
#             rp_price=100,
#             category=ProductCategory.objects.get(name="Пятюня")
#         )
#     return render(request, 'index.html')  

