from slugify import slugify

def convert_to_latin(text):
    # text = "Шакарқишлоқ МФЙ"
    text = text.replace("Ё", "Yo").replace("ё", "yo")
    text = text.replace("Ў", "O'").replace("ў", "o'")
    text = text.replace("Қ", "Q").replace("қ", "q")
    text = text.replace("МФЙ", "").strip()
    # result = cyrtranslit.to_latin(text, "ru")
    result = slugify(text, separator=" ").replace(" ", "")
    result = "{} MFY".format(result.title())
    return result


def clean_phone_number(phone):
    result = str(phone) \
            .replace("(", "") \
            .replace(")", "") \
            .replace("-", "") \
            .replace("_", "") \
            .replace(".", "") \
            .replace(" ", "")
    
    sign = "+"
    if len(result) <= 9:
        sign = "+998-"
    return sign + result

def main():
    result = convert_to_latin("Ўрмончилар МФЙ")
    print(result)


if __name__ == "__main__":
    main()