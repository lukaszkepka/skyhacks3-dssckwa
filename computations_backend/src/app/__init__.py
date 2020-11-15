from flask import Flask
from flask_cors import CORS

from speech_recognition.recognize import SpeechToTextAlgorithm
from video_analysis.analyzer import VideoAnalyzer

from src.plots_gen.PlotsGenerator import PlotsGenerator

app = Flask(__name__)
CORS(app)

text_model_lite_path = '../model/wiki-lemmas-all-100-skipg-ns.txt'
text_model_path = '../model/nkjp+wiki-forms-all-300-skipg-hs-50.txt'
lema_dict_path = '../model/polimorfologik-2.1.txt'
labels_en_pl_dict_path = '../model/labels_eng_pl.txt'
labels_path = '../model/labels.txt'
classification_model_path = '../model/Xceptionfinal_two_stage_check_fix.h5'

plots_generator = PlotsGenerator(labels_dict_path)

print('Started speech recognition module initialization')
speech_to_text_service = None # SpeechToTextAlgorithm(text_model_path, lema_dict_path, labels_en_pl_dict_path)
print('Finished speech recognition module initialization')

print('Started classification module initialization')
classification_service = VideoAnalyzer(classification_model_path, labels_path)
print('Finished classification module initialization')

from app import routes
