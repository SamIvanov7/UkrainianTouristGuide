import os
import openai
import requests
import time
from speachkit.GPT_voice import synthesize_speech
from dotenv import load_dotenv
import logging
#хуй
load_dotenv()


openai.api_key=os.getenv("OPENAI_API_KEY", default="key")
yandex_api_key=os.getenv("YANDEX_KEY", default="yakey")

# Ask for a prompt

start_chat_log = [
    {
        "role": "system",
        "content": "Act as a Ukrainian cities tourist-guide and tell me about next thing:",
    }
]
chat_log = None
completion = openai.ChatCompletion()


def ask(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    prompt2 = [{"role": "user", "content": f"{question}"}]
    prompt = chat_log + prompt2

    response = completion.create(
        messages=prompt,
        model="gpt-3.5-turbo",
    )
    answer = [response.choices[0].message]
    return answer


def append_interaction_to_chat_log(question, answer, chat_log):
    if chat_log is None:
        chat_log = start_chat_log
    prompt2 = [{"role": "user", "content": f"{question}"}]
    return chat_log + prompt2 + answer


def handle_message(text):
    try:
        global chat_log
        question = f"{text}"
        response = ask(question, chat_log)
        chat_log = append_interaction_to_chat_log(question, response, chat_log)

        # Log the user's message
        logging.info(f"\n\nUser {text}\n**********AI: {response}")

        return response[0].content

    except Exception as e:
        return f"Wait a minute please....{e}"


def get_chat_bot_response(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    prompt2 = [{"role": "user", "content": f"{question}"}]
    prompt = chat_log + prompt2

    response = completion.create(
        messages=prompt,
        model="gpt-3.5-turbo",
    )
    answer = [response.choices[0].message]
    return answer




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

 


# Translate the result using Yandex Translate


# Generate a unique file name using a timestamp

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

# Save the translated result in a unique text file



def read_prompt_and_return_mp3(question, api_key):
    source_language = "en"
    target_language = "ru"
    timestamp = int(time.time())
    file_name = f"./reulst/result_{timestamp}.mp3"


    answer = get_chat_bot_response(question)
    translated_answer = yandex_translate(api_key, answer, source_language, target_language)

    file = synthesize_speech(yandex_api_key, translated_answer, file_name)

    return file


read_prompt_and_return_mp3(question, yandex_api_key)