import cyrtranslit

def convert_to_latin(text):
    # text = "Ёрмозор МФЙ"
    text = text.replace("МФЙ", "").strip()
    result = cyrtranslit.to_latin(text, "ru")
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
        sign = ""
    return sign + result

def main():
    result = convert_to_latin("Ўрмончилар МФЙ")
    print(result)


if __name__ == "__main__":
    main()