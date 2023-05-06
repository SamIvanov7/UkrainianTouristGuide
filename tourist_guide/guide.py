import os
import time
import logging
import openai
from .yandex import yandex_translate, synthesize_speech



class UkrainianTouristGuide:
    timestamp = int(time.time())
    current_directory = os.path.dirname(os.path.abspath(__file__))
    result_directory = os.path.join(current_directory, "result")
    file_name = os.path.join(result_directory, f"answer_{timestamp}.mp3")
    openai.api_key = os.getenv("OPENAI_API_KEY", default="key")
    yandex_api_key = os.getenv("YANDEX_KEY", default="yakey")


    def __init__(self):
        self.start_chat_log = [
            {
                "role": "system",
                "content": "Act as a Ukrainian cities tourist-guide and tell me about the next thing:",
            }
        ]
        self.chat_log = None
        self.completion = openai.ChatCompletion()
        os.makedirs(self.result_directory, exist_ok=True)

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
        
    
    def read_prompt_and_return_mp3(self, question):
        source_language = "en"
        target_language = "ru"


        answer = self.handle_message(question)
        translated_answer = yandex_translate(self.yandex_api_key, answer, source_language, target_language)

        print(f"Answer: {answer}")
        print(f"Translated answer: {translated_answer}")

        file = synthesize_speech(self.yandex_api_key, translated_answer, self.file_name)
        print(f"File path returned by synthesize_speech: {file}")

        print(f"File: {file}")

        return file
