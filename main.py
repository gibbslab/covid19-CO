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


#Se define el formato de las fechas como datetime
df['Fecha']=pd.to_datetime(df['Fecha'], format='%d/%m/%Y')
#Se realizan los conteos por fecha y tipo     
df_cont = df[['Fecha','Tipo','ID']].groupby(['Fecha','Tipo']).count().add_suffix('_Count').reset_index()
# Se realizan conteos por tipo relacionado, importado, en estudio y totales
allRel = df_cont[df_cont['Tipo'] == 'Relacionado']
allImp = df_cont[df_cont['Tipo'] == 'Importado']
allEst = df_cont[df_cont['Tipo'] == 'En estudio']
allCasos = df_cont[['Fecha','ID_Count']].groupby(['Fecha']).sum().reset_index()

#---------- DATOS BASICOS ----------
    
print ("----------------") 

c = sum(allCasos['ID_Count'])
i = sum(allImp['ID_Count'])
e = sum(allEst['ID_Count'])
r = sum(allRel['ID_Count'])
print('Casos Totales:     ' + str(c))
print('Casos Importados:  ' + str(i) + "(" + str(percentage(i,c)) + "%)")  
print('Casos Relacionados:' + str(r) + "(" + str(percentage(r,c)) + "%)")
print('Casos en Estudio:  ' + str(e) + "(" + str(percentage(e,c)) + "%)")


#--------------  RELACIONADOS - IMPORTADOS - EN ESTUDIO ------------------------ 

trace1 = {'x': allImp['Fecha'],
          'y': allImp['ID_Count'],
          'mode' : "lines+markers",
          'name' : 'Contagio en el exterior',
          'marker' : dict(color = 'DarkSlateGrey')
          } ;
trace2 = {'x': allRel['Fecha'],
          'y': allRel['ID_Count'],
          'mode' : "lines+markers",
          'name' : 'Contagio en Colombia',
          'marker' : dict(color = '#ff6361')
          } ;
trace3 = {'x': allEst['Fecha'],
          'y': allEst['ID_Count'],
          'mode' : "lines+markers",
          'name' : 'En estudio',
          'marker' : dict(color = '#ffa600')
          } ;

data = [trace1, trace2, trace3];

layout = dict(title = 'Casos venidos del extranjero vs. contagios locales',  xaxis= dict(title= 'Fecha',ticklen= 5,zeroline= False)
             )

fig = dict(data = data, layout = layout)
pyo.plot(fig)
  

#--------------  ACUMULADO E INCREMENTO POR FECHA -------------------- 

#Acumulado es igual a los casos de hoy mas los acumulados hasta ayer.
allCasos["acum"]= allCasos["ID_Count"].cumsum(axis=0)

#Incremento es igual  los casos de hoy menos los casos de ayer.
allCasos["inc"] = allCasos["ID_Count"].diff(1)


# --- PLOTEAR 
 
#Crear los parámetros para cada "trace". Basicamente eje Y.
trace1 = {'x': allCasos["Fecha"],
          'y': allCasos["acum"],
          'mode' : "lines+markers",
          'name' : 'Acumulado',
          'marker' : dict(color = 'DarkSlateGrey')
          } ;

trace2 = {'x':allCasos["Fecha"],
          'y':allCasos["inc"],
          'mode' : "lines+markers",
          'name':'Incremento',
          'marker' : dict(color = '#ff6361')
          };

trace3 = {'x':allCasos["Fecha"],
          'y':allCasos["ID_Count"],
          'mode' : "lines+markers",
          'name':'Casos',
          'marker' : dict(color = '#ffa600')
          };

data = [trace1, trace2, trace3];
#print(data)

layout = dict(title = 'Progresión de casos en Colombia desde Marzo 6 del 2020 a la fecha',  xaxis= dict(title= 'Fecha',ticklen= 5,zeroline= False)
             )

fig = dict(data = data, layout = layout)
pyo.plot(fig)



    
#--------------  MODELO SIR -------------------- 

# Clasificacion por Atencion en fechas
EstadosFecha = df.groupby(['Fecha', 'Atencion'], sort=False)['ID'].count().reset_index()

# poblacion colombiana
N = 49070000 # 49,07 millones
myFechas = allCasos['Fecha'].values

# infectados y recuperados
Infectados = EstadosFecha[EstadosFecha['Atencion'].isin(['Casa','Hospital','Hospital UCI'])].groupby('Fecha').sum().reset_index()
Recuperados = EstadosFecha[EstadosFecha['Atencion'].isin(['Recuperado'])].groupby('Fecha').sum().reset_index()
Fallecido = EstadosFecha[EstadosFecha['Atencion'].isin(['Fallecido'])].groupby('Fecha').sum().reset_index()


# PLOTEAR 

trace1 = {'x': Recuperados['Fecha'],
          'y': Recuperados['ID'],
          'mode' : "lines+markers",
          'name' : 'Recuperados',
          'marker' : dict(color = 'DarkSlateGrey')
          } ;

trace2 = {'x':Infectados['Fecha'],
          'y':Infectados['ID'],
          'mode' : "lines+markers",
          'name':'Infectados',
          'marker' : dict(color = '#ff6361')
          };

trace3 = {'x':Fallecido['Fecha'],
          'y':Fallecido['ID'],
          'mode' : "lines+markers",
          'name':'Fallecidos',
          'marker' : dict(color = '#2b97eb')
          };

data = [trace1, trace2, trace3];

layout = dict(title = 'Fallecidos, Recuperados, Infectados',  xaxis= dict(title= 'Fecha',ticklen= 5,zeroline= False)
             )

fig = dict(data = data, layout = layout)
pyo.plot(fig)
