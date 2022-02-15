from core.locales import *
from core.models import *
from core.utils import clean_phone_number


MAIN_MENU_KEYBOARD = [
    [
        {
            "text": MAIN_MENU_ITEM1
        }
    ],
    [
        {
            "text": MAIN_MENU_ITEM2
        },
        {
            "text": MAIN_MENU_ITEM3
        },
    ]
]


def get_city_keyboard():
    CITY_INLINE_KEYBOARD = [
        []
    ]
    cities = City.objects.all()
    for index, city in enumerate(cities):
        CITY_INLINE_KEYBOARD[-1].append({
            "text": city.title,
            "callback_data": "data-city-{}".format(city.title)
        })
        if index % 2 == 1:
            CITY_INLINE_KEYBOARD.append([])
    return CITY_INLINE_KEYBOARD


def get_mfy_keyboard(mfys):
    MFYS_INLINE_KEYBOARD = [
        [{"text": BACK}],
        []
    ]
    for index, mfy in enumerate(mfys):
        MFYS_INLINE_KEYBOARD[-1].append({
            "text": mfy.title
        })
        if index % 2 == 1:
            MFYS_INLINE_KEYBOARD.append([])
    return MFYS_INLINE_KEYBOARD


def get_mfy_text(mfy):
    text = "👆<b>MFY nomi: {}</b>".format(mfy.title)

    if mfy.inspector and mfy.inspector_phone:
        text += "\n\n👮‍♂️IIB inspektori: {}".format(mfy.inspector)
        text += "\n☎️Telefon nomeri: {}".format(clean_phone_number(mfy.inspector_phone))
    
    if mfy.rais and mfy.rais_phone:
        text += "\n\n🔰MFY raisi: {}".format(mfy.rais)
        text += "\n☎️Telefon nomeri: {}".format(clean_phone_number(mfy.rais_phone))
    
    if mfy.helper and mfy.helper_phone:
        text += "\n\n🔰Xokim yordamchisi: {}".format(mfy.helper)
        text += "\n☎️Telefon nomeri: {}".format(clean_phone_number(mfy.helper_phone))
    
    if mfy.leader and mfy.leader_phone:
        text += "\n\n🔰Yoshlar yetakchisi: {}".format(mfy.leader)
        text += "\n☎️Telefon nomeri: {}".format(clean_phone_number(mfy.leader_phone))
    
    return text


INFO_KEYBOARD = [
    [
        {
            "text": HELPER
        },
        {
            "text": LEADER
        },
    ],
    [{"text": BACK}]
]