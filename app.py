import os
import time
import logging
import openai
import requests
from flask import Flask, render_template, request, send_file
from dotenv import load_dotenv

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "./uploads"

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY", default="key")
yandex_api_key = os.getenv("YANDEX_KEY", default="yakey")


class UkrainianTouristGuide:
    def __init__(self):
        self.start_chat_log = [
            {
                "role": "system",
                "content": "Act as a Ukrainian cities tourist-guide and tell me about next thing:",
            }
        ]
        self.chat_log = None
        self.completion = openai.ChatCompletion()

    def ask(self, question):
        if self.chat_log is None:
            self.chat_log = self.start_chat_log
        prompt = self.chat_log + [{"role": "user", "content": question}]

        response = self.completion.create(
            messages=prompt,
            model="gpt-3.5-turbo",
        )
        answer = [response.choices[0].message]
        return answer

    def append_interaction_to_chat_log(self, question, answer):
        if self.chat_log is None:
            self.chat_log = self.start_chat_log
        self.chat_log += [{"role": "user", "content": question}] + answer

    def handle_message(self, text):
        try:
            response = self.ask(text)
            self.append_interaction_to_chat_log(text, response)

            logging.info(f"\n\nUser {text}\n**********AI: {response}")

            return response[0].content

        except Exception as e:
            return f"Wait a minute please....{e}"

    @staticmethod
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

    @staticmethod
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

    def read_prompt_and_return_mp3(self, question, api_key):
        source_language = "en"
        target_language = "ru"
        timestamp = int(time.time())
        file_name = f"./result/result_{timestamp}.mp3"
        answer = self.handle_message(question)
        translated_answer = self.yandex_translate(api_key, answer, source_language, target_language)

        file = self.synthesize_speech(yandex_api_key, translated_answer, file_name)

        return file


    @app.route("/")
    def index():
        return render_template("index.html")


    @app.route("/submit", methods=["POST"])
    def submit():
        if request.method == "POST":
            question = request.form["question"]

            guide = UkrainianTouristGuide()
            file = guide.read_prompt_and_return_mp3(question, yandex_api_key)
            return send_file(file, as_attachment=True)
