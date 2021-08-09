################################################################################################
#                                Mineria de Datos 2021-2                                       #
#                                       Grupo: 01                                              #
#                              Facultad de Ingenieria UNAM                                     #
#                                 Manuel Salazar Aguilar                                       #
#                                       314245281                                              #
################################################################################################

import pandas as pd     # Para la manipulacion y analisis de datos
import numpy as np     # Para crear vectores matrices de datos de n dimensiones
import matplotlib.pyplot as plt   # Para generar graficos
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

#import seaborn as sns  # Para la visualizacion de los datos

def obtener_matriz_corr(data):
	corr = data.corr()
	corr_framed = pd.DataFrame(corr)
	return(corr_framed)

def grafs_dist(data):
	var_int64 = data.dtypes[data.dtypes == np.float64]
	var_float64 = data.dtypes[data.dtypes == np.int64]
	var_validas = sorted(list(var_int64.index)+ list(var_float64.index))
	return(var_validas)

	#columnas = lis(data.columns)
	#data.hist(figsize=(10,10),xrot=45)
	#plt.title('matplotlib.pyplot.hist() function Example\n\n',
  #        fontweight ="bold")
	#plt.show()

def gen_graf_corr():
    txt_var_corr_1 = variable_corr_1.get()
    txt_var_corr_2 = variable_corr_2.get()
    plt.plot(Datos[txt_var_corr_1], Datos[txt_var_corr_2], 'b+')
    plt.title('GRAFICO DE DISPERSION\n'+txt_var_corr_1.upper()+" VS "+txt_var_corr_2.upper())
    plt.xlabel(txt_var_corr_1.upper())
    plt.ylabel(txt_var_corr_2.upper())
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()