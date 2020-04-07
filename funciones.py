#!/usr/bin/env python2
# -*- coding: utf-8 -*-


"""
                        === PLOTME ====
Funcion para plotear
#x: eje X.
y: Array con los datos del eje Y 
labels = titulos de cada una de los datos en Y
tile: Título de la gráfica

#Lista de markers y demas formatting:
#https://matplotlib.org/api/_as_gen/matplotlib.pyplot.plot.html
#Color picking:
#https://learnui.design/tools/data-color-picker.html
"""
#Llamando matplotlib desde acá fue la única manera de evitar que Python
# no viera a "plt".
import matplotlib.pyplot as plt

def plotme(x,y,label,title):
    
    #Acá se asume que "Y" tanto como "label" tienen la misma longitud
    for i in range(0,len(y)):
        plt.plot(x,y[i],label = label[i], marker ='.',linewidth='1.5')
    
    
    plt.grid()
    plt.legend()

    #caracteristicas de los ticks:
    #https://matplotlib.org/3.1.1/tutorials/text/text_intro.html
    plt.tick_params(axis='x', rotation=70)
    
    plt.suptitle(title)
    
    #https://matplotlib.org/2.0.2/examples/pylab_examples/annotation_demo.html
    plt.annotate('Tapabocas obligatorio',
            xy=(26, 70), xycoords='data',
            xytext=(-50, 50), textcoords='offset points',
            arrowprops=dict(facecolor='#58508d', shrink=0.05),
            horizontalalignment='right', verticalalignment='bottom')
    
    plt.show()
   
    
    #plt.savefig('/Users/andresmpinzonv/Desktop/plot.png', dpi=200)

    #Este comando abre la ventana para mostrar la grafica. Es probable
    #que en spyder no sea necesario, pero e IpYthon solo debería necesitarse.
   
"""
Funcion para calcular porcentajes simples
Retorna un entero de 64
"""
    
def percentage(part, whole):
  return 100 * float(part)/float(whole)
   
    

