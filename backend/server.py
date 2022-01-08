from flask import Flask, jsonify, request
from flask_cors import cross_origin
import random
import urllib
from bs4 import BeautifulSoup
import pickle
import requests
from FeaturesExtraction.featureExtraction import FeatureExtraction
import numpy as np
import pandas as pd
# --------------------------------------------------------------------------------------------------------------------------------------------

class ServerRestAPI():

    #load our Best Model from the pickle file
    def __init__(self):
        #The best model is :          "randomForestModel-18Features.pkl" ou bien "bestModel-18Features.pkl"
        fileName = "ModelTraining/Models/bestModel-18Features.pkl"
        with open(fileName, 'rb') as file:
            self.model = pickle.load(file)

    def runServer(self):
        app = Flask(__name__)

        @app.route('/predict', methods=['GET'])
        @cross_origin()
        def predict():
            #get Url from Path Params
            url = request.args['url']
            print("The url : ",url)
            isRealUrl = False
            try:
                response = requests.get(url, timeout=5)
                print(response)
                if response.status_code < 400:
                    isRealUrl = True
            except:
                isRealUrl = False

            if(not(isRealUrl)):
                try:
                    rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(),
                              features="html.parser").find("reach")["rank"]
                    isRealUrl2 = True
                except TypeError:
                    isRealUrl2 = False

            if (True):
                #extract Features from the URL
                featureExtraction = FeatureExtraction()
                numberOfFeatures = 18
                features = featureExtraction.extractFeaturesFromUrl(url, numberOfFeatures)
                print('The extracted features : ', features)
                # Add columns name to the features, then predict if its phishing or safe url
                features = np.array(features)
                features = features.reshape(1, -1)
                features = pd.DataFrame(features)
                features.columns = ['hasIpAddress', 'hasAtSymbol', 'isLong', 'depth', 'hasPointInDomain', 'hasNumberInDomain', 'isShortened',
                                 'urlLength', 'dashNbr', 'underlineNbr', 'questionMarkNbr', 'andNbr', 'pointNbr', 'domainLength',
                                 'hasDnsRecord', 'webTraffic', 'domainAge', 'domainEnd'
                                 ]
                print('Features as DataFrame : ', features)
                prediction = self.model.predict(features)
                print("Prediction : ", prediction[0])
                # Prediction == 0 ==> Phishing url
                # Prediction == 1 ==> Safe url
                # --------------------------------
                a = jsonify(str(prediction[0]))
                return a
            else:
                a = jsonify(str(2))
                return a


        app.run(debug=True)


# --------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # threading.Thread(target=runServer).start()# run local server when starting the app
    server = ServerRestAPI()
    server.runServer()