"""
This file can be used to try a live prediction. 
"""

import keras
import librosa
import numpy as np

class LivePredictions:
    """
    Main class of the application.
    """

    def __init__(self, file):
        """
        Init method is used to initialize the main parameters.
        """
        self.file = file
        # self.path = MODEL_DIR_PATH + 'Emotion_Voice_Detection_Model_2.h5'
        self.path = '/Users/ammar/Interview_App/Interview_App/Audio_Emotion/Emotion_Voice_Detection_Model_2.h5'
        self.loaded_model = keras.models.load_model(self.path)

    def make_predictions(self):
        """
        Method to process the files and create your features.
        """
        data, sampling_rate = librosa.load(self.file)
        mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sampling_rate, n_mfcc=40).T, axis=0)
        # x = np.expand_dims(mfccs, axis=2)
        x = np.expand_dims(mfccs, axis=0)
        predictions = np.argmax(self.loaded_model.predict(x),axis=1)
        # print(predictions[0])
        print( "Prediction is", " ", self.convert_class_to_emotion(predictions[0]))
        return self.convert_class_to_emotion(predictions[0])
    
    @staticmethod
    def convert_class_to_emotion(pred):
        """
        Method to convert the predictions (int) into human readable strings.
        """
        
        label_conversion = {'0': 'neutral',
                            '1': 'calm',
                            '2': 'happy',
                            '3': 'sad',
                            '4': 'angry',
                            '5': 'fearful',
                            '6': 'disgust',
                            '7': 'surprised'}

        for key, value in label_conversion.items():
            if int(key) == pred:
                label = value
        return label


    def predict(audio_path):
        live_prediction = LivePredictions(file=audio_path)
        prediction = live_prediction.make_predictions()
        return prediction

