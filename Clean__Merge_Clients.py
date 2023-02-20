import pandas as pd
import datetime as dt
from statistics import mean
import matplotlib.pyplot as plt
import seaborn as sns
#import plotly.express as px
import numpy as np
from datetime import timedelta
import plotly.express as px
import re
#import seaborn as sns
import Fonctions_utiles as fct
import warnings
warnings.filterwarnings('ignore')
from pandas.core.computation.pytables import Timestamp
from datetime import date
from datetime import datetime


#################################################################################### CLIENTS / NETTOYAGE / RECUPERATION DATE DE CREATION POUR Y2 ###############################################################

client_torpedo = pd.read_csv(r"C:\Users\VO2GROUP\Documents\PACIFIC PECHE\CODE\DONNEES\clients Torpedo.txt",sep='|')
Y2_clients = pd.read_csv(r"C:\Users\VO2GROUP\Documents\PACIFIC PECHE\CODE\DONNEES\clients_Y2.csv",index_col=[0])

# client_torpedo = client_torpedo.iloc[:2000]
# Y2_clients = Y2_clients.iloc[:2000]

Y2_clients.drop_duplicates(inplace=True)
client_torpedo.drop_duplicates(inplace=True)

for i,j in enumerate(Y2_clients['T_TIERS']):
        compt = 0
        if len(str(j)) > 20:
            for c in Y2_clients.columns:
                    Y2_clients[c].iloc[i] = j.split('|')[compt]
                    compt += 1


client_torpedo['Prénom'] = client_torpedo['Prénom'].apply(lambda x : str(x).lower().capitalize())
client_torpedo['Nom_Prenom'] = client_torpedo.Nom +' '+client_torpedo.Prénom
Y2_clients['Nom_Prenom'] = Y2_clients.T_LIBELLE +' '+Y2_clients.T_PRENOM

######################################  CLIENTS UNIQUE ET DOUBLONS ID CLIENT ############################################################


client_unique = client_torpedo.groupby('Nom_Prenom')[['ID Client']].count().sort_values(by='ID Client',ascending=False)
client_unique.reset_index(inplace=True)
client_unique = client_unique[client_unique['ID Client']>= 2]
client_unique.to_excel('client_unique_torpedo.xlsx')

client_unique_Y2 = Y2_clients.groupby('Nom_Prenom')[['T_TIERS']].count().sort_values(by='T_TIERS',ascending=False)
client_unique_Y2.reset_index(inplace=True)
client_unique_Y2 = client_unique_Y2[client_unique_Y2['T_TIERS']>= 2]
client_unique_Y2.to_excel('client_unique_Y2.xlsx')

Client_TEST = client_torpedo[client_torpedo['ID Client'].str.contains('TEST',na=False)]
Client_TEST.to_excel('Client_TEST.xlsx')
########################################################################################################################################


client_torpedo['Date création'] = pd.to_datetime(client_torpedo['Date création'],dayfirst=True)


Y2_clients['T_ANNEENAISSANCE']=Y2_clients['T_ANNEENAISSANCE'].replace(np.nan,0)
Y2_clients['T_ANNEENAISSANCE'] = Y2_clients['T_ANNEENAISSANCE'].apply(lambda x: int(x))
Y2_clients['T_AGE'] = 2023 - Y2_clients['T_ANNEENAISSANCE']
for i,j in enumerate(Y2_clients['T_AGE']):
    if j > 100:
        Y2_clients['T_AGE'][i] = np.nan

Y2_clients.drop(columns=['T_JOURNAISSANCE','T_MOISNAISSANCE','T_ANNEENAISSANCE'],inplace=True)
Y2_clients['T_SEXE'].replace('M','Male',inplace=True)
Y2_clients['T_SEXE'].replace('F','Female',inplace=True)
li=[]
for index, element in enumerate(client_torpedo['Nom_Prenom']):
    if element in Y2_clients.Nom_Prenom.tolist():
        li.append([element,client_torpedo['ID Client'][index],client_torpedo['Date création'][index]])
Y2_clients['DATE_CREATION'] = ''
Y2_clients['ID_torpedo'] = 'aucun'
Y2_clients['ID_Y2'] = Y2_clients['T_TIERS']
Y2_clients['T_TIERS']= Y2_clients['T_TIERS'].apply(lambda x: str(x).lstrip('0'))
for cle in li:
    for index,element in enumerate(Y2_clients['Nom_Prenom']):
        if cle[1] == int(Y2_clients.T_TIERS[index]):
            Y2_clients['DATE_CREATION'][index] = cle[2]
            Y2_clients['ID_torpedo'][index] = cle[1]
Y2_clients['DATE_CREATION'] = pd.to_datetime(Y2_clients['DATE_CREATION'],dayfirst=True)
Y2_clients.to_csv('Y2_clients.csv')
#############################################################################################################################################################################################