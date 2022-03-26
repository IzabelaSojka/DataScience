import pandas as pd
import numpy as np
from datetime import datetime
df=pd.read_csv(r"C:\Users\sojka\Desktop\WAT\SemestrV\PwJF\LAB0\venv\results.csv",parse_dates=["date"])

#Zadanie 1
#Liczba wszystkich meczów rozegranych przez podaną drużynę w rozdzielczości rocznej.

def zadanie1(team):
    table=df.copy()
    table['date']=pd.DatetimeIndex(table['date']).year
    wynik1=table[(table['home_team']==team)|(table['away_team']==team)]
    wynik1=wynik1.groupby(['date']).size()
    print("Zadanie 1:\nLiczba meczy rozegrana przez:",team)
    print(wynik1)

#Zadanie 2
#Łączna liczba meczów rozegranych, wygranych, przegranych oraz zremisowanych przez podaną drużynę lub podane drużyny między sobą.
#W przypadku podania dwóch drużyn liczby meczów wygranych i przegranych dotyczą pierwszej z podanych drużyn we wszystkich meczach
# rozegranych pomiędzy obiema drużynami

def zadanie2(team, team2=''):
    table=df.copy()
    if team2=='':
        table1=table[(table['home_team']==team)|(table['away_team']==team)]
    else:
        table1=table[((table['home_team']==team)&(table['away_team']==team2))|((table['home_team']==team2)&(table['away_team']==team))]
    wynik2=table1.copy()
    wynik2['results']=np.where(table1['home_team']==team,np.where(table1['home_score']>table1['away_score'],2,np.where(table1['home_score']<table1['away_score'],0,1)),np.where(table1['away_team']==team,np.where(table1['home_score']<table1['away_score'],2,np.where(table1['home_score']>table1['away_score'],0,1)),0))
    print("\nZadanie 2:",team," ",team2,"\nRozegrane:   ",table1['home_team'].count())
    print("Wygrane:     ",wynik2[wynik2['results']==2]['results'].count())
    print("Przegrane:   ",wynik2[wynik2['results']==0]['results'].count())
    print("Zremisowane: ",wynik2[wynik2['results']==1]['results'].count())

#Zadanie 3
#Łączna liczba bramek zdobytych przez podaną drużynę oraz średniej liczby bramek na mecz zdobytych przez podaną drużynę,
#oraz bilans bramkowy podanej drużyny opcjonalnie w rywalizacji z inną podaną drużyną.

def zadanie3(team,team2=''):
    table=df.copy()
    if team2 == '':
        table1=table[(table['home_team']==team)|(table['away_team']==team)]
    else:
        table1=table[((table['home_team']==team)&(table['away_team']==team2))|((table['home_team']==team2)&(table['away_team']==team))]
    wynik3=table1.copy()
    wynik3['zdobyte']=np.where(table1['home_team']==team,table1['home_score'],table1['away_score'])
    wynik3['stracone']=np.where(table1['away_team']==team,table1['home_score'],table1['away_score'])
    print('\nZadanie 3: ',team,'\nZdobyte bramki: ',wynik3['zdobyte'].sum())
    print('Średnia liczba bramek na mecz: ',round(wynik3['zdobyte'].sum()/wynik3['home_team'].count(),3))
    print('Bilans: ',wynik3['zdobyte'].sum()," : ",wynik3['stracone'].sum())

#Zadanie 4
#Dziesięciu drużyn z największą średnią wartością punktów wraz z wartością tej średniej opcjonalnie według stanu na podany dzień.
#Punkty do meczów przyznawane są według klasycznej reguły: wygrany mecz: 3 pkt., zremisowany mecz: 1 pkt., przegrany mecz 0 pkt.

def zadanie4(date=''):
    if date!='':
        tabx=df[df['date']<=date]
    else:
        tabx=df.copy()
        date=datetime.now()
    tab2=tabx.copy()
    tab3=tabx.copy()
    tab2['Punkty']=np.where(tab2['home_score']>tab2['away_score'],3,np.where(tab2['home_score']==tab2['away_score'],1,0))
    tab3['Punkty']=np.where(tab3['home_score']>tab3['away_score'],0,np.where(tab3['home_score']==tab3['away_score'],1,3))
    tab2.drop(['date','away_team','home_score','away_score','tournament','city','country','neutral'],axis=1,inplace=True)
    tab3.drop(['date','home_team','home_score','away_score','tournament','city','country','neutral'],axis=1,inplace=True)
    tab2=tab2.rename(columns={'home_team':'Drużyna'})
    tab3=tab3.rename(columns={'away_team':'Drużyna'})
    tab4=pd.concat([tab2, tab3], axis=0, ignore_index=True)
    wynik4=tab4.groupby('Drużyna')['Punkty'].mean()
    wynik4=wynik4.reset_index()
    wynik4=wynik4.sort_values(['Punkty'],ascending=False)
    print('\nZadanie 4:\n10 drużyn z największą średnią wartością punktów na dzień: ',date,'\n',wynik4.head(10))

#zadanie1('Germany')
#zadanie2('Poland','England')
#zadanie3('Austria','Hungary')
#zadanie4('1998/09/23')

