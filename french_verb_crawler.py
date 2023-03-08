import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import logging

list_of_verbs = ['avoir']
#                 , 'etre', 'venir', 'aller', 'parler', 'faire'
#, 'prendre', 'vouloir', 'savoir', 'pouvoir', 'dire', 'interdire', 'donner', 'penser'
#, 'aider', 'aimer', 'devoir', 'habiter', 'regarder', 'utiliser', 'essayer'
#, 'acheter', 'asseoir', 'ecrire', 'boire', 'comprendre', 'connaître', 'convaincre'
#, 'courir', 'croire', 'envoyer', 'falloir', 'lire', 'manger', 'mettre', 'recevoir', 'rire'
#, 'suivre', 'tenir', 'voir', 'vivre', 'trouver', 'passer', 'demander', 'conclure', 'construire'
#, 'porter', 'montrer', 'commencer', 'compter', 'entendre', 'attendre', 'appeler', 'permettre'
#, 'partir', 'décider', 'arriver', 'répondre', 'accepter', 'jouer', 'choisir', 'toucher', 'perdre'
#, 'ouvrir', 'exister', 'gagner', 'travailler', 'risquer', 'apprendre', 'entrer', 'atteindre'
#, 'produire', 'préparer', 'écrire', 'créer', 'courir', 'contenir', 'couvrir', 'décevoir', 'sentir'
#, 'suffire', 'servir', 'rompre', 'prédire', 'pourvoir', 'plaire', 'placer', 'payer', 'naître'
#, 'mourir', 'lever', 'lancer', 'joindre', 'jeter', 'craindre', 'conduire', 'bouillir', 'battre'
#, 'apprécier', 'extraire', 'sortir', 'sourir', 'preferer', 'changer'] 
list_of_urls = []
appended_data = []
print('Retrieving '+str(len(list_of_verbs))+' verb conjugations.')

def count_nested_list(l):
    return sum(isinstance(i, list) for i in l)

def flatten(l):
    return [item for sublist in l for item in sublist]

for verb in list_of_verbs:
    link = f'https://konjugator.reverso.net/konjugation-franzosisch-verb-{verb}.html'
    list_of_urls.append(link)
    print('Number of urls: '+str(len(list_of_urls)))

 
for url in list_of_urls:
    page = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
    doc = BeautifulSoup(page.text, "html.parser")

    temps = doc.find_all('div', class_='blue-box-wrap') #all temps in this wrapper
    #infinitif = doc.find_all('div', class_='verb-forms-wrap')
    #print(temps)

    #print(temps[0]['mobile-title'])
    # print(temps[0]['graytxt'])
    # print(temps[0].text)

    temp_name = []
    pre = {}
    result = {}

    for index, temp in enumerate(temps):
        #titles = temps[index].find('p').string
        title = temps[index]['mobile-title']
        temp_name.append(title)
        verbs = temps[index].find_all('i', class_='verbtxt')
        pronouns = temps[index].find_all('i', class_='graytxt')
        if title not in pre:
            pre[title] = [pronouns[index].text for index, pronoun in enumerate(pronouns)]
            pre[title].append([verbs[index].text for index, verb in enumerate(verbs)])
        #print(pre)
                
    for key, value in pre.items():
        if len(value) != 1: #captures all cases where we have pronouns for each verbform of the temp
            result[key] = [str(value[i])+str(value[-1][i]) for i in range (len(value)-1)] #-1 because the -1 element is the nested list
        else:
            result[key] = flatten(value)[-6:] #sometimes there are 2x6 conjugated verb forms with slightly different writing. We keep the last six.

    #print(result)

    df = pd.DataFrame.from_dict(result,orient='index').transpose()
    appended_data.append(df) #list of dataframes
    
appended_data = pd.concat(appended_data)
print(appended_data)

appended_data.to_excel('french_verbs_v4.xlsx', index=False)

