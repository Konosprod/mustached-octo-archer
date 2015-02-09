#!/usr/bin/python3.3

from bs4 import BeautifulSoup
import urllib.request
import sys

rem_file = ""

#Fonction qui permet d'afficher la progression du téléchargement
def dlProgress(count, blockSize, totalSize):
    global rem_file
    percent = int(count*blockSize*100/totalSize)
    sys.stdout.write("\r" + rem_file + " ...%d%%" % percent)
    sys.stdout.flush()

#Fonction qui récupère le nom de la video et ajoute mp4 à la fin
def getName(html):
    name = html.find('meta', attrs={'property' : 'og:title', 'content' : True})
    return name['content']+".mp4"

#Fonction qui permet de télécharger la video
def downloadVideo(url):
    global rem_file

    #Recupere le code source de la page
    html = getSource(url)
    
    #Permet de trouver toutes les occurences de la balise 
    #<meta property='og:video:url' qui a un champ content
    urlVideo = html.findAll('meta', attrs={'property': 'og:video:url', 'content': True})
    
    if len(sys.argv) == 3:
        rem_file = sys.argv[2]
    else:
        rem_file = getName(html)
    
    #Telecharge la video
    urllib.request.urlretrieve(urlVideo[1]['content'], rem_file, reporthook=dlProgress)
    print("\nDone")


#Fonction qui permet de récupérer le code source d'une page internet
def getSource(url):
    reponse = urllib.request.urlopen(url)
    pageSource = reponse.read()
   
    return BeautifulSoup(pageSource.decode("utf8"))
    
    
#Affichagede l'aide d'utilisation    
def printHelp():
    print("usage : " + sys.argv[0] + " [url]")
    print("        " + sys.argv[0] + " [url] [filename]")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        printHelp()
    else:
        downloadVideo(sys.argv[1])
    
