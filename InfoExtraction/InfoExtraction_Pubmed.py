import nltk, re, pprint
from nltk.tokenize import word_tokenize
from urllib import request
from bs4 import BeautifulSoup
#import pandas as pd
import random


def findPapers(keyword, startYear, number):
    print("### Start searching with [" + keyword + "]")
    paperList = []

    author = []
    journal = []
    pmid = []
    title = []

    # Looks for the first 30 paper results 

    for i in range(number):
        url = "https://pubmed.ncbi.nlm.nih.gov/?term="+keyword+"&filter=simsearch1.fha&filter=years."+startYear+"-2020&page="+str(i+1)
        soup = BeautifulSoup(request.urlopen(url).read(), 'html.parser')
        #print(soup.text)
        author = author + (soup.find_all('span', 'docsum-authors short-authors'))
        journal = journal + (soup.find_all('span', 'docsum-journal-citation full-journal-citation'))
        pmid = pmid + (soup.find_all('span', 'docsum-pmid'))
        title = title + (soup.find_all('a', 'docsum-title'))

        print(len(author))

    cnt = 0
    
    # Goes through the 30 papers and looks for the paper information: PMID, year, title, author, and journal
    for i in range(len(author)):

        currPmid = pmid[i].text.strip()
        currYear = (journal[i].text.strip()[journal[i].text.strip().find(".")+2:journal[i].text.strip().find(".")+6])
        currTitle = title[i].text.strip()
        if "et al" in author[i].text.strip():
            currAuthor = (author[i].text.strip()[:-8])
        else:
            currAuthor = (author[i].text.strip()[:-1])
        currJournal = (journal[i].text.strip()[:journal[i].text.strip().find(".")])

        if (not currPmid in str(paperList)):
            paperList.append([currPmid, currYear, currTitle, currAuthor, currJournal])
            cnt += 1
                    
    print("Total number of papers with the keyword [" + keyword + "] :" , cnt)
    print("")
    

    return paperList


def sentParsing(paperList):
    # To store sentences with the five categories of verbs
    abstractList = []

    authorList = {}
    journalList = {}

    papercnt = 0

    print("Input number of papers: ", len(paperList))

    # Goes through all the papers found
    for paper in paperList:
        print("On paper #", papercnt)

        # Puts the author (organization) and journal name into each dictionary created
        if paper[3] in authorList:
            authorList[paper[3]] = authorList[paper[3]] + 1
        else:
            authorList[paper[3]] = 1

        if paper[4] in journalList:
            journalList[paper[4]] = journalList[paper[4]] + 1
        else:
            journalList[paper[4]] = 1


        papercnt += 1
        url = "https://pubmed.ncbi.nlm.nih.gov/"+paper[0]
        soup = BeautifulSoup(request.urlopen(url).read(), 'html.parser')
        abstract = (soup.find_all('div', {'class': 'abstract-content selected'}))
        abstract_all = (soup.find_all('div', {'class': 'abstract'}))
        keywords = abstract_all[0].text.split("Keywords:")[1] if len(abstract_all[0].text.split("Keywords:"))>1 else "NO KEYWORDS"
        #print(keywords)

        #print(abstract[0].text.strip())
        print()
        abstractList.append({"title": paper[2], "keywords": keywords.rstrip(), "abstract": abstract[0].text.strip().rstrip()})

    print("Output number of papers: ", papercnt)
    return abstractList









paperList = []
paperList = paperList + findPapers("medical", "2014", 1)


print(paperList)
print(len(paperList))

print(sentParsing(paperList))