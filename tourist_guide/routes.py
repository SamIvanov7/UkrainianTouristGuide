from flask import Blueprint, render_template, request, send_file
from dotenv import load_dotenv
from .guide import UkrainianTouristGuide
from tourist_guide.yandex import yandex_translate, synthesize_speech
import os
import openai
import re
main = Blueprint("main", __name__)

load_dotenv()
yandex_api_key = os.getenv("YANDEX_KEY", default="yakey")


from flask import Blueprint, render_template, request, send_file
from .guide import UkrainianTouristGuide

guide_bp = Blueprint("guide", __name__)

@guide_bp.route("/")
def index():
    return render_template("index.html")

@guide_bp.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        question = request.form["question"]

        guide = UkrainianTouristGuide()
        file = guide.read_prompt_and_return_mp3(guide.file_name, question, yandex_api_key)
        
        def transform_filename(file_name):
            match = re.search(r'_result_(\d+)\.mp3', file_name)
            if match:
                return f'answer_{match.group(1)}'
            else:
                return None


        return send_file(file, as_attachment=True, attachment_filename=transform_filename(guide.file_name), mimetype="audio/mpeg")
