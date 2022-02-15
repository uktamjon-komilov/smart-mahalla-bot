from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.response import Response
from rest_framework import status

from core.services import BotService, TelegramService
from core.keyboards import *
from core.locales import *



class BotViewSet(
        mixins.CreateModelMixin,
        GenericViewSet
    ):
    authentication_classes = []
    permission_classes = []


    def create(self, request):
        data = request.data

        data_service = TelegramService(data)
        bot_service = BotService(data)

        if data_service.text == START or data_service.text == BACK:
            data_service.set_step("main-menu")
            bot_service.send_message(WELCOME_TEXT, MAIN_MENU_KEYBOARD)

        elif data_service.text == MAIN_MENU_ITEM1:
            data_service.set_step("cities")
            CITY_INLINE_KEYBOARD = get_city_keyboard()
            bot_service.send_message(CHOOSE_CITY, CITY_INLINE_KEYBOARD, inline=True)
        
        elif data_service.text.startswith("data-city"):
            data_service.set_step("city")
            city_title = data_service.text.split("-")[-1]
            mfys = MFY.objects.filter(city__title=city_title)
            if not mfys.exists():
                bot_service.send_message(DATA_NOT_EXISTS)
            else:
                MFYS_KEYBOARD = get_mfy_keyboard(mfys)
                bot_service.send_message(city_title, MFYS_KEYBOARD)
        
        elif data_service.text == MAIN_MENU_ITEM2:
            bot_service.send_message(CHOOSE_INFO, INFO_KEYBOARD)
            data_service.set_step("info")
        
        elif data_service.text == MAIN_MENU_ITEM3:
            bot_service.send_message(SEND_FEEDBACK)
            data_service.set_step("feedback")
        
        elif data_service.text == HELPER:
            images = HelperInfographic.objects.all()
            image_urls = []
            for image in images:
                image_urls.append(image.full_url)
            bot_service.send_images(image_urls)
            data_service.set_step("helper-info")
        
        elif data_service.text == LEADER:
            images = LeaderInfographic.objects.all()
            image_urls = []
            for image in images:
                image_urls.append(image.full_url)
            bot_service.send_images(image_urls)
            data_service.set_step("leader-info")

        elif data_service.check_step("feedback") and data_service.text:
            bot_service.send_message(THANKS_FEEDBACK)
            feedback = Feedback(
                profile=data_service.profile,
                text=data_service.text
            )
            feedback.save()
        
        print(data_service.check_step("feedback"))

        mfy = MFY.objects.filter(title=data_service.text)
        if mfy.exists():
            mfy = mfy.first()
            text = get_mfy_text(mfy)
            bot_service.send_message(text)

        return Response(status=status.HTTP_200_OK)