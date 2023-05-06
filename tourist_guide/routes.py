from flask import Blueprint, render_template, request, send_file
from dotenv import load_dotenv
from .guide import UkrainianTouristGuide
from tourist_guide.yandex import yandex_translate, synthesize_speech
import os
from os import listdir
import openai
import re

guide_bp = Blueprint("guide", __name__)

@guide_bp.route("/")
def index():
    return render_template("index.html")

@guide_bp.route("/submit", methods=["POST"])
def submit():

            
    if request.method == "POST":
        question = request.form["question"]

        guide = UkrainianTouristGuide()

        print("Before calling read_prompt_and_return_mp3")
        output_file_path = guide.read_prompt_and_return_mp3(question)
        print(f"After calling read_prompt_and_return_mp3, output_file_path: {output_file_path}")

        try:
            return send_file(guide.file_name, as_attachment=True, attachment_filename="answer", mimetype="audio/mpeg")
        except FileNotFoundError as e:
            print(f"FileNotFoundError: {e}")
            print("Files in the /app/tourist_guide/result directory:")
            print(listdir('/app/tourist_guide/result'))
            return str(e), 500
