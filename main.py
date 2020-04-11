#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 14:18:04 2020

Bioinformatics and Systems Biology Group
Institute for Genetics
National University of Colombia

Please see contributors on GitHub
"""
import plotly.offline as pyo
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
#df = pd.read_csv('insdata.csv')
df = pd.DataFrame(data=data[1:], columns=data[0])

#Renombrar algunas columnas
df.rename(columns = {'Fecha de diagnóstico':'Fecha',
                     'ID de caso':'ID', 
                     'País de procedencia':'Procedencia', 
                     'Ciudad de ubicación':'Ciudad',
                     'Departamento o Distrito':'Departamento',
                     'Atención**':'Atencion',
                     'Tipo*':'Tipo'}, inplace = True) 





f = df[['Fecha']].drop_duplicates()
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

 
    rel = df[(df['Tipo'] == 'Relacionado') & (df['Fecha'] == r)].count()
    allRel.append(rel[0])
    
    imp = df[(df['Tipo'] == 'Importado') & (df['Fecha'] == r)].count()
    allImp.append(imp[0])
    
    est = df[(df['Tipo'] == 'En estudio') & (df['Fecha'] == r)].count()
    allEst.append(est[0])
    
    casos = df[(df['Fecha'] == r)].count()
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

trace1 = {'x': myFechas,
          'y': allImp,
          'mode' : "lines+markers",
          'name' : 'Contagio en el exterior',
          'marker' : dict(color = 'DarkSlateGrey')
          } ;
trace2 = {'x': myFechas,
          'y': allRel,
          'mode' : "lines+markers",
          'name' : 'Contagio en Colombia',
          'marker' : dict(color = '#ff6361')
          } ;
trace3 = {'x': myFechas,
          'y': allEst,
          'mode' : "lines+markers",
          'name' : 'En estudio',
          'marker' : dict(color = '#ffa600')
          } ;

data = [trace1, trace2, trace3];

layout = dict(title = 'Casos venidos del extranjero vs. contagios locales',  xaxis= dict(title= 'Fecha',ticklen= 5,zeroline= False)
             )

fig = dict(data = data, layout = layout)
pyo.plot(fig, filename='import_local.html')
  



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

# --- PLOTEAR 
fig1Ydata=[]
fig1Ydata.append(acum)
fig1Ydata.append(inc)
fig1Ydata.append(allCasos)
fig1labels = ["Acumulado","Incremento", "Casos Diarios"]
fig1Title =  "Acumulado, Incremento y Casos en Colombia desde su aparición"

 
#Crear los parámetros para cada "trace". Basicamente eje Y.
trace1 = {'x': myFechas,
          'y': acum,
          'mode' : "lines+markers",
          'name' : 'Acumulado',
          'marker' : dict(color = 'DarkSlateGrey')
          } ;

trace2 = {'x':myFechas,
          'y':inc,
          'mode' : "lines+markers",
          'name':'Incremento',
          'marker' : dict(color = '#ff6361')
          };

trace3 = {'x':myFechas,
          'y':allCasos,
          'mode' : "lines+markers",
          'name':'Casos',
          'marker' : dict(color = '#ffa600')
          };

data = [trace1, trace2, trace3];
#print(data)

layout = dict(title = 'Progresión de casos en Colombia desde Marzo 6 del 2020 a la fecha',  xaxis= dict(title= 'Fecha',ticklen= 5,zeroline= False)
             )

fig = dict(data = data, layout = layout)
pyo.plot(fig, filename='progresion.html')



    
#--------------  MODELO SIR -------------------- 

# Clasificacion por Atencion en fechas
EstadosFecha = df.groupby(['Fecha', 'Atencion'], sort=False)['ID'].count()

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

trace1 = {'x': myFechas,
          'y': Recuperados,
          'mode' : "lines+markers",
          'name' : 'Recuperados',
          'marker' : dict(color = 'DarkSlateGrey')
          } ;

trace2 = {'x':myFechas,
          'y':Infectados,
          'mode' : "lines+markers",
          'name':'Infectados',
          'marker' : dict(color = '#ff6361')
          };

data = [trace1, trace2];
#print(data)

layout = dict(title = 'Recuperados vs. Infectaods',  xaxis= dict(title= 'Fecha',ticklen= 5,zeroline= False)
             )

fig = dict(data = data, layout = layout)
pyo.plot(fig, filename='rec_inf.html')
