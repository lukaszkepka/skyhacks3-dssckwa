from flask import Flask
from flask_cors import CORS

from speech_recognition.recognize import SpeechToTextAlgorithm

app = Flask(__name__)
CORS(app)

mp3_file_path = 'C:\\Users\\Lukasz Kepka\\Downloads\\audio_all\\audio_all\\audio_tour\\69384\\pl\\625986.mp3'
text_model_lite_path = '../model/wiki-lemmas-all-100-skipg-ns.txt'
text_model_path = '../model/nkjp+wiki-forms-all-300-skipg-hs-50.txt'
lema_dict_path = '../model/polimorfologik-2.1.txt'
labels_dict_path = '../model/labels_eng_pl.txt'

print('Started speech recognition module initialization')
speech_to_text_service = SpeechToTextAlgorithm(text_model_lite_path, lema_dict_path, labels_dict_path)
print('Finished speech recognition module initialization')

from app import routes
