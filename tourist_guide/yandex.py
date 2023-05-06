import requests

def yandex_translate(api_key, text, source_lang, target_lang):
    url = "https://translate.api.cloud.yandex.net/translate/v2/translate"

    headers = {
        "Authorization": f"Api-Key {api_key}"
    }

    data = {
        "texts": [text],
        "sourceLanguageCode": source_lang,
        "targetLanguageCode": target_lang
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        translated_text = response.json()['translations'][0]['text']
        return translated_text
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def synthesize_speech(api_key, text, output_file, lang="ru-RU", voice="alena", format="mp3", emotion="neutral"):
    url = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"

    headers = {
        "Authorization": f"Api-Key {api_key}"
    }

    data = {
        "text": text,
        "lang": lang,
        "voice": voice,
        "format": format,
        "emotion": emotion
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"Audio saved to {output_file}")
        return output_file
    else:
        print(f"Error: {response.status_code} - {response.text}")
