from FeaturesExtraction.featureExtraction import FeatureExtraction
import pandas as pd
import requests


class DatasetPretreatment():
#--------------------------------------------------------------------------------#

    #Les quatres fonctions suivantes ont un role de faire un pretraitement sur les dataset collecté du web
    #c-à-dire lire les fichier et garder que les attribut "url" et "label", pour chaqu'un des 4 fichiers

    def dataset1Traitement(self):
        #fichier 1#
        input = pd.read_csv("DatasetRaw/dataset1.csv")
        output = []
        for i in range(input.shape[0]):
            print(i)
            url = input['url'][i]
            label = 1 #en cas safe url
            if input['status'][i] =='phishing':
                label = 0 #en cas phishing url
            output.append([url, label])
        outputDF = pd.DataFrame(output, columns=['url', 'label'])
        outputDF.to_csv('DatasetPretreated/dataset1.csv', index=False)
        print("data is pretreated!")

    def dataset2Traitement(self):
        # fichier 2#
        input = pd.read_csv("DatasetRaw/phishingUrls.csv")
        output = []
        for i in range(input.shape[0]):
            print(i)
            url = input['url'][i]
            label = 0  # car cas phishing url
            output.append([url, label])
        outputDF = pd.DataFrame(output, columns=['url', 'label'])
        outputDF.to_csv('DatasetPretreated/phishingUrls.csv', index=False)
        print("data is pretreated!")

    def dataset3Traitement(self):
        # fichier 3#
        input = pd.read_csv("DatasetRaw/safeUrls.csv")
        input.columns= ['url']
        output = []
        for i in range(input.shape[0]):
            print(i)
            url = input['url'][i]
            label = 1  # car cas safe url
            output.append([url, label])
        outputDF = pd.DataFrame(output, columns=['url', 'label'])
        outputDF.to_csv('DatasetPretreated/safeUrls.csv', index=False)
        print("data is pretreated!")

    def dataset4Traitement(self):
        # fichier 4#
        input = pd.read_json("DatasetRaw/safeUrls2.json")
        output = []
        for i in range(input.shape[0]):
            print(i)
            url = input['domain'][i]
            label = 1  # car cas safe url
            output.append([url, label])
        outputDF = pd.DataFrame(output, columns=['url', 'label'])
        outputDF.to_csv('DatasetPretreated/safeUrls2.csv', index=False)
        print("data is pretreated!")

#--------------------------------------------------------------------------------#


#--------------------------------------------------------------------------------#

    #check if an url is real or not (exist on web or not)
    def isUrlReal(self, url):
        try:
            response = requests.head(url, timeout=1)
            if response.status_code < 400:
                return 1
        except:
            return 0
        return 0


    #This function do the dataset cleaning (delete the url's that don't work from our raw dataset)
    # c-à-dire: supprimer les sites qui ne fonctionne pas ( qui sont supprimer du l'internet)
    def cleanDataset(self):
        #on charge les 4 sources de donnees "safeUrls.csv" "safeUrls2.csv" "phishingUrls.csv" "dataset1.csv"
        dataset1 = pd.read_csv('DatasetPretreated/dataset1.csv')
        dataset2 = pd.read_csv('DatasetPretreated/safeUrls.csv')
        dataset3 = pd.read_csv('DatasetPretreated/safeUrls2.csv')
        dataset4 = pd.read_csv('DatasetPretreated/phishingUrls.csv')

        #ce variable contient les 4 dataset
        datasetList = [dataset1, dataset2, dataset3, dataset4]
        #on parcour chaque dataset et on laisse que les urls qui marche ( on supprime les autres)
        datasetCleanedSafe = []
        datasetCleanedPhishing = []
        nbrSafe = 0
        nbrPhishing = 0
        for dataset in datasetList:
            for i in range(dataset.shape[0]):
                url = dataset['url'][i]
                label = dataset['label'][i]
                print(i)
                boolean = self.isUrlReal(url)
                if boolean:
                    if label == 1:
                        datasetCleanedSafe.append([url, label])
                        nbrSafe += 1
                    else:
                        datasetCleanedPhishing.append([url, label])
                        nbrPhishing += 1

        datasetCleanedSafeDF = pd.DataFrame(datasetCleanedSafe, columns=['url', 'label'])
        datasetCleanedSafeDF.to_csv('DatasetCleaned/datasetSafe.csv', index=False)

        datasetCleanedPhishingDF = pd.DataFrame(datasetCleanedPhishing, columns=['url', 'label'])
        datasetCleanedPhishingDF.to_csv('DatasetCleaned/datasetPhishing.csv', index=False)

        print("Le nombre de url safe est : ", nbrSafe)
        print("Le nombre de url de phishing est : ", nbrPhishing)
        print("Dataset has been cleaned !")

    #cette fonctionne verifie dans les deux fichier "datasetSafe.csv" et "datasetPhishing.csv" s'il y'a des url doublés
    def datasetVerifyUniqueUrls(self):
        datasetPhishing = pd.read_csv('DatasetCleaned/datasetPhishing.csv')
        datasetPhishingUniqueUrl = dict()
        #pour le fichier de phishing urls
        for i in range(datasetPhishing.shape[0]):
            print(i)
            url = datasetPhishing['url'][i]
            label = datasetPhishing['label'][i]
            datasetPhishingUniqueUrl[url] = label
        datasetPhishingUniqueUrlDF = pd.DataFrame(datasetPhishingUniqueUrl.items(), columns=['url', 'label'])
        datasetPhishingUniqueUrlDF.to_csv('DatasetCleaned/datasetPhishingUnique.csv', index=False)

        #pour le fichier de safe urls
        datasetSafe = pd.read_csv('DatasetCleaned/datasetSafe.csv')
        datasetSafeUniqueUrl = dict()
        #pour prendre les url court et les plus consultés dans l'internet
        # (car ils se trouvent à la fin du fichier à partir de la ligne 32909)
        for i in range(32909, datasetSafe.shape[0]):
            print(i)
            url = datasetSafe['url'][i]
            label = datasetSafe['label'][i]
            datasetSafeUniqueUrl[url] = label
        #melanger les lignes et completer le traitement de verification des doublants
        datasetSafe = datasetSafe.sample(frac=1).reset_index(drop=True)
        for i in range(datasetSafe.shape[0]):
            print(i)
            url = datasetSafe['url'][i]
            label = datasetSafe['label'][i]
            datasetSafeUniqueUrl[url] = label
        datasetSafeUniqueUrlDF = pd.DataFrame(datasetSafeUniqueUrl.items(), columns=['url', 'label'])
        datasetSafeUniqueUrlDF.to_csv('DatasetCleaned/datasetSafeUnique.csv', index=False)

        print("Le nombre des urls dans 'datasetSafeUnique.csv' est : ", datasetSafeUniqueUrl.__len__())
        print("Le nombre des urls dans 'datasetPhishingUnique.csv' est : ", datasetPhishingUniqueUrl.__len__())
        print("Dataset has been verified !")

#--------------------------------------------------------------------------------#
    #fusionner les fichiers "datasetSafe.csv" et "datasetPhishing.csv" dans un seul fichier appelé "dataset.csv"
    def generateDataset(self):
        datasetSafe = pd.read_csv('DatasetCleaned/datasetSafeUnique.csv')
        datasetPhishing = pd.read_csv('DatasetCleaned/datasetPhishingUnique.csv')
        nbrPhishingUrl = datasetPhishing.shape[0]
        nbrSafeUrl = datasetSafe.shape[0]
        #le nombre d'url à utilisé du chaque fichier dans le fichier final "dataset.csv"
        nbrUrlsToUse = nbrSafeUrl
        if nbrPhishingUrl < nbrSafeUrl:
            nbrUrlsToUse = nbrPhishingUrl
        datasetFinal = []
        for i in range(nbrUrlsToUse):
            print("safe : ", i)
            url = datasetSafe['url'][i]
            label = datasetSafe['label'][i]
            datasetFinal.append([url, label])
        for i in range(nbrUrlsToUse):
            print("phishing : ", i)
            url = datasetPhishing['url'][i]
            label = datasetPhishing['label'][i]
            datasetFinal.append([url, label])
        datasetFinalDF = pd.DataFrame(datasetFinal, columns=['url', 'label'])
        datasetFinalDF.to_csv('DatasetCleaned/dataset.csv', index=False)
        print('Le dataset finale est crée')
#--------------------------------------------------------------------------------#

    def extractFeaturesFromDataset(self,numberOfFeatures):
        dataset = pd.read_csv('DatasetCleaned/dataset.csv' )
        print("shape of the dataset : ", dataset.shape)
        #extract features from dataset
        featureExtraction = FeatureExtraction()
        datasetFeatures = []
        for i in range(dataset.shape[0]):
            print(i)
            url = dataset['url'][i]
            label = dataset['label'][i]
            try:
                datasetFeatures.append(featureExtraction.extractAllFeatures(url, numberOfFeatures, label))
            except:
                pass
        featuresNames = []
        if (numberOfFeatures == 18):
            featuresNames = ['hasIpAddress', 'hasAtSymbol', 'isLong', 'depth', 'hasPointInDomain', 'hasNumberInDomain', 'isShortened',
                             'urlLength', 'dashNbr', 'underlineNbr', 'questionMarkNbr', 'andNbr', 'pointNbr', 'domainLength',
                             'hasDnsRecord', 'webTraffic', 'domainAge', 'domainEnd',
                             'label']
        else: # numberOfFeatures == 14
            featuresNames = ['hasIpAddress', 'hasAtSymbol', 'isLong', 'depth', 'hasPointInDomain', 'hasNumberInDomain', 'isShortened',
                             'urlLength', 'dashNbr', 'underlineNbr', 'questionMarkNbr', 'andNbr', 'pointNbr', 'domainLength',
                             #'hasDnsRecord', 'webTraffic', 'domainAge', 'domainEnd',
                             'label']

        datasetDF = pd.DataFrame(datasetFeatures, columns=featuresNames)
        datasetDF.to_csv('DatasetExtractedFeatures/dataset-' +str(numberOfFeatures)+ 'Features.csv',  index= False)
        print("The dataset with "+ str(numberOfFeatures) +" features has generated!")

    """  def generatePhishingUrlsDataset(self,numberOfFeatures):
        phishingUrls = pd.read_csv('DatasetRaw/phishingUrls.csv' )
        # take 10.000 phishing url randomly
        phishingUrls = phishingUrls.sample(n=10000, random_state=12).copy()
        phishingUrls = phishingUrls.reset_index(drop=True)
        print("shape of safeUrls dataset : ", phishingUrls.shape)
        #extract features from phishingUrls
        featureExtraction = FeatureExtraction()
        phishingUrlFeatures = []
        # for phishing url we set label to 1
        label = 1
        for i in range(0, 10000):
            print(i)
            url = phishingUrls['url'][i]
            try:
                phishingUrlFeatures.append(featureExtraction.extractAllFeatures(url, numberOfFeatures, label))
            except:
                pass
        featuresNames = []
        if (numberOfFeatures == 13):
            featuresNames = ['DomainName', 'hasIpAddress', 'hasAtSymbol', 'isLong', 'depth', 'hasRedirection',
                             'hasHttps', 'isShortened', 'hasDash',
                             # 'hasDnsRecord', 'webTraffic', 'domainAge', 'domainEnd',
                             'hasIframeRedirection', 'isStatusBarCustomized', 'isRightClickDisabled', 'forwarding',
                             'label']
        else:  # numberOfFeatures == 9
            featuresNames = ['DomainName', 'hasIpAddress', 'hasAtSymbol', 'isLong', 'depth', 'hasRedirection',
                             'hasHttps', 'isShortened', 'hasDash',
                             # 'hasDnsRecord', 'webTraffic', 'domainAge', 'domainEnd',
                             # 'hasIframeRedirection', 'isStatusBarCustomized', 'isRightClickDisabled', 'forwarding',
                             'label']
        phishingUrlsDF = pd.DataFrame(phishingUrlFeatures, columns=featuresNames)
        phishingUrlsDF.to_csv('DatasetPretreated/phishingUrlDataset-' +str(numberOfFeatures)+ 'Features.csv',  index= False)
        print(phishingUrlsDF.head())
        print("Phishing URLs dataset with "+ str(numberOfFeatures) +" features has generated!")

    def generateGlobalDataset(self, numberOfFeatures):
        phishingUrls = pd.read_csv('DatasetPretreated/phishingUrlDataset-' +str(numberOfFeatures)+ 'Features.csv')
        safeUrls = pd.read_csv('DatasetPretreated/safeUrlDataset-' +str(numberOfFeatures)+ 'Features.csv')
        globalDataset = pd.concat([safeUrls, phishingUrls]).reset_index(drop=True)
        globalDataset.to_csv('DatasetPretreated/globalUrlDataset-' +str(numberOfFeatures)+ 'Features.csv', index=False)
        print(globalDataset.head())
        print("Global (Phishing + Safe) URLs dataset with "+ str(numberOfFeatures) +" features has generated!")

    def generateDataset1(self, numberOfFeatures):
        dataset1 = pd.read_csv('DatasetRaw/dataset1.csv')
        dataset1.drop(dataset1.columns.difference(['url', 'status']), 1, inplace=True)
        print("shape of dataset 1 : ", dataset1.shape)
        # extract features from dataset1
        featureExtraction = FeatureExtraction()
        dataset1Features = []
        # for phishing url we set label to 1 and 0 for safe url
        for i in range(dataset1.shape[0]):
            print(i)
            url = dataset1['url'][i]
            try:
                label = 1
                if dataset1['status'][i] == "legitimate":
                    label = 0
                else:
                    label = 1
                dataset1Features.append(featureExtraction.extractAllFeatures(url, numberOfFeatures, label))
            except:
                pass
        featuresNames = []
        if (numberOfFeatures == 13):
            featuresNames = ['DomainName', 'hasIpAddress', 'hasAtSymbol', 'isLong', 'depth', 'hasRedirection',
                             'hasHttps', 'isShortened', 'hasDash',
                             # 'hasDnsRecord', 'webTraffic', 'domainAge', 'domainEnd',
                             'hasIframeRedirection', 'isStatusBarCustomized', 'isRightClickDisabled', 'forwarding',
                             'label']
        else:  # numberOfFeatures == 9
            featuresNames = ['DomainName', 'hasIpAddress', 'hasAtSymbol', 'isLong', 'depth', 'hasRedirection',
                             'hasHttps', 'isShortened', 'hasDash',
                             # 'hasDnsRecord', 'webTraffic', 'domainAge', 'domainEnd',
                             # 'hasIframeRedirection', 'isStatusBarCustomized', 'isRightClickDisabled', 'forwarding',
                             'label']
        dataset1DF = pd.DataFrame(dataset1Features, columns=featuresNames)
        dataset1DF.to_csv('DatasetPretreated/dataset1-' + str(numberOfFeatures) + 'Features.csv',
                              index=False)
        print(dataset1DF.head())
        print("Dataset 1 with " + str(numberOfFeatures) + " features has generated!")


    def generateDataset2(self, numberOfFeatures):
        dataset2 = pd.read_csv('DatasetRaw/dataset2.csv')
        print("shape of dataset 2 : ", dataset2.shape)
        # extract features from dataset2
        featureExtraction = FeatureExtraction()
        dataset2Features = []
        # for phishing url we set label to 1 and 0 for safe url
        for i in range(dataset2.shape[0]):
            print(i)
            url = dataset2['URL'][i]
            try:
                label = 1
                if dataset2['Label'][i] == "good":
                    label = 0
                else:
                    label = 1
                dataset2Features.append(featureExtraction.extractAllFeatures(url, numberOfFeatures, label))
            except:
                pass
        featuresNames = []
        if (numberOfFeatures == 13):
            featuresNames = ['DomainName', 'hasIpAddress', 'hasAtSymbol', 'isLong', 'depth', 'hasRedirection',
                             'hasHttps', 'isShortened', 'hasDash',
                             # 'hasDnsRecord', 'webTraffic', 'domainAge', 'domainEnd',
                             'hasIframeRedirection', 'isStatusBarCustomized', 'isRightClickDisabled', 'forwarding',
                             'label']
        else:  # numberOfFeatures == 9
            featuresNames = ['DomainName', 'hasIpAddress', 'hasAtSymbol', 'isLong', 'depth', 'hasRedirection',
                             'hasHttps', 'isShortened', 'hasDash',
                             # 'hasDnsRecord', 'webTraffic', 'domainAge', 'domainEnd',
                             # 'hasIframeRedirection', 'isStatusBarCustomized', 'isRightClickDisabled', 'forwarding',
                             'label']
        dataset2DF = pd.DataFrame(dataset2Features, columns=featuresNames)
        dataset2DF.to_csv('DatasetPretreated/dataset2-' + str(numberOfFeatures) + 'Features.csv',
                              index=False)
        print(dataset2DF.head())
        print("Dataset 2 with " + str(numberOfFeatures) + " features has generated!")


    def generateDataset3(self, numberOfFeatures):
        dataset3 = pd.read_csv('DatasetRaw/dataset3.csv')
        dataset3.drop(dataset3.columns.difference(['domain', 'label']), 1, inplace=True)
        print("shape of dataset 3 : ", dataset3.shape)
        # extract features from dataset3
        featureExtraction = FeatureExtraction()
        dataset3Features = []
        # for phishing url we set label to 1 and 0 for safe url
        for i in range(dataset3.shape[0]):
            print(i)
            url = dataset3['domain'][i]
            try:
                label = dataset3['label'][i]
                dataset3Features.append(featureExtraction.extractAllFeatures(url, numberOfFeatures, label))
            except:
                pass
        featuresNames = []
        if (numberOfFeatures == 13):
            featuresNames = ['DomainName', 'hasIpAddress', 'hasAtSymbol', 'isLong', 'depth', 'hasRedirection',
                             'hasHttps', 'isShortened', 'hasDash',
                              'hasDnsRecord', 'webTraffic', 'domainAge', 'domainEnd',
                             #'hasIframeRedirection', 'isStatusBarCustomized', 'isRightClickDisabled', 'forwarding',
                             'label']
        else:  # numberOfFeatures == 9
            featuresNames = ['DomainName', 'hasIpAddress', 'hasAtSymbol', 'isLong', 'depth', 'hasRedirection',
                             'hasHttps', 'isShortened', 'hasDash',
                             # 'hasDnsRecord', 'webTraffic', 'domainAge', 'domainEnd',
                             # 'hasIframeRedirection', 'isStatusBarCustomized', 'isRightClickDisabled', 'forwarding',
                             'label']
        dataset3DF = pd.DataFrame(dataset3Features, columns=featuresNames)
        dataset3DF.to_csv('DatasetPretreated/dataset3-' + str(numberOfFeatures) + 'Features.csv',
                              index=False)
        print(dataset3DF.head())
        print("Dataset 3 with " + str(numberOfFeatures) + " features has generated!")

"""

if __name__ == "__main__":
    datasetPretreatment = DatasetPretreatment()
    """you have to run each function individually"""

    """ les quatre fonctions qui pretraitent les dataset brutes"""
    #datasetPretreatment.dataset1Traitement()
    #datasetPretreatment.dataset2Traitement()
    #datasetPretreatment.dataset3Traitement()
    #datasetPretreatment.dataset4Traitement()

    """la fonction qui lance le nettoyage des données"""
    #datasetPretreatment.cleanDataset()

    """Les fonction suivante verifie la redondance des url dans données"""
    #datasetPretreatment.datasetVerifyUniqueUrls()

    """Les fonction suivante cree le dataset finale à utiliser dans la phase d'extraction des paramètres"""
    #datasetPretreatment.generateDataset()

    """Les fonction suivante lance l'extaction des paramètres du dataset,
    Il y'a deux cas 14 ou 18 features"""
    numberOfFeatures = 18
    datasetPretreatment.extractFeaturesFromDataset(numberOfFeatures)
    #datasetPretreatment.generateSafeUrlsDataset(numberOfFeatures)
    #datasetPretreatment.generatePhishingUrlsDataset(numberOfFeatures)
    #datasetPretreatment.generateGlobalDataset(numberOfFeatures)



    #datasetPretreatment.generateDataset1(numberOfFeatures)
    #datasetPretreatment.generateDataset2(numberOfFeatures)
    #datasetPretreatment.generateDataset3(numberOfFeatures)

    #datasetPretreatment.jsonToCSV()
