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

def main():
    result = convert_to_latin("Ўрмончилар МФЙ")
    # print(result)
    trans = Trans()
    result = trans.translit("Ўрмончилар МФЙ")
    print(result)


if __name__ == "__main__":
    main()