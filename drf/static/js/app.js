$(window).on('beforeunload', function () {
    $(window).scrollTop(0);
});

$(document).ready(function () {
    if (document.location.pathname == '/') {
        let zSpacing = -1000,
            lastPos = zSpacing / 5,
            $frames = $('.frame'),
            zVals = [];

        $(window).scroll(function () {
            console.log("A")
            let top = $(document).scrollTop(),
                delta = lastPos - top;

            lastPos = top;

            $frames.each(function (i) {
                zVals.push((i * zSpacing) + zSpacing);
                zVals[i] += delta * -5.5;
                let transform = `translateZ(${zVals[i]}px)`,
                    opacity = zVals[i] < Math.abs(zSpacing) / 1.8 ? 1 : 0;
                $(this).attr('style', `transform: ${transform}; opacity: ${opacity}`);
            });
        });
        $(window).scrollTop(1);


    }
    if (document.location.pathname == '/profile/') {
        console.log("!2")
        $('#profile').addClass("hidden");
    }
});

///////////////////////////////////////////////////////////////////////

$('.soundbutton').click(function () {
    $(this).toggleClass('paused');
    if ($('.audio').prop('paused')) {
        $('.audio').trigger('play');
    } else {
        $('.audio').trigger('pause');
    }
});

$(window).focus(function () {
    if ($('.soundbutton').hasClass('paused')) {
        $('.audio').trigger('pause');
    } else {
        $('.audio').trigger('play');
    }
});

$(window).blur(function () {
    $('.audio').trigger('pause');
});

///////////////////////////////////////////////////////////////////

$('.language').click(function () {
    console.log("active")
    $('.langs').toggleClass('active');
});

///////////////////////////////////////////////////////////////////

const languageData = {
    "en":{
        "1-frame-title": "13+ unique locations",
        "1-frame-description": "Each location offers a unique experience filled with mystery and adventure",
        "2-frame-title": "20+ unique bosses",
        "2-frame-description": "All bosses and creeps have their own unique characteristics and require a special strategy to defeat",
        "3-frame-title": "Unique heroes",
        "3-frame-description": "Each hero has his own skills and talents, which makes the game more interesting and varied",
        "4-frame-title": "100+ unique items",
        "4-frame-description": "The ability to assemble a unique build set of the hero",
        "5-frame-title": "RPG system",
        "5-frame-description": "Playing you get experience that allows you to develop your account",
        "id-player-description": "You need to play at least 1 game to display stats!",
        "id-player-level":"Level:",
        "id-player-exp":"Exp:",
        "id-player-rating":"Rating:",
        "id-player-games":"Games:",
        "id-player-wins":"Wins:",
        "id-player-simple":"Regular games:",
        "id-player-ability":"Abili mod:",
        "id-player-dd": "Damaged:",
        "id-player-dt": "Taken damage:",
        "id-player-creeps": "Killed creeps:",
        "id-player-boss": "Killed bosses:",
        "id-player-golden": "Killed golden monsters:",
        "id-player-min": "Minutes in game:",
        "pay-description-1": "Your purchase will appear in the new game!",
        "pay-description-2": "You need to login!",
    },
    "ru":{
        "1-frame-title": "13+ уникальных локаций",
        "1-frame-description": "Каждая локация предлагает уникальный сюжет, наполненный тайнами и приключениями",
        "2-frame-title": "20+ уникальных боссов",
        "2-frame-description": "Все боссы и крипы имеют свои уникальные способности и требуют особой стратегии для победы",
        "3-frame-title": "Уникальные герои",
        "3-frame-description": "У каждого героя свои навыки и таланты, что делает игру более интересной и разнообразной",
        "4-frame-title": "100+ уникальных предметов",
        "4-frame-description": "Возможность собрать уникальный билд для любого героя",
        "5-frame-title": "Система РПГ",
        "5-frame-description": "Играя вы получаете опыт, который позволяет вам развивать свой аккаунт",
        "id-player-description":"Для отображения статистики необходимо сыграть хотя бы в 1 игру!",
        "id-player-level":"Уровень:",
        "id-player-exp":"Опыт:",
        "id-player-rating":"Рейтинг:",
        "id-player-games":"Игр:",
        "id-player-wins":"Побед:",
        "id-player-simple":"Обычных игр:",
        "id-player-ability":"Абили мод:",
        "id-player-dd":"Нанес урон:",
        "id-player-dt":"Получил урон:",
        "id-player-creeps":"Убил крипов:",
        "id-player-boss":"Убил боссов:",
        "id-player-golden":"Убил золотых монстров:",
        "id-player-min":"Минут в игре:",
        "pay-description-1": "Ваша покупка появится в новой игре!",
        "pay-description-2": "Вам необходимо авторизоваться!",
    },
    "ua":{
        "1-frame-title": "13+ унікальних локацій",
        "1-frame-description": "Кожна локація пропонує унікальний досвід, наповнений таємницею та пригодами",
        "2-frame-title": "20+ унікальних босів",
        "2-frame-description": "Усі боси і кріпи є унікальними та неповторними для перемоги над якими потрібна спеціальна стратегія",
        "3-frame-title": "Унікальні герої",
        "3-frame-description": "У кожного героя свої навики і таланти, чим роблять гру більш цікавою і різносторонньою",
        "4-frame-title": "100+ унікальних артефактів",
        "4-frame-description": "Можливість зібрати унікальну зборку для кожного героя",
        "5-frame-title": "Система РПГ",
        "5-frame-description": "Граючи ви получаєте досвід, який дозволяє вам розвивати свій акаунт",
        "id-player-description": "Для відображення статистики потрібно зіграти хоча б 1 гру!",
        "id-player-level":"Рівень:",
        "id-player-exp":"Опит:",
        "id-player-rating":"Рейтинг:",
        "id-player-games":"Ігор:",
        "id-player-wins":"Перемог:",
        "id-player-simple":"Класичних ігор:",
        "id-player-ability":"Абіліті мод:",
        "id-player-dd": "Наніс урона:",
        "id-player-dt": "Получив урон:",
        "id-player-creeps": "Вбив крипів:",
        "id-player-boss": "Вбив босів:",
        "id-player-golden": "Вбив золотих монстрів:",
        "id-player-min": "Хвилин в грі:",
        "pay-description-1": "Ваша покупка з'явиться у новій грі!",
        "pay-description-2": "Вам необхідно авторизуватись!",
    },
    "ch":{
        "1-frame-title": "13+ 个独特的位置",
        "1-frame-description": "每个地点都提供充满神秘和冒险的独特体验",
        "2-frame-title": "20 多个独特的老板",
        "2-frame-description": "所有 Boss 和 creep 都有自己独特的特点，需要特殊的策略才能打败",
        "3-frame-title": "独特的英雄",
        "3-frame-description": "每个英雄都有自己的技能和天赋，让游戏更加有趣和多样",
        "4-frame-title": "100+ 独特物品",
        "4-frame-description": "组装英雄独特构建集的能力",
        "5-frame-title": "RPG系统",
        "5-frame-description": "玩你获得的经验可以让你发展你的账户",
        "id-player-description": "你需要至少玩 1 场比赛才能显示数据！",
        "id-player-level":"等级:",
        "id-player-exp":"经验:",
        "id-player-rating":"评分：",
        "id-player-games":"游戏:",
        "id-player-wins":"获胜次数：",
        "id-player-simple":"常规游戏：",
        "id-player-ability":"技能模组:",
        "id-player-dd": "损坏：",
        "id-player-dt": "受到伤害：",
        "id-player-creeps": "杀死的小兵：",
        "id-player-boss": "杀死的老板：",
        "id-player-golden": "击杀金色怪物：",
        "id-player-min": "游戏时间：",
        "pay-description-1": "您的购买将出现在新游戏中!",
        "pay-description-2": "您需要登录！",
    }
}


$(document).ready(function () {
    let language = localStorage.getItem("language") || "en";
    $(".fab-buttons__link").click(function () {
        const selectedLanguage = $(this).attr("id");
        console.log(selectedLanguage, "!")
        localStorage.setItem("language", selectedLanguage);
        language = selectedLanguage; 
        $("#1-frame-title").text(languageData[language]["1-frame-title"]);
        $("#1-frame-description").text(languageData[language]["1-frame-description"]);
        $("#2-frame-title").text(languageData[language]["2-frame-title"]);
        $("#2-frame-description").text(languageData[language]["2-frame-description"]);
        $("#3-frame-title").text(languageData[language]["3-frame-title"]);
        $("#3-frame-description").text(languageData[language]["3-frame-description"]);
        $("#4-frame-title").text(languageData[language]["4-frame-title"]);
        $("#4-frame-description").text(languageData[language]["4-frame-description"]);
        $("#5-frame-title").text(languageData[language]["5-frame-title"]);
        $("#5-frame-description").text(languageData[language]["5-frame-description"]);
        $("#id-player-description").text(languageData[language]["id-player-description"]);
        $("#id-player-level").text(languageData[language]["id-player-level"]);
        $("#id-player-exp").text(languageData[language]["id-player-exp"]);
        $("#id-player-rating").text(languageData[language]["id-player-rating"]);
        $("#id-player-games").text(languageData[language]["id-player-games"]);
        $("#id-player-wins").text(languageData[language]["id-player-wins"]);
        $("#id-player-simple").text(languageData[language]["id-player-simple"]);
        $("#id-player-ability").text(languageData[language]["id-player-ability"]);
        $("#id-player-dd").text(languageData[language]["id-player-dd"]);
        $("#id-player-dt").text(languageData[language]["id-player-dd"]);
        $("#id-player-creeps").text(languageData[language]["id-player-creeps"]);
        $("#id-player-boss").text(languageData[language]["id-player-boss"]);
        $("#id-player-golden").text(languageData[language]["id-player-golden"]);
        $("#id-player-min").text(languageData[language]["id-player-min"]);
        $("#pay-description-1").text(languageData[language]["pay-description-1"]);
        $("#pay-description-2").text(languageData[language]["pay-description-2"]);
    });
});

/////////////////////////////////////////////////////////////////////////////////

$(document).ready(function() {
    function submitForm(element) {
      var form = $(element).find(".payment-form");
      form.submit();
    }
  
    $('.payment-cart').click(function() {
      submitForm(this);
    });
  });