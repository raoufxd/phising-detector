from FeaturesExtraction.urlBasedFeatures import UrlBasedFeatures
from FeaturesExtraction.domainBasedFeatures import DomainBasedFeatures
import requests

class FeatureExtraction():

    #extract features from All the URLs
    def extractAllFeatures(self, url, numberOfFeatures, label):
        features= []
        if(numberOfFeatures == 18):
            # extract URL based features
            urlBasedFeatures = UrlBasedFeatures()
            features1 = urlBasedFeatures.extractFeatures(url)
            # extract DOMAIN based features
            domainBasedFeatures = DomainBasedFeatures()
            features2 = domainBasedFeatures.extractFeatures(url)
            # return all features in one list
            features = features1 + features2
        else:
            # extract URL based features
            urlBasedFeatures = UrlBasedFeatures()
            features1 = urlBasedFeatures.extractFeatures(url)
            # return features in one list
            features = features1
        #add the label (0 for safe url, 1 for phishing url)
        features.append(label)
        return features


    #extract features from One URL
    def extractFeaturesFromUrl(self, url, numberOfFeatures):
        #extract URL based features
        urlBasedFeatures = UrlBasedFeatures()
        features1 = urlBasedFeatures.extractFeatures(url)

        # extract DOMAIN based features
        domainBasedFeatures = DomainBasedFeatures()
        features3 = domainBasedFeatures.extractFeatures(url)

        #return all features in one list

        if numberOfFeatures == 14:
            features = features1
        else:
            features = features1 + features3
        return features


if __name__=="__main__":
    featureExtraction = FeatureExtraction()
    url = 'http://www.google.com/profile?user=105405&token=dqsdq//example.dz'
    features = featureExtraction.extractAllFeatures(url, 17, 0)
    print("All the"
          " features : ", features)
    print("Number of features : ", len(features))

