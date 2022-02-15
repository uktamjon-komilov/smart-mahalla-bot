from django.conf import settings
import requests as r

from core.models import Profile


class TelegramService:
    def __init__(self, data):
        self.data = data
    
    @property
    def message(self):
        return self.data.get("message", {})
    
    @property
    def callback_query(self):
        return self.data.get("callback_query", {})
    
    @property
    def chat(self):
        return self.message.get("chat", {})
    
    @property
    def chat_id(self):
        chat_id = self.chat.get("id", 0)
        if chat_id == 0:
            chat_id = self.data \
                .get("callback_query", {}) \
                .get("message", {}) \
                .get("chat", {}) \
                .get("id", 0)
        return chat_id
    
    @property
    def username(self):
        return self.chat.get("username", "")
    
    @property
    def first_name(self):
        return self.chat.get("first_name", "")
    
    @property
    def last_name(self):
        return self.chat.get("last_name", "")
    

    @property
    def text(self):
        text = self.message.get("text", "")
        if text == "":
            text = self.callback_query.get("data", "")
        return text

    @property
    def profile(self):
        profile = self.get_or_create_profile()
        return profile

    def get_or_create_profile(self):
        profiles = Profile.objects.filter(tg_id=self.chat_id)
        if profiles.exists():
            profile = profiles.first()
            return profile
        profile = Profile(
            tg_id=self.chat_id,
            tg_username=self.username,
            first_name=self.first_name,
            last_name=self.last_name
        )
        profile.save()
        return profile


class BotService:
    BASE_URL = "https://api.telegram.org/bot{}/".format(settings.BOT_TOKEN)
    
    def __init__(self, data):
        self.chat_id = TelegramService(data).chat_id
    

    def send_message(self, text, menu=None, inline=False):
        ACTION_VERB = "sendMessage"
        URL = "{}{}".format(self.BASE_URL, ACTION_VERB)
        DATA = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        if menu:
            if inline:
                DATA["reply_markup"] = {
                    "inline_keyboard": menu
                }
            else:
                DATA["reply_markup"] = {
                    "resize_keyboard": True,
                    "one_time_keyboard": True,
                    "keyboard": menu
                }
        response = r.post(
            URL,
            json=DATA
        )
        if response.status_code == 200:
            return True
        return False