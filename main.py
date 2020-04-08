#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 14:18:04 2020

Bioinformatics and Systems Biology Group
Institute for Genetics
National University of Colombia

Please see contributors on GitHub
"""

import matplotlib.dates as mdates
import pandas as pd
import requests
from funciones import plotme, percentage

#Teniendo en cuenta que la informacion del Covid-19 se encuentra en la web, se referencia la data para que esta este actualizada
url="https://e.infogram.com/api/live/flex/bc384047-e71c-47d9-b606-1eb6a29962e3/664bc407-2569-4ab8-b7fb-9deb668ddb7a?"

#Debido a que la información no proviene de un formato dado, es necesario definirla como texto y aprovechar
#que esta viene en formato py, por ende se evalua ese texto
s=eval(requests.get(url).text)

#Se seleccionan unicamente el dataframe del historico y se define como dataframe
data=s["data"][0]
df = pd.DataFrame(data=data[1:], columns=data[0])

#df = pd.read_csv('insdata.csv')
f = df[['Fecha de diagnóstico']].drop_duplicates()
#print(f[['Fecha de diagnóstico']])
#Parece ser q iterar un dataframe de pandas no es buena idea. Convertir mejor a lista
#https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
ff = f.values.tolist()

#Definir listas para usar más abajo
allRel=[]
allImp=[]
allEst=[]
allCasos=[]
myFechas=[]

for row in ff:
    r = row[0]
    #Pandas y SQL:https://pandas.pydata.org/pandas-docs/stable/getting_started/comparison/comparison_with_sql.html

 
    rel = df[(df['Tipo*'] == 'Relacionado') & (df['Fecha de diagnóstico'] == r)].count()
    allRel.append(rel[0])
    
    imp = df[(df['Tipo*'] == 'Importado') & (df['Fecha de diagnóstico'] == r)].count()
    allImp.append(imp[0])
    
    est = df[(df['Tipo*'] == 'En estudio') & (df['Fecha de diagnóstico'] == r)].count()
    allEst.append(est[0])
    
    casos = df[(df['Fecha de diagnóstico'] == r)].count()
    allCasos.append(casos[0])
    
    myFechas.append(r)
    

#---------- DATOS BASICOS ----------
    
print ("----------------") 

c = sum(allCasos)
i = sum(allImp)
e = sum(allEst)
r = sum(allRel)
print('Casos Totales:     ' + str(c))
print('Casos Importados:  ' + str(i) + "(" + str(percentage(i,c)) + "%)")  
print('Casos Relacionados:' + str(r) + "(" + str(percentage(r,c)) + "%)")
print('Casos en Estudio:  ' + str(e) + "(" + str(percentage(e,c)) + "%)")





#--------------  RELACIONADOS - IMPORTADOS - EN ESTUDIO ------------------------ 
# PLOTEAR 
plot2Ydata=[]
plot2Ydata.append(allImp)
plot2Ydata.append(allRel)
plot2Ydata.append(allEst)
plot2Labels = ["Importados","Relacionados","En Estudio"]
plot2Title = "Importados, Relacionados y En Estudio por Fecha"

plotme(myFechas,plot2Ydata,plot2Labels,plot2Title)



#--------------  ACUMULADO E INCREMENTO POR FECHA -------------------- 
acum = []
inc = []

#Esta append es necesario porun error de "index out of range"
#https://www.stechies.com/indexerror-list-assignment-index-out-range/
inc.append(1)
acum.append(1)

for i in range(1,len(allCasos)):
    
    #Acumulado es igual a los casos de hoy mas los acumulados hasta ayer.
    v = allCasos[i] + acum[i-1]
    acum.append(v) 
    
    #Incremento es igual  los casos de hoy menos los casos de ayer.
    x = allCasos[i] - allCasos[i-1]
    inc.append(x)

# PLOTEAR 
fig1Ydata=[]
fig1Ydata.append(acum)
fig1Ydata.append(inc)
fig1Ydata.append(allCasos)
fig1labels = ["Acumulado","Incremento", "Casos Diarios"]
fig1Title =  "Acumulado, Incremento y Casos por fecha"

plotme(myFechas, fig1Ydata,fig1labels, fig1Title)


#--------------  MODELO SIR -------------------- 

# Clasificacion por Atencion en fechas
EstadosFecha = df.groupby(['Fecha de diagnóstico', 'Atención**'], sort=False)['ID de caso'].count()

# poblacion colombiana
N = 49070000 # 49,07 millones

# infectados y recuperados
Infectados = []
Recuperados = []
Fechas = []

Recuperados.append(1)
Infectados.append(1)
Fechas.append('')
Rec = 0
Inf = 0
for items in EstadosFecha.iteritems():
    if Fechas[-1] != items[0][0]:
        Fechas.append(items[0][0])
        Recuperados.append(Rec)
        Infectados.append(Inf)
        
        Inf = 0
        Rec = 0
    Tipo = items[0][1]
    if Tipo == 'Casa' or Tipo == 'Hospital' or Tipo == 'Hospital UCI':
        Inf = Inf + items[1]
    elif Tipo == 'Recuperado' or Tipo == 'Fallecido':
        Rec = Rec + items[1]


# PLOTEAR 
fig1Ydata=[]
fig1Ydata.append(Recuperados)
fig1Ydata.append(Infectados)
fig1labels = ["Recuperados","Infectados"]
fig1Title =  "Recuperados vs Infectados por Fecha"

plotme(Fechas, fig1Ydata,fig1labels, fig1Title)
