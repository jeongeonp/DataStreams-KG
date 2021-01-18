import nltk, re, pprint
#from nltk.tokenize import word_tokenize
from urllib import request
from bs4 import BeautifulSoup
nltk.download('punkt')

def findArticles(pages):
    articleLinks = []
    for i in range(pages):
        pageNo = i
        url = "https://www.cnbc.com/transportation/?page="+str(pageNo+1)
        soup = BeautifulSoup(request.urlopen(url).read(), 'html.parser')

        count = 0
        for link in soup.find_all('a'):
            if ('https://www.cnbc.com/2020' in link.get('href') and not link.get('href') in articleLinks): 
                articleLinks.append(link.get('href'))
                count += 1
            
        
        print(count, "at page", pageNo + 1)

    counts = dict()
    for i in articleLinks:
        counts[i] = counts.get(i, 0) + 1

    print('Total article number:', len(articleLinks))
    return articleLinks


def parseArticles(articleLinkList):
    sentInArticles = []
    keypointsInArticles = []
    
    for articleLink in articleLinkList[:]:
        print("On article", articleLink)
        soup = BeautifulSoup(request.urlopen(articleLink).read(), 'html.parser')
        keyPart = soup.find_all('div', 'RenderKeyPoints-list')
        if (len(keyPart) > 0):
            keypoints = list(map(lambda x: x.text, keyPart[0].find_all('li')))
            for key in keypoints:
                keypointsInArticles.append(key)
        
        mainPart = soup.find_all('div', 'group')
        for group in mainPart:
            for paragraph in group.find_all('p'):
                for sent in nltk.tokenize.sent_tokenize(paragraph.text):
                    sentInArticles.append(sent)
        
    return keypointsInArticles, sentInArticles

articleLinkList = findArticles(1)
keypointList, sentList = parseArticles(articleLinkList)

for i in sentList+keypointList:
    print ("-", i)

print(len(sentList))