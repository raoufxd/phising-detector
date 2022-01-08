# phishing-detector
This web application let the user know if a random url is a phishing url or legitimate url.
This project is devided to main parts:
- The frontend: the frontend is created using the framework ReactJS, and Ant Design for the ui components.
- The backend: the backend is programmed using Python.

 To implement our solution we followed the following steps:

1- Collect the dataset that we need from different sources.
2- We have applied some pretretments to the collected data like (cleaning the data, cheking the urls in the dataset if they are reel...etc.)
3- When the dataset is pretreted, we extract the features frol the dataset like ( url reach, url lenght, domain length, number of dashes in domain....etc.)
4- After we extract our features, we can pass to model training phase. For that we have used different algorithms like (Decision Tree, Random Forest, SVC...etc.)
5- After we test different models, we chooses the best model who gives the better accuracy.
6- The last step is to make our model accessible from the frontend by creating a server using flask library in python.
