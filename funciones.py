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
    #plt.annotate(xy=[1,1], s="Inico")
    plt.show()
   
    
    #plt.savefig('/Users/andresmpinzonv/Desktop/plot.png', dpi=200)

    #Este comando abre la ventana para mostrar la grafica. Es probable
    #que en spyder no sea necesario, pero e IpYthon solo debería necesitarse.
   
    

