import os
import time
import azure.cognitiveservices.speech as speechsdk
import json
from gensim.models import Word2Vec, KeyedVectors, word2vec
import gensim

from os import path
from pydub import AudioSegment


class SpeechToTextAlgorithm:

    def __init__(self, model_path, lema_dict_path, labels_dict_path):
        self.pl_en_label_dict = self.load_labels_dictionary(labels_dict_path)
        self.lematization_dictionary = self.load_lematization_dictionary(lema_dict_path)
        self.word2vec_model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=False)

        self.word_time_range = 1000
        self.similarity_threshold = 0.5
        self.transcript_display_list = []
        self.transcript_ITN_list = []
        self.confidence_list = []
        self.word_metadata_list = []

    def load_labels_dictionary(self, labels_dict_path):
        label_dict = {}
        file_content = open(labels_dict_path, 'r', encoding='utf-8')
        for line in file_content.readlines():
            line_parts = line.lower().split(':')
            label_dict[line_parts[1].strip()] = line_parts[0].strip()
        return label_dict

    def load_lematization_dictionary(self, dictionary_path):
        len_dict = {}
        file_content = open(dictionary_path, 'r', encoding='utf-8')
        for line in file_content.readlines():
            line_parts = line.lower().split(';')
            len_dict[line_parts[1]] = line_parts[0]
        return len_dict

    def convert_to_wav(self, mp3_file_path):
        output_file_path = mp3_file_path[:-3] + "wav"
        sound = AudioSegment.from_mp3(mp3_file_path)
        sound.export(output_file_path, format="wav")
        return output_file_path

    def parse_speech_to_text_result(self, evt):
        print(evt.result.json)
        response = json.loads(evt.result.json)
        self.transcript_display_list.append(response['DisplayText'])
        confidence_list_temp = [item.get('Confidence') for item in response['NBest']]
        max_confidence_index = confidence_list_temp.index(max(confidence_list_temp))
        self.confidence_list.append(response['NBest'][max_confidence_index]['Confidence'])
        self.transcript_ITN_list.append(response['NBest'][max_confidence_index]['ITN'])
        self.word_metadata_list.extend(response['NBest'][max_confidence_index]['Words'])
        print(response['NBest'][max_confidence_index]['Words'])

    def clear_temp_data(self):
        self.transcript_display_list = []
        self.transcript_ITN_list = []
        self.confidence_list = []
        self.word_metadata_list = []

    def extract_text_from_speech_mock(self, w):
        self.word_metadata_list.append(
            {
                'Word': 'TEST',
                'Offset': 100000
            })

        self.word_metadata_list.append(
            {
                'Word': 'TEST',
                'Offset': 200000
            })

    def extract_text_from_speech(self, wav_file_path, language='pl-pl'):
        speech_config = speechsdk.SpeechConfig(
            speech_recognition_language=language,
            subscription=os.environ['AZURE_SPEECH_KEY'],
            region=os.environ['AZURE_SERVICE_REGION']
        )

        speech_config.request_word_level_timestamps()
        speech_config.output_format = speechsdk.OutputFormat.Detailed

        audio_config = speechsdk.audio.AudioConfig(filename=wav_file_path)
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config
        )

        done = False

        def stop_cb(evt):
            """callback that signals to stop continuous recognition upon receiving an event `evt`"""
            print('CLOSING on {}'.format(evt))
            nonlocal done
            done = True

        # Connect callbacks to the events fired by the speech recognizer
        speech_recognizer.recognized.connect(lambda evt: self.parse_speech_to_text_result(evt))
        speech_recognizer.session_stopped.connect(stop_cb)
        speech_recognizer.canceled.connect(stop_cb)

        speech_recognizer.start_continuous_recognition()
        while not done:
            time.sleep(.5)

        speech_recognizer.stop_continuous_recognition()

    def preprocess_word(self, word):
        word_lemat = self.lematization_dictionary.get(word)
        return word_lemat if word_lemat is not None else word

    def response_to_dto(self, response):
        for i in response.values():
            i['label'] = self.pl_en_label_dict[i['label']]

        return list(response.values())

    def append_word_to_result(self, response, timestamp, label):
        if not response.__contains__(label):
            response[label] = {'label': label, 'ranges': []}

        was_in_range = False
        for range in response[label]['ranges']:
            if range['start'] < timestamp <= range['end']:
                range['end'] = int(timestamp + self.word_time_range)
                was_in_range = True

        if not was_in_range:
            response[label]['ranges'].append(
                {
                    'start': int(timestamp),
                    'end': int(timestamp + self.word_time_range),
                }
            )

    def process(self, mp3_file_path):
        response = {}
        wav_file_path = self.convert_to_wav(mp3_file_path)
        self.extract_text_from_speech(wav_file_path)

        for word_metadata in self.word_metadata_list:
            timestamp = word_metadata['Offset'] / 10000
            original_word = word_metadata['Word'].lower()
            word = self.preprocess_word(original_word)

            for label in self.pl_en_label_dict.keys():
                try:
                    similarity = self.word2vec_model.similarity(word, label)

                    if similarity >= self.similarity_threshold:
                        self.append_word_to_result(response, timestamp, label)

                    print(f'({timestamp}) {word} <=> {label} = {similarity}')
                except KeyError as e:
                    print(e)

        self.clear_temp_data()
        return self.response_to_dto(response)
