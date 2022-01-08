import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, recall_score
import numpy as np
import pickle
import seaborn


class ModelTraining():

    def showStatistics(self):
        data = pd.read_csv("../DatasetPretreatment/DatasetExtractedFeatures/dataset-14Features.csv")
        print(data.head())
        print(data.tail())
        print("Shape of dataset : ", data.shape)
        print("Columns of dataset : ", data.columns)
        print("Info about dataset : \n", data.info())
        print("Dataset description : \n", data.describe(()))
        print("Number of missing values in the dataset : \n", data.isnull().sum())
        #show the distributions of each columns of our dataset
        data.hist(bins= 50, figsize= (15, 15))
        plt.show()

    def svcModel(self, X_train, X_valid, y_train, y_valid, numberOfFeatures):
        print('SVM Model Training')
        C_range = [3,5,7,9]
        bestAccuracy = 0
        bestModel = None
        bestC = 0
        kernels = ['sigmoid', "rbf"]
        bestTestPredctions = []
        for kernel in kernels:
            for c in C_range:
                model = SVC(kernel=kernel, C=c, random_state=12)
                model.fit(X_train, y_train)
                testPredctions = model.predict(X_valid)
                # calculate the accuracy of the model
                testPredctionsAccuracy = accuracy_score(y_valid, testPredctions)
                f1score = f1_score(y_valid, testPredctions)
                recallScore = recall_score(y_valid, testPredctions)
                print("Accuracy % on testing set : ", testPredctionsAccuracy, "kernel = ", kernel, ", c = ",c)
                print("F1 score % on testing set : ", f1score, "kernel = ", kernel, ", c = ",c)
                print("recall score % on testing set : ", recallScore, "kernel = ", kernel, ", c = ",c)
                if(testPredctionsAccuracy> bestAccuracy):
                    bestModel = model
                    bestAccuracy = testPredctionsAccuracy
                    bestC = c
                    bestTestPredctions = testPredctions

        # --------------------------
        print("Confusion Matrix :")
        confusionMatrix = confusion_matrix(y_valid, bestTestPredctions)
        print(confusionMatrix)
        seaborn.heatmap(confusionMatrix, annot=True, fmt='d')
        plt.show()
        # --------------------------
        print("The best accuracy % is : ", bestAccuracy, " with C = ",bestC)
        with open("Models/svcModel-" +str(numberOfFeatures)+ "Features.pkl", 'wb') as file:
            pickle.dump(bestModel, file)
            print('SVC model with '+ str(numberOfFeatures) +' features saved!')

    def decisionTreeModel(self, X_train, X_valid, y_train, y_valid, numberOfFeatures):
        print('Decision Tree Model Training')
        maxDepth_range = [5,6,7,8,9,10,11,12,13,14,15]
        bestAccuracy = 0
        bestModel = None
        bestMaxDepth = 0
        bestTestPredctions = []
        for d in maxDepth_range:
            model = DecisionTreeClassifier(max_depth=d)
            model.fit(X_train, y_train)
            testPredctions = model.predict(X_valid)
            # calculate the accuracy of the model
            testPredctionsAccuracy = accuracy_score(y_valid, testPredctions)
            f1score = f1_score(y_valid, testPredctions)
            recallScore = recall_score(y_valid, testPredctions)
            print("Accuracy % on testing set with maxDepth = ",d ," : ", testPredctionsAccuracy)
            print("F1 score % on testing set with maxDepth = ",d ," : ", f1score)
            print("recall score % on testing set with maxDepth = ",d ," : ", recallScore)
            if (testPredctionsAccuracy > bestAccuracy):
                bestModel = model
                bestAccuracy = testPredctionsAccuracy
                bestMaxDepth = d
                bestTestPredctions = testPredctions
        plt.figure(figsize=(9, 7))
        n_features = X_train.shape[1]
        #model.feature_importances_ will be : bestModel.feature_importances_
        plt.barh(range(n_features), bestModel.feature_importances_, align="center")
        plt.yticks(np.arange(n_features), X_train.columns)
        plt.show()
        # --------------------------
        print("Confusion Matrix :")
        confusionMatrix = confusion_matrix(y_valid, bestTestPredctions)
        print(confusionMatrix)
        seaborn.heatmap(confusionMatrix, annot=True, fmt='d')
        plt.show()
        # --------------------------
        print("The best accuracy % is : ", bestAccuracy, " with maxDepth = ", bestMaxDepth)
        with open("Models/decisionTreeModel-" +str(numberOfFeatures)+ "Features.pkl", 'wb') as file:
            pickle.dump(bestModel, file)
            print('Decision Tree model with '+ str(numberOfFeatures) +' features saved!')

    def randomForestModel(self, X_train, X_valid, y_train, y_valid, numberOfFeatures):
        print('Random Forest Model Training')
        maxDepth_range = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        bestAccuracy = 0
        bestModel = None
        bestMaxDepth = 0
        bestTestPredctions = []
        for d in maxDepth_range:
            model = RandomForestClassifier(max_depth=d)
            model.fit(X_train, y_train)
            testPredctions = model.predict(X_valid)
            # calculate the accuracy of the model
            testPredctionsAccuracy = accuracy_score(y_valid, testPredctions)
            f1score = f1_score(y_valid, testPredctions)
            recallScore = recall_score(y_valid, testPredctions)
            print("Accuracy % on testing set with maxDepth = ", d, " : ", testPredctionsAccuracy)
            print("F1 score % on testing set with maxDepth = ", d, " : ", f1score)
            print("recall score % on testing set with maxDepth = ", d, " : ", recallScore)
            if (testPredctionsAccuracy > bestAccuracy):
                bestModel = model
                bestAccuracy = testPredctionsAccuracy
                bestMaxDepth = d
                bestTestPredctions = testPredctions
        plt.figure(figsize=(9, 7))
        n_features = X_train.shape[1]
        plt.barh(range(n_features), bestModel.feature_importances_, align="center")
        plt.yticks(np.arange(n_features), X_train.columns)
        plt.show()
        #--------------------------
        print("Confusion Matrix :")
        confusionMatrix = confusion_matrix(y_valid, bestTestPredctions)
        print(confusionMatrix)
        seaborn.heatmap(confusionMatrix, annot=True, fmt='d')
        plt.show()
        # --------------------------
        print("The best accuracy % is : ", bestAccuracy, " with maxDepth = ", bestMaxDepth)
        with open("Models/randomForestModel-" +str(numberOfFeatures)+ "Features.pkl", 'wb') as file:
            pickle.dump(bestModel, file)
            print('Random Forest model with '+ str(numberOfFeatures) +' features saved!')


    def createBestModel(self, X_train, y_train, numberOfFeatures):
        print('Random Forest Model Training')
        maxDepth = 13
        model = RandomForestClassifier(max_depth=maxDepth)
        model.fit(X_train, y_train)
        plt.figure(figsize=(9, 7))
        n_features = X_train.shape[1]
        plt.barh(range(n_features), model.feature_importances_, align="center")
        plt.yticks(np.arange(n_features), X_train.columns)
        plt.show()
        with open("Models/bestModel-" + str(numberOfFeatures) + "Features.pkl", 'wb') as file:
            pickle.dump(model, file)
            print('Best Model with ' + str(numberOfFeatures) + ' features saved!')

    """def xGBoostModel(self, X_train, X_valid, y_train, y_valid, numberOfFeatures):
        print('XGBoost Model Training')
        learningRate_range = [0.3, 0.6, 0.9]
        maxDepth_range = [6, 9, 12, 15]
        bestAccuracy = 0
        bestModel = None
        bestLearningRate = 0
        bestMaxDepth = 0
        for d in maxDepth_range:
            for l in learningRate_range:
                model = XGBClassifier(learning_rate=l, max_depth=d)
                model.fit(X_train, y_train)
                testPredctions = model.predict(X_valid)
                # calculate the accuracy of the model
                testPredctionsAccuracy = accuracy_score(y_valid, testPredctions)
                print("Accuracy % on testing set : ",d," , ",l," ", testPredctionsAccuracy)
                if (testPredctionsAccuracy > bestAccuracy):
                    bestModel = model
                    bestAccuracy = testPredctionsAccuracy
                    bestLearningRate = l
                    bestMaxDepth = d
        plt.figure(figsize=(9, 7))
        n_features = X_train.shape[1]
        plt.barh(range(n_features), model.feature_importances_, align="center")
        plt.yticks(np.arange(n_features), X_train.columns)
        plt.show()
        print("The best accuracy % is : ", bestAccuracy, " with maxDepth = ",bestMaxDepth,", learningRate = ",bestLearningRate)
        with open("Models/xGBoostModel-" +str(numberOfFeatures)+ "Features.pkl", 'wb') as file:
            pickle.dump(bestModel, file)
            print('XGBoost model with '+ str(numberOfFeatures) +' features saved!')

"""
if __name__=="__main__":
    modelTraining = ModelTraining()
    """cette fonction affiche quelque information a propos de la dataset à utilisant deans l'entrainement du modèle"""
    #modelTraining.showStatistics()

    # number of Features used in the training 14 or 18 features
    numberOfFeatures = 18
    data = pd.read_csv("../DatasetPretreatment/DatasetExtractedFeatures/dataset-" +str(numberOfFeatures)+ "Features.csv")
    # Shuffle the dataset (melanger la dataset)
    data = data.sample(frac=1).reset_index(drop=True)
    # devide dataset to train and test(validation) sets
    y = data['label']
    X = data.drop('label', axis=1)
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.7, test_size=0.3, random_state=1)

    """Les fonctions suivantes lancent l'entrainment du modele en utilisant différentes algorithmes"""
    modelTraining.svcModel(X_train, X_valid, y_train, y_valid, numberOfFeatures)
    #modelTraining.decisionTreeModel(X_train, X_valid, y_train, y_valid, numberOfFeatures)
    #modelTraining.randomForestModel(X_train, X_valid, y_train, y_valid, numberOfFeatures)
    #modelTraining.xGBoostModel(X_train, X_valid, y_train, y_valid, numberOfFeatures)


    """Apres la comparaison entre les algorithmes précedentes, on choisi la meilleure, et on relance
    l'entrainement du model avec tout la dataset (et non pas avec 70%)"""
    #modelTraining.createBestModel(X, y, numberOfFeatures)
