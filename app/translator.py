from deep_translator import GoogleTranslator

SUPPORTED_LANGUAGES = {
    "en":  {"name": "English",    "google_code": None},   
    "fil": {"name": "Filipino",   "google_code": "tl"},   
    "ceb": {"name": "Cebuano",    "google_code": "ceb"},
    "hil": {"name": "Hiligaynon", "google_code": "ceb"},  
    "ilo": {"name": "Ilocano",    "google_code": "ilo"},
}

def translate_text(text: str, google_code: str) -> str:

    if not text:
        return text

    try:
        result = GoogleTranslator(source="en", target=google_code).translate(text)
        return result if result else text
    except Exception as e:
        print(f"Translation error (target={google_code}): {e}")
        return text


def translate_response(response: dict, language: str) -> dict:

    if language == "en":
        return response

    config = SUPPORTED_LANGUAGES.get(language)

    if not config or not config["google_code"]:
        return response

    google_code = config["google_code"]
    translated = response.copy()

    string_fields = ["action", "referral", "medicines", "follow_up", "flag"]
    for field in string_fields:
        if translated.get(field):
            translated[field] = translate_text(translated[field], google_code)

    if translated.get("lifestyle"):
        translated["lifestyle"] = [
            translate_text(item, google_code)
            for item in translated["lifestyle"]
        ]

    translated["language"] = config["name"]

    return translated