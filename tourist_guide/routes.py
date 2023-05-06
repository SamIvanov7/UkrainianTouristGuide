from flask import Blueprint, render_template, request, send_file, jsonify, send_from_directory
from dotenv import load_dotenv
from .guide import UkrainianTouristGuide
from flask import Flask
from tourist_guide.yandex import yandex_translate, synthesize_speech
import os
from os import listdir
import openai
import re
app = Flask(__name__)
guide_bp = Blueprint("guide", __name__)


@guide_bp.route('/audio/<filename>')
def audio(filename):
    audio_file_path = os.path.join('tourist_guide', 'result', filename)
    print(f"Audio file path: {audio_file_path}")  # Add this line to log the file path
    return send_from_directory('tourist_guide/result', filename)

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
            return jsonify({"filename": guide.file_name})
        except FileNotFoundError as e:
            print(f"FileNotFoundError: {e}")
            return str(e), 500
