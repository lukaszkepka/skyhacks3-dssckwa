from keras.applications import ResNet50, MobileNet, Xception, DenseNet121
from keras import backend as K
from keras.models import load_model
import numpy as np
import cv2 as cv


def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall


def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision


def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2 * ((precision * recall) / (precision + recall + K.epsilon()))


class VideoAnalyzer:
    def __init__(self, model_path, labels_path):
        self.image_size = 224
        self.labels = self.load_labels(labels_path)
        self.model = load_model(model_path, custom_objects={'f1_m': f1_m})
        self.frame_time_range = 1000
        self.results = {}
        pass

    def clear_state(self):
        self.results = {}

    def load_labels(self, labels_path):
        labels = []
        file_content = open(labels_path, 'r', encoding='utf-8')
        for line in file_content.readlines():
            label = line.lower().strip()
            labels.append(label)
        return np.expand_dims(np.array(labels), axis=0)

    def preprocess_frame(self, image):
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image = cv.resize(image, (self.image_size, self.image_size), interpolation=cv.INTER_AREA)
        image = np.expand_dims(image, axis=0)
        image = image / 255

        return image

    def response_to_dto(self):
        return list(self.results.values())

    def process_image_file(self, file_path):
        image = cv.imread(file_path)
        image = self.preprocess_frame(image)
        labels_values_pred = np.round(self.model.predict(image)).astype(bool)
        return [str(lbl) for lbl in list(self.labels[labels_values_pred])]

    def append_results(self, labels, timestamp):
        for label in labels:
            if not self.results.__contains__(label):
                self.results[label] = {'label': label, 'ranges': []}

            was_in_range = False
            for range in self.results[label]['ranges']:
                if range['start'] < timestamp <= range['end']:
                    range['end'] = int(timestamp + self.frame_time_range)
                    was_in_range = True

            if not was_in_range:
                self.results[label]['ranges'].append(
                    {
                        'start': int(timestamp),
                        'end': int(timestamp + self.frame_time_range),
                    }
                )

    def process_video_file(self, file_path):
        cap = cv.VideoCapture(file_path)
        fps = cap.get(5)

        if not cap.isOpened():
            print("Cannot open camera")
            return

        i = 0
        timestamp = 0
        while True:

            if i % fps != 0:
                print(f'Skipping frame {i}')
                i = i + 1
                continue

            print(f'Prediction on frame {i}')
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            # Predict
            frame = self.preprocess_frame(frame)
            labels_values_pred = np.round(self.model.predict(frame)).astype(bool)
            self.append_results([str(lbl) for lbl in list(self.labels[labels_values_pred])], timestamp)

            # We have processed 30 seconds
            if timestamp >= 30000:
                break

            timestamp = timestamp + 1000
            i = i + 1

        # When everything done, release the capture
        cap.release()

        resp = self.response_to_dto()
        self.clear_state()
        return resp
