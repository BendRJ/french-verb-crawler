import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

list_of_verbs = ['avoir'
, 'etre', 'venir', 'aller', 'parler', 'faire'
, 'prendre', 'vouloir', 'savoir', 'pouvoir', 'dire', 'interdire', 'donner', 'penser'
, 'aider', 'aimer', 'devoir', 'habiter', 'regarder', 'utiliser', 'essayer'
, 'acheter', 'asseoir', 'ecrire', 'boire', 'comprendre', 'connaître', 'convaincre'
, 'courir', 'croire', 'envoyer', 'lire', 'manger', 'mettre', 'recevoir', 'rire'
, 'suivre', 'tenir', 'voir', 'vivre', 'trouver', 'passer', 'demander', 'conclure', 'construire'
, 'porter', 'montrer', 'commencer', 'compter', 'entendre', 'attendre', 'appeler', 'permettre'
, 'partir', 'décider', 'arriver', 'répondre', 'accepter', 'jouer', 'choisir', 'toucher', 'perdre'
, 'ouvrir', 'exister', 'gagner', 'travailler', 'risquer', 'apprendre', 'entrer', 'atteindre'
, 'produire', 'préparer', 'écrire', 'créer', 'courir', 'contenir', 'couvrir', 'décevoir', 'sentir'
, 'suffire', 'servir', 'rompre', 'prédire', 'pourvoir', 'plaire', 'placer', 'payer', 'naître'
, 'mourir', 'lever', 'lancer', 'joindre', 'jeter', 'craindre', 'conduire', 'bouillir', 'battre'
, 'apprécier', 'extraire', 'sortir', 'sourir', 'preferer', 'changer'] 

list_of_urls = []
appended_data = []

print('Retrieving '+str(len(list_of_verbs))+' verb conjugations.')

start_time = datetime.now()

def flatten(l):
    return [item for sublist in l for item in sublist]

for verb in list_of_verbs:
    time.sleep(2)
    print(f"Loading -{verb}- now...")
    url = f'https://konjugator.reverso.net/konjugation-franzosisch-verb-{verb}.html'

    page = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
    doc = BeautifulSoup(page.text, "html.parser")
    temps = doc.find_all('div', class_='blue-box-wrap') #all temps in this wrapper

    pre = {}

    for index, temp in enumerate(temps):
        title = temps[index]['mobile-title']

        particles = temps[index].find_all('i', class_='particletxt')
        pronouns = temps[index].find_all('i', class_='graytxt')
        verbs_aux = temps[index].find_all('i', class_='auxgraytxt')
        verbs = temps[index].find_all('i', class_='verbtxt')

        if title not in pre:  
            pre[title] = [[particle.text for particle in particles]]
            pre[title].append([pronoun.text for pronoun in pronouns])
            pre[title].append([verb_aux.text for verb_aux in verbs_aux])
            pre[title].append([verb.text for verb in verbs])

    dict_without_empty_lists = {
    key: [lst for lst in value if lst] for key, value in pre.items() if value #checks for empty values and empty lists in values
    }
    
    result = {key: ["".join(x) for x in zip(*value)][:6] for key, value in dict_without_empty_lists.items()} #x is a tuple created from zip
    #[:6] indexing used to remove the additional writing variants for some verbs
    df = pd.DataFrame.from_dict(result,orient='index').transpose()
    appended_data.append(df) #list of dataframes
    
appended_data = pd.concat(appended_data)
print(appended_data.head())

current_timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
filename = f"french_verbs_{current_timestamp}.xlsx"
appended_data.to_excel(filename, index=False)

end_time = datetime.now()
delta = end_time - start_time
duration = delta.total_seconds() / 60
print(f"Crawl done after {duration} minutes.")