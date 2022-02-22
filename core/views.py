from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.response import Response
from rest_framework import status

from core.services import BotService, TelegramService
from core.keyboards import *
from core.locales import *
from core.utils import send_infographics_photos, send_infographics_videos
from core.serializers import JustSerializer



class BotViewSet(
        mixins.CreateModelMixin,
        GenericViewSet
    ):
    authentication_classes = []
    permission_classes = []
    serializer_class = JustSerializer


    def create(self, request):
        data = request.data

        data_service = TelegramService(data)
        bot_service = BotService(data)

        print(data_service.text)
        if data_service.text == CONFIRM:
            print(1)
            if data_service.member:
                bot_service.delete_message(data_service.message_id)
                bot_service.send_message(WELCOME_TEXT, MAIN_MENU_KEYBOARD)
                data_service.set_step("main-menu")
            else:
                bot_service.delete_message(data_service.message_id)
                CHANNELS_KEYBOARD = get_subscription_keyboard(data_service.unsubscribed)
                bot_service.send_message(JOIN_CHANNELS, CHANNELS_KEYBOARD, inline=True)
                data_service.set_step("ask-subsciption")
        
        elif data_service.text == BACK and data_service.check_step("regions"):
            print(2)
            bot_service.send_message(WELCOME_TEXT, MAIN_MENU_KEYBOARD)
            bot_service.delete_message(data_service.message_id)
        
        elif data_service.text == BACK and data_service.check_step("city"):
            print(3)
            REGIONS_INLINE_KEYBOARD = get_regions_keyboard()
            bot_service.send_message(CHOOSE_REGION, REGIONS_INLINE_KEYBOARD, inline=True)
            data_service.set_step("regions")
            bot_service.delete_message(data_service.message_id)

        elif not data_service.member:
            print(4)
            CHANNELS_KEYBOARD = get_subscription_keyboard(data_service.unsubscribed)
            bot_service.send_message(JOIN_CHANNELS, CHANNELS_KEYBOARD, inline=True)
            data_service.set_step("ask-subsciption")

        elif data_service.text == START or data_service.text == BACK:
            print(5)
            bot_service.send_message(WELCOME_TEXT, MAIN_MENU_KEYBOARD)
            data_service.set_step("main-menu")

        elif data_service.text == MAIN_MENU_ITEM1:
            print(6)
            REGIONS_INLINE_KEYBOARD = get_regions_keyboard()
            bot_service.send_message(CHOOSE_REGION, REGIONS_INLINE_KEYBOARD, inline=True)
            data_service.set_step("regions")
        
        elif data_service.text.startswith("data-region"):
            print(7)
            region_title = data_service.text.split("-")[-1]
            cities = City.objects.filter(region__title=region_title)
            if not cities.exists():
                bot_service.send_message(DATA_NOT_EXISTS)
            else:
                bot_service.delete_message(data_service.message_id)
                CITY_INLINE_KEYBOARD = get_city_keyboard(cities)
                bot_service.send_message(region_title, CITY_INLINE_KEYBOARD, inline=True)
            data_service.set_step("city")
        
        elif data_service.text.startswith("data-city"):
            print(8)
            city_title = data_service.text.split("-")[-1]
            mfys = MFY.objects.filter(city__title=city_title)
            if not mfys.exists():
                bot_service.send_message(DATA_NOT_EXISTS)
            else:
                MFYS_KEYBOARD = get_mfy_keyboard(mfys)
                bot_service.send_message(city_title, MFYS_KEYBOARD)
            data_service.set_step("city")
        
        elif data_service.text == MAIN_MENU_ITEM2:
            print(9)
            bot_service.send_message(CHOOSE_INFO, INFO_KEYBOARD)
            data_service.set_step("info")
        
        elif data_service.text == MAIN_MENU_ITEM3:
            print(10)
            bot_service.send_message(SEND_FEEDBACK)
            data_service.set_step("feedback")
        
        elif data_service.text == HELPER:
            print(11)
            files = HelperInfographic.objects.all()
            send_infographics_videos(bot_service, files)
            send_infographics_photos(bot_service, files)
            data_service.set_step("helper-info")
        
        elif data_service.text == LEADER:
            print(12)
            files = LeaderInfographic.objects.all()
            send_infographics_videos(bot_service, files)
            send_infographics_photos(bot_service, files)
            data_service.set_step("leader-info")

        elif data_service.check_step("feedback") and data_service.text:
            print(13)
            bot_service.send_message(THANKS_FEEDBACK, MAIN_MENU_KEYBOARD)
            feedback = Feedback(
                profile=data_service.profile,
                text=data_service.text
            )
            feedback.save()
            data_service.set_step("main-menu")

        mfy = MFY.objects.filter(title=data_service.text)
        if mfy.exists():
            mfy = mfy.first()
            text = get_mfy_text(mfy)
            bot_service.send_message(text)

        print(14)
        return Response(status=status.HTTP_200_OK)