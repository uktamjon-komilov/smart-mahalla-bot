from time import sleep
import cyrtranslit
from selenium import webdriver

CHROME_DRIVER = "C:\\Program Files (x86)\\chromedriver.exe"


class Trans:
    BASE_URL = "https://uzlatin.com"
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.headless = True
        self.driver = webdriver.Chrome(
            CHROME_DRIVER,
            chrome_options=chrome_options
        )
        self.driver.get(self.BASE_URL)
    
    def translit(self, text):
        if text.strip() == "":
            text = "-"
        from_text = self.driver.find_element_by_id("from-text")
        from_text.clear()
        from_text.send_keys(text)
        button = self.driver.find_element_by_css_selector(".btn.btn-primary.btn-lg.form-send-btn")
        button.click()
        sleep(0.3)
        result_input = self.driver.find_element_by_id("to-text")
        result = result_input.get_attribute("value")
        while result == "":
            result = result_input.get_attribute("value")
        print(result)
        from_text.clear()
        return result
    

def convert_to_latin(text):
    # text = "Шакарқишлоқ МФЙ"
    text = text.replace("Ё", "Yo").replace("ё", "yo")
    text = text.replace("Ў", "O'").replace("ў", "o'")
    text = text.replace("Қ", "Q").replace("қ", "q")
    text = text.replace("МФЙ", "").strip()
    result = cyrtranslit.to_latin(text, "ru")
    # result = slugify(text, separator=" ").replace(" ", "")
    result = "{} MFY".format(result.title())
    return result


def clean_phone_number(phone):
    result = str(phone) \
            .replace("(", "") \
            .replace(")", "") \
            .replace("/", "") \
            .replace("\\", "") \
            .replace("-", "") \
            .replace("_", "") \
            .replace(".", "") \
            .replace("+", "") \
            .replace(" ", "")
    
    sign = "+"
    if len(result) <= 9:
        sign = "+998-"
    return sign + result


def is_photo(file_path):
    TYPES = ["jpg", "jpeg"]
    parts = file_path.split(".")
    if len(parts):
        return parts[-1].lower() in TYPES
    return False


def is_video(file_path):
    TYPES = ["mp4"]
    parts = file_path.split(".")
    if len(parts):
        return parts[-1].lower() in TYPES
    return False


def send_infographics_photos(bot_service, media):
    media = [media_item for media_item in media if is_photo(media_item.full_url)]
    print(media)
    image_urls = [[]]
    for image in media:
        image_urls[-1].append(image.full_url)
        if len(image_urls[-1]) == 9:
            image_urls.append([])
    print(image_urls)
    for images_list in image_urls:
        bot_service.send_images(images_list)


def send_infographics_videos(bot_service, media):
    media = [media_item for media_item in media if is_video(media_item.full_url)]
    print(media)
    video_urls = [[]]
    for video in media:
        video_urls[-1].append(video.full_url)
        if len(video_urls[-1]) == 9:
            video_urls.append([])
    print(video_urls)
    for videos_list in video_urls:
        bot_service.send_images(videos_list)


def main():
    result = convert_to_latin("Ўрмончилар МФЙ")
    # print(result)
    trans = Trans()
    result = trans.translit("Ўрмончилар МФЙ")
    print(result)


if __name__ == "__main__":
    main()