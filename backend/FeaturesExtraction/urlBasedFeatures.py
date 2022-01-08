from urllib.parse import urlparse, urlencode
import ipaddress
import re
from matplotlib import pyplot as plt
import pandas as pd


class UrlBasedFeatures():

    def __init__(self):
        self.shorteningServices = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                              r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                              r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                              r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                              r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                              r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                              r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                              r"tr\.im|link\.zip\.net"

    #extract all the 14 features ( URL based Features)
    def extractFeatures(self, url):
        result =[]
        result.append(self.getDomainFeature(url))
        result.append(self.hasIpAddress(result[0]))
        result.append(self.hasAtSymbol(url))
        result.append(self.isLong(url))
        result.append(self.getDepth(url))
        result.append(self.hasPointInDomain(result[0]))
        result.append(self.hasNumberInDomain(result[0]))
        result.append(self.isShortend(url))
        result.append(self.getUrlLength(url))
        result.append(self.getDashNumber(url))
        result.append(self.getUnderlineNumber(url))
        result.append(self.getQuestionMarkNumber(url))
        result.append(self.getAndNumber(url))
        result.append(self.getPointNumber(url))
        result.append(self.getDomainLength(result[0]))

        #return features exect the domain name cause we don't need it
        return result[1:]


    #feature 1
    def getDomainFeature(self, url):
        domain = urlparse(url).netloc
        if re.match(r"^www.",domain):
            domain = domain.replace("www.", "")
        return domain

    #feature 2
    def hasIpAddress(self, domain):
        #return 1 if domain is ip address
        #return 0 if domain is not has ip address
        ip = 0
        try:
            ipaddress.ip_address(domain)
            ip = 1
        except:
            ip = 0
        return ip

    #feature 3
    def hasAtSymbol(self, url):
        # return 1 if url has @ symbol
        # return 0 if url don't has @ symbol
        if '@' in url:
            return 1
        else:
            return 0

    #feature 4
    def isLong(self, url):
        # return 1 if url length > 80
        # return 0 if url length <= 80
        if len(url) > 80:
            return 0
        else:
            return 1

    #feature 5
    def getDepth(self, url):
        #return the number of '/'
        depth = 0
        temp = urlparse(url).path.split('/')
        for i in range(len(temp)):
            if(len(temp[i])!=0):
                depth = depth + 1
        return depth

    #feature 6
    def hasPointInDomain(self, domain):
        #return 1 if domain contient 2 points ou plus, else return 0
        cpt = 0
        for c in domain:
            if c == '.':
                cpt += 1
        if cpt >= 2:
            return 1
        else:
            return 0

    #feature 7
    def hasNumberInDomain(self, domain):
        # return 1 if url has a number
        # return 0 if url hasn't a number
        for c in domain:
            if c.isdigit():
                return 1
        return 0

    #feature 8
    def isShortend(self, url):
        # return 1 if url is shortned by a service
        # return 0 if url is not shortned by a service
        temp = re.search(self.shorteningServices, url)
        if temp:
            return 1
        else:
            return 0

    # feature 9
    def getUrlLength(self, url):
        return len(url)

    #feature 10
    def getDashNumber(self, url):
        cpt = 0
        for c in url:
            if c == '-':
                cpt += 1
        return cpt

    # feature 11
    def getUnderlineNumber(self, url):
        cpt = 0
        for c in url:
            if c == '_':
                cpt += 1
        return cpt

    # feature 12
    def getQuestionMarkNumber(self, url):
        cpt = 0
        for c in url:
            if c == '?':
                cpt += 1
        return cpt

    # feature 13
    def getAndNumber(self, url):
        cpt = 0
        for c in url:
            if c == '&':
                cpt += 1
        return cpt

    # feature 14
    def getPointNumber(self, url):
        cpt = 0
        for c in url:
            if c == '.':
                cpt += 1
        return cpt

    # feature 15
    def getDomainLength(self, domain):
        return len(domain)



if __name__== "__main__":
    urlBasedFeatures = UrlBasedFeatures()
    """data = pd.read_csv('../DatasetPretreatment/DatasetCleaned/dataset.csv')
    temp = set()
    som = 0
    cpt = 0
    for i in range(data.shape[0]):
        url = data['url'][i]
        a = urlBasedFeatures.isLong(url)
        print(i, " length : ", a)
        label = data['label'][i]
        if a >80 and label == 1:
            cpt += 1
        som += a
        temp.add(a)

    print("the avg length is : ", som/data.shape[0])
    print("number url > 100 is : ", cpt)
    print(list(temp))
    temp = dict.fromkeys(list(temp), 0)
    for i in range(data.shape[0]):
        url = data['url'][i]
        a = urlBasedFeatures.isLong(url)
        temp[a] += 1

    plt.plot(temp.values())
    plt.show()"""
    url = 'http://www.facebook.com/fake.html'
    #url = 'http://ww38.xieziet.do22.co/track.php'
    d = urlBasedFeatures.getDomainFeature(url)
    print("the domain: ", d)
    ip = urlBasedFeatures.hasIpAddress(d)
    print("has ip address ? : ", ip)
    atSymbol = urlBasedFeatures.hasAtSymbol(url)
    print("has @ symbol ? : ", atSymbol)
    isLong = urlBasedFeatures.isLong(url)
    print("is long ? : ", isLong)
    depth = urlBasedFeatures.getDepth(url)
    print("Depth ? : ", depth)
    point = urlBasedFeatures.hasPointInDomain(url)
    print("has Point In Domain ? : ", point)
    num = urlBasedFeatures.hasNumberInDomain(d)
    print("has number in domain ? : ", num)
    shortned = urlBasedFeatures.isShortend(url)
    print("is shortned ? : ", shortned)

    result = urlBasedFeatures.extractFeatures(url)
    print('URL based features : ',result)
    print('Number of features : ', result.__len__())
