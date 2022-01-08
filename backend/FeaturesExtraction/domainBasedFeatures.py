import math
import urllib.request
import urllib
from urllib.parse import urlparse

import pandas as pd
from bs4 import BeautifulSoup
import whois
import re
from datetime import datetime

class DomainBasedFeatures():

    #extract all the 4 features ( Domain based Features)
    def extractFeatures(self, url):
        domainName = ""
        try:
            domainName = whois.whois(urlparse(url).netloc)
        except:
            domainName = ""
        result =[]
        result.append(self.hasDNSRecord(domainName))
        result.append(self.getWebTraffic(url))
        result.append(self.getDomainAge(domainName))
        result.append(self.getDomainEnd(domainName))
        return result


    #feature 1
    def hasDNSRecord(self, domainName):
        # return 1 if the domain name is found
        # return 0 if the domain name is not found
        if domainName == "":
            return 0
        else:
            return 1

    #feature 2
    def getWebTraffic(self, url):
        # return 1 if url the rank of domain < 100.000
        # return 0 if url the rank of domain >= 100.000 (phishing)

        try:
            url = urllib.parse.quote(url)
            rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), features="html.parser").find("reach")["rank"]
            rank = int(rank)
        except TypeError:
            return 0
        return rank
        """if rank >= 10000:
            return 0
        else:
            return 1"""

    #feature 3
    def getDomainAge(self, domainName):
        # return 1 if url the domain age > 6 months - safe
        # return 0 if url the domain age < 6 months - phishing
        if(domainName==""):
            return 0
        else:
            creationDate = domainName.creation_date
            expirationDate = domainName.expiration_date
            if(isinstance(creationDate, str)) or isinstance(expirationDate, str):
                try:
                    format = "%Y-%m-%d"
                    creationDate = datetime.strptime(creationDate, format)
                    expirationDate = datetime.strptime(expirationDate, format)
                    print("creation :", creationDate)
                    print("expiration :", expirationDate)
                except:
                    return 0
            if (creationDate is None) or (expirationDate is None):
                return 0
            elif (type(expirationDate) is list) or (type(creationDate) is list):
                return 0
            else:
                domainAge = abs((expirationDate - creationDate).days)
                return round(domainAge/30, 2)
                """if(domainAge/30) > 150:
                    return 1
                else:
                    return 0"""

    #feature 4
    def getDomainEnd(self, domainName):
        # return nbr if url the domain end time > 6 months safe
        # return 0 if url the domain end time < 6 months phishing
        if (domainName == ""):
            return 0
        else:
            expirationDate = domainName.expiration_date
            if (isinstance(expirationDate, str)):
                try:
                    format = "%Y-%m-%d"
                    expirationDate = datetime.strptime(expirationDate,format )
                except:
                    return 0
            if(expirationDate is None):
                return 0
            elif (type(expirationDate) is list):
                return 0
            else:
                todayDate = datetime.now()
                domainEnd = abs((expirationDate - todayDate).days)
                return round(domainEnd/30, 2)
                """if (domainEnd/30) < 6:
                    return 1
                else:
                    return 0"""

if __name__== "__main__":
    domaineBasedFeatures = DomainBasedFeatures()

    url = 'https://www.facebook.com'
    #url = 'http://www.Confirme-paypal.com/'
    domainName = ""
    try:
        domainName = whois.whois(urlparse(url).netloc)
    except:
        domainName = ""
    dns = domaineBasedFeatures.hasDNSRecord(domainName)
    print("DNS found ? : ", dns)
    traffic = domaineBasedFeatures.getWebTraffic(url)
    print("web traffic: ", traffic)
    domainAge = domaineBasedFeatures.getDomainAge(domainName)
    print("domain age < 6 months: ", domainAge)
    domainEnd = domaineBasedFeatures.getDomainEnd(domainName)
    print("domain end time > 6 months: ", domainEnd)

    result = domaineBasedFeatures.extractFeatures(url)
    print('Domain based features : ', result)

