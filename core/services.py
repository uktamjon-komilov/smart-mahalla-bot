from django.conf import settings
import requests as r
from openpyxl import load_workbook

from core.models import MFY, City, Profile
from core.utils import *


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


class MfyData:
    def __init__(self, data, cities):
        self.city = cities[data[0]]
        self.title = data[1]
        self.inspector = data[2] or ""
        self.inspector_phone = clean_phone_number(data[3] or "")
        self.rais = data[4] or ""
        self.rais_phone = clean_phone_number(data[5] or "")
        self.helper = data[6] or ""
        self.helper_phone = clean_phone_number(data[7] or "")
        self.leader = data[8] or ""
        self.leader_phone = clean_phone_number(data[9] or "")
        self.translit()
    

    def translit(self):
        self.title = convert_to_latin(self.title)
        self.inspector = convert_to_latin(self.inspector)
        self.rais = convert_to_latin(self.rais)
        self.helper = convert_to_latin(self.helper)
        self.leader = convert_to_latin(self.leader)
    

    def json(self):
        return {
            "city": self.city,
            "title": self.title,
            "inspector": self.inspector,
            "inspector_phone": self.inspector_phone,
            "rais": self.rais,
            "rais_phone": self.rais_phone,
            "helper": self.helper,
            "helper_phone": self.helper_phone,
            "leader": self.leader,
            "leader_phone": self.leader_phone
        }


class ExcelService:
    error = None
    items_sheet = None
    cities_sheet = None
    cities = {}

    def __init__(self, file_name):
        from pprint import pprint
        try:
            self.wb = load_workbook(file_name)
            for sheet in self.wb:
                if sheet.title == "Sheet1":
                    self.items_sheet = sheet
                if sheet.title == "Sheet2":
                    self.cities_sheet = sheet
        except:
            self.error = "Cannot be opened"
            return

    
    def execute(self):
        if not self.items_sheet or not self.cities_sheet:
            self.error = "Sheet not found"
            return
        
        for row in self.cities_sheet.values:
            try:
                city = City.objects.get(id=row[1])
                self.cities[city.id] = city
            except:
                pass
        
        for row in self.items_sheet.values:
            if row[0] != "city":
                mfy_data = MfyData(row, self.cities)
                self.save_or_update(mfy_data.json())
    

    def save_or_update(mfy_data):
        mfys = MFY.objects.filter(city=mfy_data["city"], title=mfy_data["title"])
        if mfys.exists():
            mfy_obj = mfys.first()
            for key in mfy_data.keys():
                if hasattr(mfy_obj, key):
                    setattr(mfy_obj, key, mfy_data[key])
            mfy_obj.save()
        else:
            mfy_obj = MFY(**mfy_data)
            mfy_obj.save()