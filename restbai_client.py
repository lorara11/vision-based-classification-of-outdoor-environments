import requests
import time

from config import RESTB_AI_KEY


class RestbAiClient():
    def __init__(self):
        self.key = RESTB_AI_KEY
        self.url = 'https://api-us.restb.ai/vision/v2/multipredict'


    def type_of_zone(self, img_url):
        """Classifies the type of zone that the image depicts.
        It uses the classifier of the Room Type from the restb.ai API.

        :param img_url: URL of the image
        :type img_url: str
        :return: list of tuples ({label},{confidence}), where the label is a str
            which describes the image, and the confidence is a float between 0 and 1.
        :rtype: _type_
        """
        params = {
            'client_key': self.key,
            'model_id':'re_roomtype_global_v2',
            'image_url':img_url
        }
        time.sleep(1)
        response = requests.get(self.url,params=params).json()

        labels_and_confidences = [(d['label'],d['confidence']) for d in response['response']['solutions']['re_roomtype_global_v2']['predictions']]
        labels_and_confidences.sort(key=lambda x: x[1], reverse=True)

        return labels_and_confidences


    def building_exterior_style(self, img_url):
        """Classifies the style of the exterior of the building the image depicts.
        It uses the classifier of the Exterior Style from the restb.ai API.

        :param img_url: URL of the image
        :type img_url: str
        :return: list of tuples ({label},{confidence}), where the label is a str
            which describes the image, and the confidence is a float between 0 and 1.
        :rtype: _type_
        """

        params = {
            'client_key': self.key,
            'model_id':'re_exterior_styles',
            'image_url':img_url
        }
        time.sleep(1)
        response = requests.get(self.url,params=params).json()

        labels_and_confidences = [(d['label'],d['confidence']) for d in response['response']['solutions']['re_exterior_styles']['predictions']]
        labels_and_confidences.sort(key=lambda x: x[1], reverse=True)

        return labels_and_confidences


    def natural_light(self, img_url):
        """Returns True if there is a significant presence of natural light in the place that the image depicts, and False otherwise.

        :param img_url: URL of the image
        :type img_url: str
        :return: True if there is a significant presence of natural light, False otherwise.
        :rtype: bool
        """

        params = {
            'client_key': self.key,
            'model_id':'re_features_v3',
            'image_url':img_url
        }
        time.sleep(1)
        response = requests.get(self.url,params=params).json()

        labels = [d['label'] for d in response['response']['solutions']['re_features_v3']['detections']]

        return ('natural_light' in labels)
    

    def condition(self, img_url):
        """Returns a score of the condition of the place the image depicts. The score is a float from 1.0 to 6.0.

        :param img_url: URL of the image
        :type img_url: str
        :return: score of the condition.
        :rtype: float
        """

        params = {
            'client_key': self.key,
            'model_id':'re_condition',
            'image_url':img_url
        }
        time.sleep(1)
        response = requests.get(self.url,params=params).json()
        
        return response['response']['solutions']['re_condition']['score']


    def image_caption(self, img_url):
        # Experiment

        """Generates a human-readable description of the image.

        :param img_url: URL of the image
        :type img_url: str
        :return: the caption
        :rtype: str
        """

        params = {
            'client_key': self.key,
            'model_id':'caption',
            'image_url':img_url
        }
        time.sleep(1)
        response = requests.get(self.url,params=params).json()

        return response['response']['solutions']['caption']['description']


