def get_ai_response(text):
    responses = {
        "سلام": "سلام 👋 به ANOX خوش اومدی",
        "قیمت": "برای قیمت خدمات لطفاً وارد بخش خدمات شو",
        "سایت": "https://anox-2wmo.vecel.app"
    }

    for k in responses:
        if k in text:
            return responses[k]

    return "در حال بررسی پیام شما هستیم..."