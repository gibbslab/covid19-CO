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
url_pacientes = "https://e.infogram.com/api/live/flex/bc384047-e71c-47d9-b606-1eb6a29962e3/664bc407-2569-4ab8-b7fb-9deb668ddb7a?"
url_generales = 'https://e.infogram.com/api/live/flex/bc384047-e71c-47d9-b606-1eb6a29962e3/523ca417-2781-47f0-87e8-1ccc2d5c2839?'

#Debido a que la información no proviene de un formato dado, es necesario definirla como texto y aprovechar
#que esta viene en formato py, por ende se evalua ese texto
json_pacientes = eval(requests.get(url_pacientes).text)
json_generales = eval(requests.get(url_generales).text)

#Se seleccionan unicamente el dataframe del historico y se define como dataframe
data = json_pacientes["data"][0]
df_pacientes = pd.DataFrame(data=data[1:], columns=data[0])
data = json_generales["data"][0] # Hoja de casos acumulados
df_generales = pd.DataFrame(data=data[1:], columns=data[0])

#Renombrar algunas columnas
df_pacientes.rename(columns = {'Fecha de diagnóstico':'Fecha',
                     'ID de caso':'ID', 
                     'País de procedencia':'Procedencia', 
                     'Ciudad de ubicación':'Ciudad',
                     'Departamento o Distrito':'Departamento',
                     'Atención**':'Atencion',
                     'Tipo*':'Tipo'}, inplace = True)

df_generales.rename(columns = {'Fallecidos acumulados':'Fallecidos',
                     'Positivos acumulados':'Infectados',
                     'Recuperados acumulados':'Recuperados'}, inplace = True)

f = df_pacientes[['Fecha']].drop_duplicates()


#Se define el formato de las fechas como datetime
df_pacientes['Fecha']=pd.to_datetime(df_pacientes['Fecha'], format='%d/%m/%Y')
#Se realizan los conteos por fecha y tipo     
df_cont = df_pacientes[['Fecha','Tipo','ID']].groupby(['Fecha','Tipo']).count().add_suffix('_Count').reset_index()
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
pyo.plot(fig, filename='import_local.html')
  

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
pyo.plot(fig, filename='progresion.html')



    
#--------------  MODELO SIR -------------------- 

# poblacion colombiana
N = 49070000 # 49,07 millones
myFechas = allCasos['Fecha'].values

# Obtiene las columnas en listas por separado
I = df_generales['Infectados'].to_list()
R = df_generales['Recuperados'].to_list()
Fallecidos = df_generales['Fallecidos'].to_list()

# Convierte las listas de string a integer
I = [int(i) if i!='' else 0 for i in I]
R = [int(i) if i!='' else 0 for i in R]
Fallecidos = [int(i) if i!='' else 0 for i in Fallecidos]

# Añade los fallecidos a la lista de recuperados
for i, bi in enumerate(Fallecidos): R[i] += bi

S = [N - I[i] - R[i] for i in range(len(I))]

# Calcula la derivada de los acumulados
puntoS = [x - S[i-1] for i, x in enumerate(S)]
puntoI = [x - I[i-1] for i, x in enumerate(I)]
puntoR = [x - R[i-1] for i, x in enumerate(R)]
puntoS[0] = 0
puntoI[0] = 0
puntoR[0] = 0

import SIR
beta_gamma, intercept = SIR.RegresionLineal(I, puntoI)
print ("(beta-gamma) found by gradient descent: %f" %(beta_gamma[0]))

# Grafica
trendX = [I[0], I[-1]]
trendY = [(I[0]*beta_gamma[0])+intercept, (I[-1]*beta_gamma[0])+intercept]
trend = {'x': trendX,
          'y': trendY,
          'mode' : "lines",
          'name' : 'tendencia',
          'marker' : dict(color = '#ffa600')
          } ;
scatter =  {'x': I,
          'y': puntoI,
          'mode' : "markers",
          'name' : 'infectados',
          'marker' : dict(color = '#ff6361')
          } ;

data = [scatter, trend];

layout = dict(title = 'Infectados acumulados vs nuevos infectados',  xaxis= dict(title= 'Infectados acumulados',ticklen= 5,zeroline= False)
             )

fig = dict(data = data, layout = layout)
pyo.plot(fig, filename='acu_nuevos.html')

# Encontrando gamma
gamma, _ = SIR.RegresionLineal(I, puntoR)
print ("(gamma) found by gradient descent: %f" %(gamma[0]))

# Grafica
trendX = [I[0], I[-1]]
trendY = [(I[0]*gamma[0])+_, (I[-1]*gamma[0])+_]
trend = {'x': trendX,
          'y': trendY,
          'mode' : "lines",
          'name' : 'tendencia',
          'marker' : dict(color = '#ffa600')
          } ;
scatter =  {'x': I,
          'y': puntoR,
          'mode' : "markers",
          'name' : 'Recuperados',
          'marker' : dict(color = '#ff6361')
          } ;

data = [scatter, trend];

layout = dict(title = 'Infectados acumulados vs nuevos recuperados',  xaxis= dict(title= 'Infectados acumulados',ticklen= 5,zeroline= False)
             )

fig = dict(data = data, layout = layout)
pyo.plot(fig, filename='acumulados_vs_nuevos_recuperados.html')

beta = beta_gamma[0] - gamma[0]
R_0 = beta / gamma
print ("(beta) found by gradient descent: %f" %(beta))
print ("(R_0) found by gradient descent: %f" %(R_0))

""" 
# Coeficiente de transmicion beta 
# y Tasa de recuperacion gama
# se obtienen por gradient descent


# Calculo de derivadas: tasa de cambio
punto_S = -beta * Suceptibles * Infectados / N
punto_I = (beta * Suceptibles * Infectados / N) - (gama * Infectados)
punto_R = gama * Infectados
# NOTA: punto_S + punto_I + punto_R = 0 
"""

trace1 = {'x': myFechas,
          'y': R,
          'mode' : "lines+markers",
          'name' : 'Recuperados',
          'marker' : dict(color = 'DarkSlateGrey')
          } ;

trace2 = {'x':myFechas,
          'y':I,
          'mode' : "lines+markers",
          'name':'Infectados',
          'marker' : dict(color = '#ff6361')
          };

data = [trace1, trace2];

layout = dict(title = 'Fallecidos, Recuperados, Infectados',  xaxis= dict(title= 'Fecha',ticklen= 5,zeroline= False)
             )

fig = dict(data = data, layout = layout)
pyo.plot(fig, filename='rec_inf.html')
