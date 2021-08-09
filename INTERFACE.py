################################################################################################
#                                Mineria de Datos 2021-2                                       #
#                                       Grupo: 01                                              #
#                              Facultad de Ingenieria UNAM                                     #
#                                 Manuel Salazar Aguilar                                       #
#                                       314245281                                              #
################################################################################################

import tkinter as tk
import tkinter.font as font
from tkinter import LabelFrame
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import StringVar
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

import matplotlib.pyplot as plt 
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk 
import seaborn as sns

from PIL import ImageTk, Image

import os.path  

import pandas as pd

import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn import linear_model
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score 

from kneed import KneeLocator

#from scipy.spatial.distance import cdist

from mpl_toolkits.mplot3d import Axes3D

import EDA

################################################################################################
################################################################################################
################################# VENTANA PRINCIPAL ############################################
################################################################################################
################################################################################################

#Se crea la instancia de la aplicacion
#Geometry (WxH) permite determinar el tamaño de la ventana, al añadir los valores 
#extras se determina una posicion inicial para la ventana diferente al extremo 
#superior izquierdo de la pantalla, en este caso los valores estan ajustados para
#posicionarla en el centro de la pantalla

app = tk.Tk()
app.geometry("800x400+283+184")
app.maxsize(800,400)
app.title("PROYECTO FINAL MD")
color_fondo = '#CFD7FF' 
app.configure(bg=color_fondo)
plt.rcParams.update({'font.size': 6})

#Definicion de fuentes
fontApp = font.Font(family='Cambria', size=12, weight='bold')
pathFont = font.Font(family='Cambria', size=11, weight='bold')
fontTitle = font.Font(family='Cambria', size=15, weight='bold')
smallfont = font.Font(family='Cambria', size=9)
font = font.Font(family='Cambria', size=12, weight='bold', slant='italic')
########### DEFINICION DE PESTAÑAS ############################

style = ttk.Style()
settings = {"TNotebook.Tab": {"configure": {"padding": [19, 2],
                                            "background": color_fondo
                                           },
                              "map": {"background": [("selected", "#787CFA"), 
                                                     ("active", "#E8ECFC")]

                                     }
                              }
           }  

style.theme_create("mi_estilo", parent="alt", settings=settings)
style.theme_use("mi_estilo")

notebook = ttk.Notebook(app)

tab_1 = tk.Frame(notebook,background = color_fondo)
tab_2 = tk.Frame(notebook,background = color_fondo)
tab_3 = tk.Frame(notebook,background = color_fondo)
tab_4 = tk.Frame(notebook,background = color_fondo)
#tab_5 = tk.Frame(notebook,background = color_fondo)
tab_6 = tk.Frame(notebook,background = color_fondo)
tab_7 = tk.Frame(notebook,background = color_fondo)
tab_8 = tk.Frame(notebook,background = color_fondo)

notebook.add(tab_1, text = '    ARCHIVO    ')
notebook.add(tab_2, text = '     DATOS     ')
notebook.add(tab_3, text = '      EDA      ')
notebook.add(tab_4, text = '      PCA      ')
#notebook.add(tab_5, text = '   DISTANCIA   ')
notebook.add(tab_6, text = '    CLUSTER    ')
notebook.add(tab_7, text = ' CLASIFICACION ')
notebook.add(tab_8, text = '   PREDICCION  ')

#Las pestañas de analisis de datos estan bloqueadas hasta la lectura de
#un archivo
notebook.tab(1,state="disabled")
notebook.tab(2,state="disabled")
notebook.tab(3,state="disabled")
notebook.tab(4,state="disabled")
notebook.tab(5,state="disabled")
notebook.tab(6,state="disabled")

notebook.pack(fill='both',expand=1)

########### LOGOS #############################################

#Creación de label para el titulo
lbl_intro = tk.Label(tab_1)
lbl_intro["text"] = "Mineria de Datos GUI"
lbl_intro["font"] = fontTitle
lbl_intro["bg"] = color_fondo
lbl_intro.place(x=0,y=50,width=800)

#Creación de label para el inicio
lbl_main = tk.Label(tab_1)
lbl_main["text"] = "Seleccione un archivo desde el cual\nse tomaran los datos"
lbl_main["font"] = fontApp
lbl_main["bg"] = color_fondo
lbl_main.place(x=0,y=120,width=800,height=40)

image_logo = Image.open("IMAGES/unam.jpg")
image_logo = image_logo.resize((125,140),Image.ANTIALIAS)
logo = ImageTk.PhotoImage(image_logo)
label_logo = tk.Label(tab_1,image=logo)
label_logo.image=logo
label_logo["bg"] = color_fondo
label_logo.place(x=10, y=10)

image_fi = Image.open("IMAGES/fi.jpg")
image_fi = image_fi.resize((125,140),Image.ANTIALIAS)
logo_fi = ImageTk.PhotoImage(image_fi)
label_logo_fi = tk.Label(tab_1,image=logo_fi)
label_logo_fi.image=logo_fi
label_logo_fi["bg"] = color_fondo
label_logo_fi.place(x=660, y=10)

########### BOTONES INICIO Y ARCHIVO #########################

########### FUNCION PARA LA LECTURA DE DATOS ##################

def open_File():
    global Datos
    Datos=[]    
    filepath = askopenfilename(
        filetypes=[("Archivo CSV", "*.csv*"), ("Archivo de texto", "*.txt"), ("Archivo XLS", "*.xls")]
    )
    if not filepath:
        lbl_file["text"] = "No se ha seleccionado\n un archivo"
        notebook.tab(1,state="disabled")
        notebook.tab(2,state="disabled")
        return
    nombre,extension = os.path.splitext(filepath)
    splited_1 = nombre.split('/')
    splited_2 = extension.split('.')
    lbl_file["text"] = ("Nombre del archivo: " + splited_1[-1] + "\n Extensión: "+ splited_2[-1])
    #Se decide la funcion de lectura de datos en funcion del tipo de archivo
    #Se crea un DataFrame adecuado al tipo de datos
    if extension in [".txt"]:
        Datos=pd.read_table(filepath)
    elif extension in [".csv"]:
        Datos=pd.read_csv(filepath)
    elif extension in [".xls"]:
        Datos=pd.read_excel(filepath)
    #Se obtiene la lista de variables float64 e int64
    global var_vals
    global var_others
    global Datos_Retagged
    Datos_Retagged = Datos
    var_vals = EDA.grafs_dist(Datos)
    #Se habilitan las pestañas bloqueadas
    notebook.tab(1,state="normal")
    notebook.tab(2,state="normal")
    notebook.tab(3,state="normal")
    notebook.tab(4,state="normal")
    notebook.tab(5,state="normal")
    notebook.tab(6,state="normal")

#Boton empleado para seleccionar archivos
border = LabelFrame(tab_1, bd = 6, bg = '#D8D8E3')
border.place(x=315,y=195,width=170,height=50)
open_file_btn = tk.Button(tab_1)
open_file_btn["text"] = "Seleccionar Archivo"
open_file_btn["font"] = font
open_file_btn["fg"] = '#020233'
open_file_btn["bg"] = '#D8D8E3'
open_file_btn["command"] = open_File
open_file_btn.place(x=320,y=200,width=160,height=40)

#Label para mostrar el nombre del archivo
lbl_file = tk.Label(tab_1)
lbl_file["text"] = "No se ha seleccionado\n un archivo"
lbl_file["font"] = pathFont
lbl_file["bg"] = color_fondo
lbl_file.place(x=0,y=265,width=800,height=40)

#Boton para cerrar la aplicacion
border = LabelFrame(tab_1,bd = 6, bg = '#D8D8E3')
border.place(x=360,y=330,width=80,height=40)
quit = tk.Button(tab_1)
quit["text"] = "SALIR"
quit["fg"] = "red"
quit["font"]=font
quit["bg"] = '#D8D8E3'
quit["command"] = app.destroy
quit.place(x=365,y=335,width=70,height=30)

################################################################################################
################################################################################################
########################### PESTAÑA DE DESPLIEGUE DE DATOS #####################################
################################################################################################
################################################################################################

############# Funciones empleadas para refrescar y mostrar datos #########
def refresh_shape():
    lbl_shape["text"] = ("Numero de Registros: "+ str(Datos.shape[0]) +"\n Numero de Columnas: "+str(Datos.shape[1]))

############# Ventanas emergentes #############################
def show_types():
    #Creación y definición de ventana emergente
    wind_full_pear = tk.Toplevel(app)
    wind_full_pear.title("TIPOS DE DATOS")
    wind_full_pear.geometry("500x300+433+234")
    wind_full_pear.maxsize(500,300)
    #Ventana donde se muestra el tipo de datos
    window_type=scrolledtext.ScrolledText(wind_full_pear, width = 59, height = 18)
    window_type.insert(tk.INSERT,Datos.dtypes)
    #Se inhabilita la opcion de añadir texto  
    window_type.configure(state='disabled',bg=color_fondo)
    window_type.grid(column = 0, pady = 5, padx = 5)

def show_nulls():
    #Creación y definición de ventana emergente
    wind_full_pear = tk.Toplevel(app)
    wind_full_pear.title("DATOS NULOS")
    wind_full_pear.geometry("500x300+433+234")
    wind_full_pear.maxsize(500,300)
    #Ventana donde se muestra el tipo de datos
    window_nulls=scrolledtext.ScrolledText(wind_full_pear, width = 59, height = 18)
    window_nulls.insert(tk.INSERT,Datos.isnull().sum())
    #Se inhabilita la opcion de añadir texto  
    window_nulls.configure(state='disabled',bg=color_fondo)
    window_nulls.grid(column = 0, pady = 5, padx = 5)

def display_regs():
    #Creación y definición de ventana emergente
    wind_full_pear = tk.Toplevel(app)
    wind_full_pear.title("REGISTROS")
    wind_full_pear.geometry("1300x300+33+234")
    wind_full_pear.maxsize(1300,300)
    #Ventana donde se muestran los registros
    window_nulls=scrolledtext.ScrolledText(wind_full_pear, width = 159, height = 18)
    window_nulls.insert(tk.INSERT,Datos.head(-10))
    #Se inhabilita la opcion de añadir texto  
    window_nulls.configure(state='disabled',bg=color_fondo)
    window_nulls.grid(column = 0, pady = 5, padx = 5)

lbl_desc = tk.Label(tab_2)
lbl_desc["text"] = "Descripción de los datos"
lbl_desc["font"] = fontTitle
lbl_desc["bg"] = color_fondo
lbl_desc.place(x=0,y=10,width=780,height=40)

#Boton empleado para obtener el Shape de los datos
border_tab2_shape = LabelFrame(tab_2,bd = 6, bg = '#D8D8E3')
border_tab2_shape.place(x=340,y=60,width=120,height=40)
btn_shape = tk.Button(tab_2)
btn_shape["text"] = "Descripcion"
btn_shape["font"] = smallfont
btn_shape["bg"] = '#D8D8E3'
btn_shape["command"] = refresh_shape
btn_shape.place(x=345,y=65,width=110,height=30)

lbl_shape = tk.Label(tab_2)
lbl_shape["font"] = pathFont
lbl_shape["bg"] = '#CFD7FF'
lbl_shape.place(x=0,y=115,width=800,height=40)

#Boton empleado para obtener el dtype de los datos
border_tab2_type = LabelFrame(tab_2,bd = 6, bg = '#D8D8E3')
border_tab2_type.place(x=340,y=180,width=120,height=40)
btn_type = tk.Button(tab_2)
btn_type["text"] = "Tipos"
btn_type["font"] = smallfont
btn_type["bg"] = '#D8D8E3'
btn_type["command"] = show_types
btn_type.place(x=345,y=185,width=110,height=30)

#Boton empleado para obtener los datos nulos
border_tab2_nulls = LabelFrame(tab_2,bd = 6, bg = '#D8D8E3')
border_tab2_nulls.place(x=340,y=240,width=120,height=40)
btn_nulls = tk.Button(tab_2)
btn_nulls["text"] = "Nulos"
btn_nulls["font"] = smallfont
btn_nulls["bg"] = '#D8D8E3'
btn_nulls["command"] = show_nulls
btn_nulls.place(x=345,y=245,width=110,height=30)

#Boton empleado para desplegar datos
border_tab2_regs = LabelFrame(tab_2,bd = 6, bg = '#D8D8E3')
border_tab2_regs.place(x=340,y=300,width=120,height=40)
btn_regs = tk.Button(tab_2)
btn_regs["text"] = "Registros"
btn_regs["font"] = smallfont
btn_regs["bg"] = '#D8D8E3'
btn_regs["command"] = display_regs
btn_regs.place(x=345,y=305,width=110,height=30)

################################################################################################
################################################################################################
######################################### PESTAÑA EDA ##########################################
################################################################################################
################################################################################################

def display_matriz_corr():
    fig = plt.figure(figsize=(8,4))
    plt.title('MATRIZ DE CORRELACIÓN')
    sns.heatmap(Datos.corr(),cmap='RdBu_r',annot=True)
    plt.xticks(rotation=20)
    plt.yticks(rotation=20)
    plt.show()

def confirmacion_btn_1():
    txt_var_corr = variable_corr.get()
    Datos[txt_var_corr].hist(figsize= (5.5,5),xrot=45,alpha=0.75)
    plt.title('DISTRIBUCION DE LA VARIABLE\n '+txt_var_corr.upper())
    plt.grid(True)
    plt.show()

def confirmacion_btn_2():
    txt_var_corr = variable_corr.get()
    #Datos[txt_var_corr].hist(figsize= (5.5,5),xrot=45,alpha=0.75)
    plt.title('BOXPLOT DE LA VARIABLE\n '+txt_var_corr.upper())
    sns.boxplot(data = Datos[txt_var_corr],orient="h")
    plt.grid(True)
    plt.show()

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

def display_distr():
    global variable_corr
    global txt_var_corr
    
    #Creación y definición de ventana emergente
    window_2 = tk.Toplevel(app)
    window_2.title("DISTRIBUCION DE DATOS")
    window_2.geometry("500x190+433+309")
    window_2.maxsize(500,190)
    window_2.configure(bg=color_fondo)

    #Label del menu
    lbl_menu = tk.Label(window_2)
    lbl_menu["font"] =  font
    lbl_menu["text"] = "Eliga la variable para elaborar la grafica de distribución"
    lbl_menu["bg"] = '#CFD7FF'
    lbl_menu.place(x=0,y=20,width=500,height=40)

    #Menu para seleccionar la variable para observar la distribucion
    variable_corr = tk.StringVar(window_2)
    variable_corr.set(var_vals[0])
    menu = tk.OptionMenu(window_2, variable_corr, *var_vals)
    menu.place(x=90,y=70,width=320,height=40)
    txt_var_corr = variable_corr.get()
    
    #Boton empleado para confirmar la creacion de la grafica
    border_conf = LabelFrame(window_2,bd = 6, bg = '#D8D8E3')
    border_conf.place(x=90,y=130,width=120,height=40)
    btn_conf = tk.Button(window_2)
    btn_conf["text"] = "HISTOGRAMA"
    btn_conf["font"] = smallfont
    btn_conf["bg"] = '#D8D8E3'
    btn_conf["command"] = confirmacion_btn_1
    btn_conf.place(x=95,y=135,width=110,height=30)

    #Boton empleado para confirmar la creacion de la grafica
    border_conf_2 = LabelFrame(window_2,bd = 6, bg = '#D8D8E3')
    border_conf_2.place(x=290,y=130,width=120,height=40)
    btn_conf_2 = tk.Button(window_2)
    btn_conf_2["text"] = "BOXPLOT"
    btn_conf_2["font"] = smallfont
    btn_conf_2["bg"] = '#D8D8E3'
    btn_conf_2["command"] = confirmacion_btn_2
    btn_conf_2.place(x=295,y=135,width=110,height=30)

def display_corr_var():
    global variable_corr_1
    global variable_corr_2
    global txt_var_corr_1
    global txt_var_corr_2
    
    #Creación y definición de ventana emergente
    window_3 = tk.Toplevel(app)
    window_3.title("CORRELACION DE DOS VARIABLES")
    window_3.geometry("500x190+433+289")
    window_3.maxsize(500,190)
    window_3.configure(bg=color_fondo)

    #Label del menu
    lbl_menu_1 = tk.Label(window_3)
    lbl_menu_1["font"] =  font
    lbl_menu_1["text"] = "Eliga las variable para elaborar la grafica de correlación"
    lbl_menu_1["bg"] = '#CFD7FF'
    lbl_menu_1.place(x=0,y=20,width=500,height=40)

    #Menu para seleccionar la variable 1 para la correlacion
    variable_corr_1 = tk.StringVar(window_3)
    variable_corr_1.set(var_vals[0])
    menu_1 = tk.OptionMenu(window_3, variable_corr_1, *var_vals)
    menu_1.place(x=30,y=70,width=200,height=40)
    txt_var_corr_1 = variable_corr_1.get()
    
    #Menu para seleccionar la variable 2 para la correlacion
    variable_corr_2 = tk.StringVar(window_3)
    variable_corr_2.set(var_vals[0])
    menu_2 = tk.OptionMenu(window_3, variable_corr_2, *var_vals)
    menu_2.place(x=270,y=70,width=200,height=40)
    txt_var_corr_2 = variable_corr_2.get()

    #Boton empleado para confirmar la creacion de la grafica
    border_conf_1 = LabelFrame(window_3,bd = 6, bg = '#D8D8E3')
    border_conf_1.place(x=190,y=130,width=120,height=40)
    btn_conf_1 = tk.Button(window_3)
    btn_conf_1["text"] = "Confirmar"
    btn_conf_1["font"] = smallfont
    btn_conf_1["bg"] = '#D8D8E3'
    btn_conf_1["command"] = gen_graf_corr
    btn_conf_1.place(x=195,y=135,width=110,height=30)

def lbl_data_conf():
    txt_var_corr_3 = variable_corr_3.get()
    Correlaciones = Datos.corr(method='pearson')
    cadena = ""
    rows = ""
    for row in Correlaciones[txt_var_corr_3].sort_values(ascending=False)[:10].index:
        rows += row
        rows += '\n\n'
    for value in Correlaciones[txt_var_corr_3].sort_values(ascending=False)[:10]:
        cadena +="{:.4f}".format(value)+'\n\n'
    #lbl_data["text"]="VALORES\n\n"+str(Correlaciones[txt_var_corr_3].sort_values(ascending=False)[:10])
    lbl_data["text"]="VALORES\n\n"+cadena
    lbl_data_name["text"]="VARIABLE\n\n"+rows

def display_lista_corr():
    global variable_corr_3
    global txt_var_corr_3
    global lbl_data
    global lbl_data_name
    #Creación y definición de ventana emergente
    window_4 = tk.Toplevel(app)
    window_4.title("VALORES DE CORRELACION")
    window_4.geometry("500x500+433+134")
    window_4.maxsize(500,500)
    window_4.configure(bg=color_fondo)

    #Label del menu
    lbl_menu_3 = tk.Label(window_4)
    lbl_menu_3["font"] =  smallfont
    lbl_menu_3["text"] = "Eliga la variable para obtener los valores de correlación más altos"
    lbl_menu_3["bg"] = '#CFD7FF'
    lbl_menu_3.place(x=0,y=20,width=500,height=40)

    #Menu para seleccionar la variable para la correlacion
    variable_corr_3 = tk.StringVar(window_4)
    variable_corr_3.set(var_vals[0])
    menu_3 = tk.OptionMenu(window_4, variable_corr_3, *var_vals)
    menu_3.place(x=50,y=70,width=230,height=40)
    txt_var_corr_3 = variable_corr_3.get()

    #Labels de los datos
    #Label de los datos
    lbl_data_name = tk.Label(window_4)
    lbl_data_name["font"] =  smallfont
    lbl_data_name["bg"] = '#CFD7FF'
    lbl_data_name.place(x=50,y=130,width=200,height=350)
    lbl_data = tk.Label(window_4)
    lbl_data["font"] =  smallfont
    lbl_data["bg"] = '#CFD7FF'
    lbl_data.place(x=265,y=130,width=200,height=350)

    #Boton empleado para confirmar la generacion de datos
    border_conf_3 = LabelFrame(window_4,bd = 6, bg = '#D8D8E3')
    border_conf_3.place(x=300,y=70,width=150,height=40)
    btn_conf_3 = tk.Button(window_4)
    btn_conf_3["text"] = "Generar Valores"
    btn_conf_3["font"] = smallfont
    btn_conf_3["bg"] = '#D8D8E3'
    btn_conf_3["command"] = lbl_data_conf
    btn_conf_3.place(x=305,y=75,width=140,height=30)

#Boton empleado para desplegar la matriz de correlaciones
border_tab3_corr = LabelFrame(tab_3,bd = 6, bg = '#D8D8E3')
border_tab3_corr.place(x=310,y=60,width=180,height=40)
btn_mat_corr = tk.Button(tab_3)
btn_mat_corr["text"] = "Matriz de Correlación"
btn_mat_corr["font"] = smallfont
btn_mat_corr["bg"] = '#D8D8E3'
btn_mat_corr["command"] = display_matriz_corr
btn_mat_corr.place(x=315,y=65,width=170,height=30)

#Boton empleado para desplegar las graficas de distribucion 
border_tab3_dist = LabelFrame(tab_3,bd = 6, bg = '#D8D8E3')
border_tab3_dist.place(x=310,y=120,width=180,height=40)
btn_mat_corr = tk.Button(tab_3)
btn_mat_corr["text"] = "Distribución"
btn_mat_corr["font"] = smallfont
btn_mat_corr["bg"] = '#D8D8E3'
btn_mat_corr["command"] = display_distr
btn_mat_corr.place(x=315,y=125,width=170,height=30)

#Boton empleado para desplegar la correlacion de dos variables
border_tab3_vars = LabelFrame(tab_3,bd = 6, bg = '#D8D8E3')
border_tab3_vars.place(x=310,y=180,width=180,height=40)
btn_mat_vars = tk.Button(tab_3)
btn_mat_vars["text"] = "Correlación Variables"
btn_mat_vars["font"] = smallfont
btn_mat_vars["bg"] = '#D8D8E3'
btn_mat_vars["command"] = display_corr_var
btn_mat_vars.place(x=315,y=185,width=170,height=30)

#Boton empleado para desplegar los valores de correlacion mas altos
#para una variable
border_tab3_val = LabelFrame(tab_3,bd = 6, bg = '#D8D8E3')
border_tab3_val.place(x=310,y=240,width=180,height=40)
btn_mat_val = tk.Button(tab_3)
btn_mat_val["text"] = "Valores de Correlación"
btn_mat_val["font"] = smallfont
btn_mat_val["bg"] = '#D8D8E3'
btn_mat_val["command"] = display_lista_corr
btn_mat_val.place(x=315,y=245,width=170,height=30)

################################################################################################
################################################################################################
######################################### PESTAÑA PCA ##########################################
################################################################################################
################################################################################################

def show_Data_Frame(DataFrame,titulo,alineacion):
    #Creación y definición de ventana emergente
    window_MN = tk.Toplevel(app)
    window_MN.title(titulo)
    window_MN.geometry("800x400+283+184")
    window_MN.maxsize(800,400)
    #Ventana donde se muestra la matriz normalizada
    textContainer = tk.Frame(window_MN, borderwidth=5, relief="sunken")
    text = tk.Text(textContainer, width=24, height=13, wrap="none", borderwidth=0)
    textVsb = tk.Scrollbar(textContainer, orient="vertical", command=text.yview)
    textHsb = tk.Scrollbar(textContainer, orient="horizontal", command=text.xview)
    text.configure(yscrollcommand=textVsb.set, xscrollcommand=textHsb.set,bg=color_fondo)
    text.tag_configure("tag_left", justify='left')
    text.tag_configure("tag_center", justify='center')
    titulo = "\n\n"+titulo+"\n\n\n"
    text.insert("insert",titulo,"tag_center")
    text.insert("insert",DataFrame,alineacion)
    text.configure(state="disable")
    text.grid(row=0, column=0, sticky="nsew")
    textVsb.grid(row=0, column=1, sticky="ns")
    textHsb.grid(row=1, column=0, sticky="ew")
    textContainer.grid_rowconfigure(0, weight=1)
    textContainer.grid_columnconfigure(0, weight=1)
    #textContainer.insert(tk.INSERT, "Hola Mundo")
    textContainer.pack(side="top", fill="both", expand=True)

def gen_estandar():
    global MNormalizada
    global Datos_Drop
    global Datos_Drop_New
    var_others = []
    var_others = list(Datos.columns)
    var_others_new = var_others
    #Se obtienen las columnas que seran removidas de la matriz de datos original
    for val in var_vals:
        if val in var_others:
            var_others_new.remove(val)
    #Emplea la matriz de datos para generar una matriz solo con variables numericas
    normalizar = StandardScaler()                         # Se instancia el objeto StandardScaler 
    Datos_Drop = Datos.drop(var_others_new, axis=1)       # Se quitan las variables no necesarias
    Datos_Drop_New = Datos_Drop
    normalizar.fit(Datos_Drop)                            # Se calcula la media y desviación para cada dimensión
    MNormalizada = normalizar.transform(Datos_Drop)        # Se normalizan los datos 
    framed_MNormalizada = pd.DataFrame(MNormalizada,columns=Datos_Drop.columns)
    btn_pca["state"] = "normal"
    #btn_euc["state"] = "normal"
    #btn_chev["state"] = "normal"
    #btn_manh["state"] = "normal"
    #btn_mink["state"] = "normal"
    show_Data_Frame(framed_MNormalizada,"MATRIZ DE DATOS NORMALIZADA","tag_left")

def gen_componentes():
    global pca
    global X_pca
    #Se genera un objeto PCA con 10 componentes principales    
    pca = PCA(n_components=None)                # Se instancia el objeto PCA           
    pca.fit(MNormalizada)                       # Se obtiene los componentes
    X_pca = pca.transform(MNormalizada)         # Se convierte los datos con las nuevas dimensiones     
    framed_Comps=pd.DataFrame(pca.components_,columns=Datos_Drop.columns)
    show_Data_Frame(framed_Comps,"COMPONENTES PRINCIPALES","tag_left")
    btn_eig["state"] = "normal"
    
def gen_vect_PCA():
    global Varianza
    Varianza = pca.explained_variance_ratio_
    text = "\n\n\n"+str(Varianza)+"\n\n\n"
    framed_eigen = pd.DataFrame(Varianza)
    show_Data_Frame(framed_eigen,"EIGENVALORES","tag_center")
    btn_sum_var["state"] = "normal"

def lbl_var_conf():
    txt_var_acum = var_acum.get()
    var_acumulada = sum(Varianza[0:int(txt_var_acum)])
    percent_var_acum = var_acumulada*100
    lbl_var_acum["text"]= "Varianza acumulada para "+txt_var_acum+" variables:\n\n"+\
                         "{:.4f}".format(var_acumulada)+"("+"{:.2f}".format(percent_var_acum)+" %)" 
    #Generacion de la grafica
    data_sum = np.cumsum(pca.explained_variance_ratio_)
    plt.plot(data_sum)
    plt.xlabel('NUMERO DE COMPONENTES')
    plt.ylabel('VARIANZA ACUMULADA')
    plt.plot([int(txt_var_acum),int(txt_var_acum)], [0, 1],lw=2,color='r')
    plt.grid()
    plt.show()

def gen_var_acumulada():
    global var_acum
    global lbl_var_acum
    num_vars = []
    for x in range(0,len(pca.components_)):
        num_vars.append(x)
    #Creación y definición de ventana emergente
    window_5 = tk.Toplevel(app)
    window_5.title("VARIANZA ACUMULADA")
    window_5.geometry("500x250+433+259")
    window_5.maxsize(500,250)
    window_5.configure(bg=color_fondo)
    #Label del menu
    lbl_menu_5 = tk.Label(window_5)
    lbl_menu_5["font"] =  smallfont
    lbl_menu_5["text"] = "Eliga el numero de componentes deseados para el valor de varianza acumulada"
    lbl_menu_5["bg"] = '#CFD7FF'
    lbl_menu_5.place(x=0,y=20,width=500,height=40)
    #Menu para seleccionar la variable para la correlacion
    var_acum = tk.StringVar(window_5)
    var_acum.set(num_vars[0])
    menu_5 = tk.OptionMenu(window_5, var_acum, *num_vars)
    menu_5.place(x=50,y=70,width=230,height=40)
    txt_var_acum = var_acum.get()
    #Boton empleado para confirmar el calculo de varianza acumulada
    border_conf_5 = LabelFrame(window_5,bd = 6, bg = '#D8D8E3')
    border_conf_5.place(x=300,y=70,width=150,height=40)
    btn_conf_5 = tk.Button(window_5)
    btn_conf_5["text"] = "Varianza Acumulada"
    btn_conf_5["font"] = smallfont
    btn_conf_5["bg"] = '#D8D8E3'
    btn_conf_5["command"] = lbl_var_conf
    btn_conf_5.place(x=305,y=75,width=140,height=30)
    #Labels de los datos
    lbl_var_acum = tk.Label(window_5)
    lbl_var_acum["font"] =  smallfont
    lbl_var_acum["bg"] = '#CFD7FF'
    lbl_var_acum.place(x=0,y=120,width=500,height=100)
    btn_discard["state"] = "normal"

def elegir_var():
    txt_var_eliminada = var_selec.get()
    if txt_var_eliminada not in vars_eliminadas:
        vars_eliminadas.append(txt_var_eliminada)

def gen_new_mat():
    global Local_Datos_Drop
    Local_Datos_Drop = Datos_Drop_New.drop(vars_eliminadas, axis=1)
    show_Data_Frame(Local_Datos_Drop,"NUEVA MATRIZ","tag_left")
    btn_mat_act["state"]="normal" 
    btn_k_means["state"] = "normal"
    btn_knee["state"] = "normal"
    btn_etiq["state"] = "normal"

vars_eliminadas = []

def select_vars():
    global var_selec
    #Se eliminan las variables que no fueron seleccionadas para un analisis posterior
    var_elegidas = list(Datos_Drop.columns)
    #Creación y definición de ventana emergente
    window_6 = tk.Toplevel(app)
    window_6.title("DESCARTAR VARIABLES")
    window_6.geometry("500x200+433+284")
    window_6.maxsize(500,200)
    window_6.configure(bg=color_fondo)
    #Label del menu
    lbl_menu_6 = tk.Label(window_6)
    lbl_menu_6["font"] =  smallfont
    lbl_menu_6["text"] = "Eliga las componentes que desea eliminar"
    lbl_menu_6["bg"] = '#CFD7FF'
    lbl_menu_6.place(x=0,y=20,width=500,height=40)
    #Menu para seleccionar la variable que se eliminara
    var_selec = tk.StringVar(window_6)
    var_selec.set(var_elegidas[0])
    menu_6 = tk.OptionMenu(window_6, var_selec, *var_elegidas)
    menu_6.place(x=50,y=70,width=230,height=40)
    txt_var_eliminada = var_selec.get()
    #Boton empleado para confirmar la eliminacion de la variable
    border_conf_6 = LabelFrame(window_6,bd = 6, bg = '#D8D8E3')
    border_conf_6.place(x=300,y=70,width=150,height=40)
    btn_conf_6 = tk.Button(window_6)
    btn_conf_6["text"] = "Confirmar"
    btn_conf_6["font"] = smallfont
    btn_conf_6["bg"] = '#D8D8E3'
    btn_conf_6["command"] = elegir_var
    btn_conf_6.place(x=305,y=75,width=140,height=30)
    #Boton para confirmar la generacion de la nueva matriz con variables eliminadas
    border_conf_7 = LabelFrame(window_6,bd = 6, bg = '#D8D8E3')
    border_conf_7.place(x=175,y=130,width=150,height=40)
    btn_conf_7 = tk.Button(window_6)
    btn_conf_7["text"] = "Generar Matriz"
    btn_conf_7["font"] = smallfont
    btn_conf_7["bg"] = '#D8D8E3'
    btn_conf_7["command"] = gen_new_mat
    btn_conf_7.place(x=180,y=135,width=140,height=30)

#Boton empleado para generar la estandarizacion de los datos
border_gen_est = LabelFrame(tab_4,bd = 6, bg = '#D8D8E3')
border_gen_est.place(x=310,y=60,width=180,height=40)
btn_gen_est = tk.Button(tab_4)
btn_gen_est["text"] = "Estandarizar Datos"
btn_gen_est["font"] = smallfont
btn_gen_est["bg"] = '#D8D8E3'
btn_gen_est["command"] = gen_estandar
btn_gen_est.place(x=315,y=65,width=170,height=30)

#Boton empleado para generar los componentes principales
border_pca = LabelFrame(tab_4,bd = 6, bg = '#D8D8E3')
border_pca.place(x=310,y=120,width=180,height=40)
btn_pca = tk.Button(tab_4)
btn_pca["text"] = "Comp. Principales"
btn_pca["font"] = smallfont
btn_pca["bg"] = '#D8D8E3'
btn_pca["command"] = gen_componentes
btn_pca["state"] = "disabled"
btn_pca.place(x=315,y=125,width=170,height=30)

#Boton empleado para generar los componentes y eigenvectores
border_eig = LabelFrame(tab_4,bd = 6, bg = '#D8D8E3')
border_eig.place(x=310,y=180,width=180,height=40)
btn_eig = tk.Button(tab_4)
btn_eig["text"] = "Eigenvalores"
btn_eig["font"] = smallfont
btn_eig["bg"] = '#D8D8E3'
btn_eig["command"] = gen_vect_PCA
btn_eig["state"] = "disabled"
btn_eig.place(x=315,y=185,width=170,height=30)

#Boton empleado para obtener la suma de varianzas
border_sum_var = LabelFrame(tab_4,bd = 6, bg = '#D8D8E3')
border_sum_var.place(x=310,y=240,width=180,height=40)
btn_sum_var = tk.Button(tab_4)
btn_sum_var["text"] = "Varianza Acumulada"
btn_sum_var["font"] = smallfont
btn_sum_var["bg"] = '#D8D8E3' 
btn_sum_var["command"] = gen_var_acumulada
btn_sum_var["state"] = "disabled"
btn_sum_var.place(x=315,y=245,width=170,height=30)

#Boton empleado para descartar las variables no deseadas
border_discard = LabelFrame(tab_4,bd = 6, bg = '#D8D8E3')
border_discard.place(x=310,y=300,width=180,height=40)
btn_discard = tk.Button(tab_4)
btn_discard["text"] = "Descartar Variables"
btn_discard["font"] = smallfont
btn_discard["bg"] = '#D8D8E3'
btn_discard["command"] = select_vars
btn_discard["state"] = "disabled"
btn_discard.place(x=315,y=305,width=170,height=30)

################################################################################################
################################################################################################
###############################        NO HABILITADA       #####################################
################################################################################################
################################################################################################
#################################### PESTAÑA DISTANCIAS ########################################
################################################################################################
################################################################################################

# def euc_dist():
#     Distancias = cdist(Datos_Drop,Datos_Drop,metric='euclidean')
#     MEuclidiana = pd.DataFrame(Distancias)
#     show_Data_Frame(MEuclidiana,"DISTANCIA EUCLIDIANA","tag_left")

# def cheby_dist():
#     Distancias = cdist(Datos_Drop,Datos_Drop,metric='chebyshev')
#     MChebyshev = pd.DataFrame(Distancias)
#     show_Data_Frame(MChebyshev,"DISTANCIA CHEBYSHEV","tag_left")

# def manh_dist():
#     Distancias = cdist(Datos_Drop,Datos_Drop,metric='cityblock')
#     MManhattan = pd.DataFrame(Distancias)
#     show_Data_Frame(MManhattan,"DISTANCIA MANHATTAN","tag_left")

# def deploy_p_value():
#     global text_7
#     #Creación y definición de ventana emergente
#     window_7 = tk.Toplevel(app)
#     window_7.title("PARAMETRO P(LAMBDA)")
#     window_7.geometry("400x150+483+309")
#     window_7.maxsize(400,150)
#     window_7.configure(bg=color_fondo)
#     #Label del menu
#     lbl_menu_7 = tk.Label(window_7)
#     lbl_menu_7["font"] =  smallfont
#     lbl_menu_7["text"] = "Inserte el valor del parametro P(Lambda) deseado"
#     lbl_menu_7["bg"] = '#CFD7FF'
#     lbl_menu_7.place(x=0,y=20,width=400,height=40)
#     #Entrada de texto para el valor del parametro P
#     text_7 = tk.Entry(window_7,justify=tk.CENTER)
#     text_7.place(x=30,y=70,width=150,height=40)
#     #Boton empleado para confirmar el valor de la variable p
#     border_conf_7 = LabelFrame(window_7,bd = 6, bg = '#D8D8E3')
#     border_conf_7.place(x=220,y=70,width=150,height=40)
#     btn_conf_7 = tk.Button(window_7)
#     btn_conf_7["text"] = "Confirmar"
#     btn_conf_7["font"] = smallfont
#     btn_conf_7["bg"] = '#D8D8E3'
#     btn_conf_7["command"] = mink_dist
#     btn_conf_7.place(x=225,y=75,width=140,height=30)

# def mink_dist():
#     int_text_7 = text_7.get()
#     try:
#         float(int_text_7)
#     except ValueError:
#         messagebox.showerror("ERROR", "Ingrese un valor valido (int) o (float)")
#     Distancias = cdist(Datos_Drop,Datos_Drop,metric='minkowski',p=float(int_text_7))
#     MMinkowski = pd.DataFrame(Distancias)
#     show_Data_Frame(MMinkowski,"DISTANCIA MINKOWSKI","tag_left")

# #Boton empleado para generar la matriz de distancia euclidiana
# border_euc = LabelFrame(tab_5,bd = 6, bg = '#D8D8E3')
# border_euc.place(x=310,y=60,width=180,height=40)
# btn_euc = tk.Button(tab_5)
# btn_euc["text"] = "Distancia Euclidiana"
# btn_euc["font"] = smallfont
# btn_euc["bg"] = '#D8D8E3'
# btn_euc["command"] = euc_dist
# btn_euc["state"] = "disabled"
# btn_euc.place(x=315,y=65,width=170,height=30)

# #Boton empleado para generar la matriz de distancia 
# border_chev = LabelFrame(tab_5,bd = 6, bg = '#D8D8E3')
# border_chev.place(x=310,y=120,width=180,height=40)
# btn_chev = tk.Button(tab_5)
# btn_chev["text"] = "Distancia Chebyshev"
# btn_chev["font"] = smallfont
# btn_chev["bg"] = '#D8D8E3'
# btn_chev["command"] = cheby_dist
# btn_chev["state"] = "disabled"
# btn_chev.place(x=315,y=125,width=170,height=30)

# #Boton empleado para generar la matriz de distancia 
# border_manh = LabelFrame(tab_5,bd = 6, bg = '#D8D8E3')
# border_manh.place(x=310,y=180,width=180,height=40)
# btn_manh = tk.Button(tab_5)
# btn_manh["text"] = "Distancia Manhattan"
# btn_manh["font"] = smallfont
# btn_manh["bg"] = '#D8D8E3'
# btn_manh["command"] = manh_dist
# btn_manh["state"] = "disabled"
# btn_manh.place(x=315,y=185,width=170,height=30)

# #Boton empleado para generar la matriz de distancia 
# border_mink = LabelFrame(tab_5,bd = 6, bg = '#D8D8E3')
# border_mink.place(x=310,y=240,width=180,height=40)
# btn_mink = tk.Button(tab_5)
# btn_mink["text"] = "Distancia Minkowski"
# btn_mink["font"] = smallfont
# btn_mink["bg"] = '#D8D8E3'
# btn_mink["command"] = deploy_p_value
# btn_mink["state"] = "disabled"
# btn_mink.place(x=315,y=245,width=170,height=30)

################################################################################################
################################################################################################
#################################### PESTAÑA CLUSTER ###########################################
################################################################################################
################################################################################################

#Se despliega la matriz actual en caso de existir.
def disply_mat_select():
    show_Data_Frame(Local_Datos_Drop,"MATRIZ ACTUAL","tag_left")

def alg_k_means():
    global SSE
    global MatrizVariables
    MatrizVariables = Local_Datos_Drop
    SSE = []
    for i in range(2, 12):
        km = KMeans(n_clusters=i, random_state=0)
        km.fit(MatrizVariables)
        SSE.append(km.inertia_)
    #Se grafica SSE en función de k
    plt.figure(figsize=(7, 7))
    plt.plot(range(2, 12), SSE, marker='o')
    plt.xlabel('CANTIDAD DE CLUSTERS *k*')
    plt.ylabel('SSE')
    plt.title('ELBOW METHOD')
    plt.show()

def knee_locator():
    kl = KneeLocator(range(2, 12), SSE, curve="convex", direction="decreasing")
    mensaje =  "El numero de clusters optimo calculado es "+str(kl.elbow)
    #plt.style.use('ggplot')
    #kl.plot_knee()    
    messagebox.showinfo("KNEE LOCATOR",mensaje)

def func_etiquetar():
    global MatrizEtiquetada
    global MParticional
    int_text_8 = text_8.get()
    try:
        int(int_text_8)
    except ValueError:
        messagebox.showerror("ERROR", "Ingrese un valor valido (int)")
    MParticional = KMeans(n_clusters=int(int_text_8), random_state=0).fit(MatrizVariables)
    MParticional.predict(MatrizVariables)
    MatrizEtiquetada = Datos
    MatrizEtiquetada['clusterP'] = MParticional.labels_
    btn_centroide["state"] = "normal"
    show_Data_Frame(MatrizEtiquetada,"MATRIZ ETIQUETADA CON CLUSTER","tag_left")
    elem_clusters = pd.DataFrame(MatrizEtiquetada.groupby(['clusterP'])['clusterP'].count())
    show_Data_Frame(elem_clusters,"NUMERO DE ELEMENTOS EN CADA CLUSTER","tag_center")

def select_k_cluster():
    global text_8
    #Creación y definición de ventana emergente
    window_8 = tk.Toplevel(app)
    window_8.title("NUMERO DE K CLUSTERS")
    window_8.geometry("400x150+483+309")
    window_8.maxsize(400,150)
    window_8.configure(bg=color_fondo)
    #Label del menu
    lbl_menu_8 = tk.Label(window_8)
    lbl_menu_8["font"] =  smallfont
    lbl_menu_8["text"] = "Inserte el numero (k) de clusters deseados"
    lbl_menu_8["bg"] = '#CFD7FF'
    lbl_menu_8.place(x=0,y=20,width=400,height=40)
    #Entrada de texto para el valor del parametro P
    text_8 = tk.Entry(window_8,justify=tk.CENTER)
    text_8.place(x=30,y=70,width=150,height=40)
    #Boton empleado para confirmar el valor de k clusters
    border_conf_8 = LabelFrame(window_8,bd = 6, bg = '#D8D8E3')
    border_conf_8.place(x=220,y=70,width=150,height=40)
    btn_conf_8 = tk.Button(window_8)
    btn_conf_8["text"] = "Confirmar"
    btn_conf_8["font"] = smallfont
    btn_conf_8["bg"] = '#D8D8E3'
    btn_conf_8["command"] = func_etiquetar
    btn_conf_8.place(x=225,y=75,width=140,height=30)

def display_centroides():
    global framed_Cent
    CentroidesP = MParticional.cluster_centers_
    framed_Cent = pd.DataFrame(CentroidesP.round(4), columns=MatrizVariables.columns)
    btn_disp_clst["state"] = "normal"
    show_Data_Frame(framed_Cent,"\nCENTROIDES\n","tag_left")

def gen_cluster_2():
    #Grafica 2D en base a dos variables de la matriz actual
    var_1 = var_graf_1.get()
    var_2 = var_graf_2.get()
    plt.figure(figsize=(10, 7))
    plt.scatter(Local_Datos_Drop[var_1], Local_Datos_Drop[var_2], c=MParticional.labels_, cmap='rainbow')
    plt.show()

def gen_cluster_3():
    #Grafica 3D en base a dos variables de la matriz actual
    var_1 = var_graf_1.get()
    var_2 = var_graf_2.get()
    var_3 = var_graf_3.get()
    plt.rcParams['figure.figsize'] = (10, 7)
    plt.style.use('ggplot')
    colores=['red', 'blue', 'cyan', 'green', 'yellow','black','purple']
    new_colors = []
    #Se retiran los colores que no seran empleados 
    for x in range(0,max(MParticional.labels_)+1):
        new_colors.append(colores[x])
    asignar=[]
    for row in MParticional.labels_:
        asignar.append(colores[row])
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(Local_Datos_Drop[var_1], Local_Datos_Drop[var_2], Local_Datos_Drop[var_3], marker='o', c=asignar, s=60)
    ax.scatter(framed_Cent[var_1], framed_Cent[var_2], framed_Cent[var_3], marker='o', c=new_colors, s=1000)
    plt.show()

def select_graf_cls():
    global var_graf_1
    global var_graf_2
    global var_graf_3
    list_vars = list(Local_Datos_Drop.columns)
    #Creación y definición de ventana emergente
    window_9 = tk.Toplevel(app)
    window_9.title("GRAFICA DE CLUSTERS")
    window_9.geometry("570x200+398+284")
    window_9.maxsize(570,200)
    window_9.configure(bg=color_fondo)
    #Label de seleccion de las variables para la grafica
    lbl_menu_9 = tk.Label(window_9)
    lbl_menu_9["font"] =  smallfont
    lbl_menu_9["text"] = "Eliga las variables que desea emplear para la grafica de clusters"
    lbl_menu_9["bg"] = '#CFD7FF'
    lbl_menu_9.place(x=0,y=20,width=500,height=40)

    #Menu para seleccionar la primera variable que se empleara
    var_graf_1 = tk.StringVar(window_9)
    var_graf_1.set(list_vars[0])
    menu_var_1 = tk.OptionMenu(window_9, var_graf_1, *list_vars)
    menu_var_1.place(x=30,y=70,width=150,height=40)

    #Menu para seleccionar la segunda variable que se empleara
    var_graf_2 = tk.StringVar(window_9)
    var_graf_2.set(list_vars[1])
    menu_var_2 = tk.OptionMenu(window_9, var_graf_2, *list_vars)
    menu_var_2.place(x=210,y=70,width=150,height=40)

    #Menu para seleccionar la tercera variable que se empleara
    var_graf_3 = tk.StringVar(window_9)
    var_graf_3.set(list_vars[2])
    menu_var_3 = tk.OptionMenu(window_9, var_graf_3, *list_vars)
    menu_var_3.place(x=390,y=70,width=150,height=40)

    #Boton empleado para confirmar la generacion de la grafica en 2D
    border_graf_2d = LabelFrame(window_9,bd = 6, bg = '#D8D8E3')
    border_graf_2d.place(x=90,y=130,width=150,height=40)
    btn_graf_2d = tk.Button(window_9)
    btn_graf_2d["text"] = "Grafica 2D"
    btn_graf_2d["font"] = smallfont
    btn_graf_2d["bg"] = '#D8D8E3'
    btn_graf_2d["command"] = gen_cluster_2
    btn_graf_2d.place(x=95,y=135,width=140,height=30)
    
    #Boton empleado para confirmar la generacion de la grafica en 3D
    border_graf_3d = LabelFrame(window_9,bd = 6, bg = '#D8D8E3')
    border_graf_3d.place(x=330,y=130,width=150,height=40)
    btn_graf_3d = tk.Button(window_9)
    btn_graf_3d["text"] = "Grafica 3D"
    btn_graf_3d["font"] = smallfont
    btn_graf_3d["bg"] = '#D8D8E3'
    btn_graf_3d["command"] = gen_cluster_3
    btn_graf_3d.place(x=335,y=135,width=140,height=30)

#Boton empleado para observar la matriz actual con las variables ya eliminadas
border_mat_act = LabelFrame(tab_6,bd = 6, bg = '#D8D8E3')
border_mat_act.place(x=310,y=20,width=180,height=40)
btn_mat_act = tk.Button(tab_6)
btn_mat_act["text"] = "Matriz Actual"
btn_mat_act["font"] = smallfont
btn_mat_act["bg"] = '#D8D8E3'
btn_mat_act["command"] = disply_mat_select
btn_mat_act["state"] = "disabled"
btn_mat_act.place(x=315,y=25,width=170,height=30)

#Boton empleado para el algoritmo k-means
border_k_means = LabelFrame(tab_6,bd = 6, bg = '#D8D8E3')
border_k_means.place(x=310,y=80,width=180,height=40)
btn_k_means = tk.Button(tab_6)
btn_k_means["text"] = "K-Means"
btn_k_means["font"] = smallfont
btn_k_means["bg"] = '#D8D8E3'
btn_k_means["command"] = alg_k_means
btn_k_means["state"] = "disabled"
btn_k_means.place(x=315,y=85,width=170,height=30)

#Boton empleado para usar knee locatos
border_knee = LabelFrame(tab_6,bd = 6, bg = '#D8D8E3')
border_knee.place(x=310,y=140,width=180,height=40)
btn_knee = tk.Button(tab_6)
btn_knee["text"] = "Knee Locator"
btn_knee["font"] = smallfont
btn_knee["bg"] = '#D8D8E3'
btn_knee["command"] = knee_locator
btn_knee["state"] = "disabled"
btn_knee.place(x=315,y=145,width=170,height=30)

#Boton empleado para usar knee locatos
border_etiq = LabelFrame(tab_6,bd = 6, bg = '#D8D8E3')
border_etiq.place(x=310,y=200,width=180,height=40)
btn_etiq = tk.Button(tab_6)
btn_etiq["text"] = "Etiquetar"
btn_etiq["font"] = smallfont
btn_etiq["bg"] = '#D8D8E3'
btn_etiq["command"] = select_k_cluster
btn_etiq["state"] = "disabled"
btn_etiq.place(x=315,y=205,width=170,height=30)

#Boton empleado para usar knee locatos
border_centroide = LabelFrame(tab_6,bd = 6, bg = '#D8D8E3')
border_centroide.place(x=310,y=260,width=180,height=40)
btn_centroide = tk.Button(tab_6)
btn_centroide["text"] = "Centroides"
btn_centroide["font"] = smallfont
btn_centroide["bg"] = '#D8D8E3'
btn_centroide["command"] = display_centroides
btn_centroide["state"] = "disabled"
btn_centroide.place(x=315,y=265,width=170,height=30)

#Boton empleado para usar knee locatos
border_disp_clst = LabelFrame(tab_6,bd = 6, bg = '#D8D8E3')
border_disp_clst.place(x=310,y=320,width=180,height=40)
btn_disp_clst = tk.Button(tab_6)
btn_disp_clst["text"] = "Grafica de Clusters"
btn_disp_clst["font"] = smallfont
btn_disp_clst["bg"] = '#D8D8E3'
btn_disp_clst["command"] = select_graf_cls
btn_disp_clst["state"] = "disabled"
btn_disp_clst.place(x=315,y=325,width=170,height=30)

################################################################################################
################################################################################################
#################################### PESTAÑA CLASIFICACION #####################################
################################################################################################
################################################################################################

################### Variables empleadas para la seleccion de variables predictorias ############
vars_clasificacion_entrenamiento = []

def elegir_var_clasificacion():
    txt_var_seleccionada = var_selec_clasificacion.get()
    if txt_var_seleccionada not in vars_clasificacion_entrenamiento:
        vars_clasificacion_entrenamiento.append(txt_var_seleccionada)

def gen_mat_clasificacion():
    global X_Variables_Predictorias
    Variables_Predictorias = Datos[vars_clasificacion_entrenamiento]
    X_Variables_Predictorias = np.array(Datos[vars_clasificacion_entrenamiento])
    show_Data_Frame(Variables_Predictorias,"VARIABLES PREDICTORIAS","tag_left")

def select_vars_clasificacion():
    global var_selec_clasificacion
    #Se obtienen todas las columnas de los datos ya que no se sabe cual de ellas 
    #sera empleada o cuyos valores se reemplezaran 
    var_elegidas = list(Datos.columns)
    #Creación y definición de ventana emergente
    window_10 = tk.Toplevel(app)
    window_10.title("ELEGIR VARIABLES PREDICTORIAS")
    window_10.geometry("500x200+433+284")
    window_10.maxsize(500,200)
    window_10.configure(bg=color_fondo)
    #Label del menu
    lbl_menu_10 = tk.Label(window_10)
    lbl_menu_10["font"] =  smallfont
    lbl_menu_10["text"] = "Eliga las variables que desea emplear como variables predictorias"
    lbl_menu_10["bg"] = '#CFD7FF'
    lbl_menu_10.place(x=0,y=20,width=500,height=40)
    #Menu para seleccionar la variable que se eliminara
    var_selec_clasificacion = tk.StringVar(window_10)
    var_selec_clasificacion.set(var_elegidas[0])
    menu_10 = tk.OptionMenu(window_10, var_selec_clasificacion, *var_elegidas)
    menu_10.place(x=50,y=70,width=230,height=40)
    txt_var_eliminada = var_selec_clasificacion.get()
    #Boton empleado para confirmar la eliminacion de la variable
    border_conf_10 = LabelFrame(window_10,bd = 6, bg = '#D8D8E3')
    border_conf_10.place(x=300,y=70,width=150,height=40)
    btn_conf_10 = tk.Button(window_10)
    btn_conf_10["text"] = "Confirmar"
    btn_conf_10["font"] = smallfont
    btn_conf_10["bg"] = '#D8D8E3'
    btn_conf_10["command"] = elegir_var_clasificacion
    btn_conf_10.place(x=305,y=75,width=140,height=30)
    #Boton para confirmar la generacion de la nueva matriz con variables eliminadas
    border_conf_11 = LabelFrame(window_10,bd = 6, bg = '#D8D8E3')
    border_conf_11.place(x=175,y=130,width=150,height=40)
    btn_conf_11 = tk.Button(window_10)
    btn_conf_11["text"] = "Generar Matriz"
    btn_conf_11["font"] = smallfont
    btn_conf_11["bg"] = '#D8D8E3'
    btn_conf_11["command"] = gen_mat_clasificacion
    btn_conf_11.place(x=180,y=135,width=140,height=30)

################### Variables empleadas para la seleccion de variable predecida ############

vars_clasificacion_prediccion = []


def actualiza_datos(value_0,value_1):
    Datos_Retagged.replace({value_0:0,value_1:1})

def confirmar_sustitucion():
    global Data_Retagged
    value_0 = text_var_0.get()
    value_1 = text_var_1.get()
    if(value_0 == ""):
        messagebox.showerror("ERROR", "Entrada para sustituir valor 0 invalida")
    elif(value_1 == ""):
        messagebox.showerror("ERROR", "Entrada para sustituir valor 1 invalida")
    #Se realiza la sustitucion de variables si no ocurrio un error
    Data_Retagged = Datos_Retagged.replace({value_0:0,value_1:1})
    actualiza_datos(value_0,value_1)
    vars_clasificacion_prediccion.append(txt_var_prediccion)
    show_Data_Frame(Data_Retagged,"DATOS REETIQUETADOS","tag_left")

def replace_tags(txt_variable):
    global text_var_0
    global text_var_1
    tipo = Datos[txt_variable].dtypes
    window_replace = tk.Toplevel(app)
    window_replace.title("SUSTITUCION VARIABLE PREDECIDA")
    window_replace.geometry("500x240+433+284")
    window_replace.maxsize(500,240)
    window_replace.configure(bg=color_fondo)
    #Label del menu
    lbl_menu_replace = tk.Label(window_replace)
    lbl_menu_replace["font"] =  smallfont
    cadena = "La variable seleccionada es de tipo "+str(tipo)+"\n"+\
             "Es necesario realiza una sustitucion de variables"
    lbl_menu_replace["text"] = cadena
    lbl_menu_replace["bg"] = '#CFD7FF'
    lbl_menu_replace.place(x=0,y=20,width=500,height=40)
    
    #Seleccion de la variable que sera reemplazada con 0
    lbl_valor_0 = tk.Label(window_replace)
    lbl_valor_0["font"] =  smallfont
    cadena_0 = "Valor actual de la variable que tomara el valor 0: "
    lbl_valor_0["text"] = cadena_0
    lbl_valor_0["bg"] = '#CFD7FF'
    lbl_valor_0.place(x=30,y=70,width=300,height=40)
    #Entrada de texto para el valor de la variable a reemplazar
    text_var_0 = tk.Entry(window_replace,justify=tk.CENTER)
    text_var_0.place(x=360,y=70,width=100,height=40)

    #Seleccion de la variable que sera reemplazada con 1
    lbl_valor_1 = tk.Label(window_replace)
    lbl_valor_1["font"] =  smallfont
    cadena_1 = "Valor actual de la variable que tomara el valor 1: "
    lbl_valor_1["text"] = cadena_1
    lbl_valor_1["bg"] = '#CFD7FF'
    lbl_valor_1.place(x=30,y=120,width=300,height=40)
    #Entrada de texto para el valor de la variable a reemplazar
    text_var_1 = tk.Entry(window_replace,justify=tk.CENTER)
    text_var_1.place(x=360,y=120,width=100,height=40)

    #Boton empleada para confirmar la sustitucion
    border_conf_replace = LabelFrame(window_replace,bd = 6, bg = '#D8D8E3')
    border_conf_replace.place(x=175,y=180,width=150,height=40)
    btn_conf_replace = tk.Button(window_replace)
    btn_conf_replace["text"] = "Sustituir"
    btn_conf_replace["font"] = smallfont
    btn_conf_replace["bg"] = '#D8D8E3'
    btn_conf_replace["command"] = confirmar_sustitucion
    btn_conf_replace.place(x=180,y=185,width=140,height=30)

def elegir_var_prediccion():
    global txt_var_prediccion
    txt_var_prediccion = var_selec_predecir.get()
    if txt_var_prediccion not in vars_clasificacion_prediccion:
        #Se verifica que se eliga una sola variable que se desea predecir
        if len(vars_clasificacion_prediccion) == 0:
            #En caso de que no se hayan seleccionado variables de forma previa, se verifica
            #que la variable seleccionada sea de tipo entero
            tipo = Datos[txt_var_prediccion].dtypes
            if tipo != np.int64 or tipo!= np.float64:
                replace_tags(txt_var_prediccion)
            else:
                vars_clasificacion_prediccion.append(txt_var_prediccion)
        elif len(vars_clasificacion_prediccion) > 0:
            mensaje_error = "Solo es posible predecir una variable.\nSe ha elegido la variable "+str(vars_clasificacion_prediccion[0])
            messagebox.showerror("ERROR",mensaje_error)

def gen_mat_prediccion():
    global Y_Variable_Predecida
    Variable_Predecida = Data_Retagged[vars_clasificacion_prediccion]
    Y_Variable_Predecida = np.array(Data_Retagged[vars_clasificacion_prediccion])
    show_Data_Frame(Variable_Predecida,"VARIABLE PREDECIDA","tag_center")

def select_var_prediccion():
    global var_selec_predecir
    #Se obtienen todas las columnas de los datos ya que no se sabe cual de ellas 
    #sera empleada o cuyos valores se reemplezaran 
    var_elegidas = list(Datos.columns)
    #Creación y definición de ventana emergente
    window_11 = tk.Toplevel(app)
    window_11.title("ELEGIR VARIABLE PREDECIDA")
    window_11.geometry("500x200+433+284")
    window_11.maxsize(500,200)
    window_11.configure(bg=color_fondo)
    #Label del menu
    lbl_menu_12 = tk.Label(window_11)
    lbl_menu_12["font"] =  smallfont
    lbl_menu_12["text"] = "Eliga la variable que desea predecir (Debe ser una variable binaria o\n \
                            con etiquetas que puedan ser sustituidas por valores binarios)"
    lbl_menu_12["bg"] = '#CFD7FF'
    lbl_menu_12.place(x=0,y=20,width=500,height=40)
    #Menu para seleccionar la variable que se eliminara
    var_selec_predecir = tk.StringVar(window_11)
    var_selec_predecir.set(var_elegidas[0])
    menu_11 = tk.OptionMenu(window_11, var_selec_predecir, *var_elegidas)
    menu_11.place(x=50,y=70,width=230,height=40)
    #Boton empleado para confirmar la eliminacion de la variable
    border_conf_12 = LabelFrame(window_11,bd = 6, bg = '#D8D8E3')
    border_conf_12.place(x=300,y=70,width=150,height=40)
    btn_conf_12 = tk.Button(window_11)
    btn_conf_12["text"] = "Confirmar"
    btn_conf_12["font"] = smallfont
    btn_conf_12["bg"] = '#D8D8E3'
    btn_conf_12["command"] = elegir_var_prediccion
    btn_conf_12.place(x=305,y=75,width=140,height=30)
    #Boton para confirmar la generacion de la nueva matriz con variables eliminadas
    border_conf_13 = LabelFrame(window_11,bd = 6, bg = '#D8D8E3')
    border_conf_13.place(x=175,y=130,width=150,height=40)
    btn_conf_13 = tk.Button(window_11)
    btn_conf_13["text"] = "Mostrar Datos"
    btn_conf_13["font"] = smallfont
    btn_conf_13["bg"] = '#D8D8E3'
    btn_conf_13["command"] = gen_mat_prediccion
    btn_conf_13.place(x=180,y=135,width=140,height=30)

def show_reporte_clas(X_validation,Y_validation,PrediccionesNuevas):
    #Matriz de clasificacion 
    PrediccionesNuevas = Clasificacion.predict(X_validation)
    confusion_matrix = pd.crosstab(Y_validation.ravel(),PrediccionesNuevas,rownames=['Real'],colnames=['Clasificacion'])
    data = pd.DataFrame(confusion_matrix)
    cadena = str(data)
    #Se obtiene los casos de falsos positivos y negativos
    v_positivo = data[1].iloc[1]
    f_positivo = data[1].iloc[0]
    v_negativo = data[0].iloc[0]
    f_negativo = data[0].iloc[1]
    casos_totales = v_positivo+f_positivo+v_negativo+f_negativo

    cadena += "\n\nCASOS TOTALES: "
    cadena += str(casos_totales)
    cadena += "\nVERDADERO POSITIVO: "
    cadena += str(v_positivo)
    cadena += "\nFALSO POSITIVO: "
    cadena += str(f_positivo)
    cadena += "\nVERDADERO NEGATIVO: "
    cadena += str(v_negativo)
    cadena += "\nFALSO NEGATIVO: "
    cadena += str(f_negativo)
    cadena += "\n\n"

    #Reporte de clasificacion
    cadena += "Exactitud\n"
    cadena += str(Clasificacion.score(X_validation,Y_validation))
    cadena += "\n\n"
    cadena += str(classification_report(Y_validation,PrediccionesNuevas))

    #Se obtienen los coeficientes de exactitud, precision, especificidad, sensibilidad
    exactitud = (v_positivo+v_negativo)/(v_positivo+v_negativo+f_positivo+f_negativo)
    tasa_e = (f_positivo+f_negativo)/(casos_totales)
    precision = (v_positivo)/(v_positivo+f_positivo)
    especificidad = (v_negativo)/(v_negativo+f_positivo)
    sensibilidad = (v_positivo)/(v_positivo+f_negativo)
    #Se despliegan los valores obtenidos
    cadena += "\n\nReporte de clasificación del modelo\n\n"
    cadena += "EXACTITUD: {:.3f}".format(exactitud)
    cadena += "\nTASA DE ERROR: {:.3f}".format(tasa_e)
    cadena += "\nPRECISION: {:.3f}".format(precision)
    cadena += "\nESPECIFICIDAD: {:.3f}".format(especificidad)
    cadena += "\nSENSIBILIDAD: {:.3f}".format(sensibilidad)
    cadena += "\n\n\n"
    show_Data_Frame(cadena,"\n\n\nCONFUSION MATRIX","tag_center")
    #Se habilita la pestaña de prediccion
    notebook.tab(6,state="normal")

def gen_modelo():
    global Clasificacion
    #Se declara el modelo de regresion logistica
    Clasificacion = linear_model.LogisticRegression()
    #inicializa un generador de numeros aleatorios para recuperar registros 
    #de forma aleatoria para el entrenameinto y prueba del algoritmo.
    int_porcentaje = text_porcentaje.get()
    try:
        int(int_porcentaje)
    except ValueError:
        messagebox.showerror("ERROR", "Ingrese un valor valido (int) entre 10 y 100")
    float_porcentaje = float(int_porcentaje)/100
    print(float_porcentaje)
    seed = 1234
    X_train, X_validation,Y_train,Y_validation = model_selection.train_test_split(X_Variables_Predictorias,Y_Variable_Predecida,test_size=float_porcentaje,random_state = seed, shuffle = True)
    Clasificacion.fit(X_train,Y_train)
    Probabilidad = Clasificacion.predict_proba(X_train)
    Predicciones = Clasificacion.predict(X_train)
    Clasificacion.score(X_train,Y_train)
    PrediccionesNuevas = Clasificacion.predict(X_validation)
    #confusion_matrix = pd.crosstab(Y_validation.ravel(),PrediccionesNuevas,rownames=['Real'],colnames=['Clasificacion'])
    show_reporte_clas(X_validation,Y_validation,PrediccionesNuevas)

def def_modelo():
    global text_porcentaje
    window_modelo = tk.Toplevel(app)
    window_modelo.title("GENERAR MODELO")
    window_modelo.geometry("500x200+433+284")
    window_modelo.maxsize(500,200)
    window_modelo.configure(bg=color_fondo)
    #Label del menu
    lbl_modelo = tk.Label(window_modelo)
    lbl_modelo["font"] =  smallfont
    cadena = "Ingrese el porcentaje de datos que se desea emplear en la\n prueba del modelo (Recomendado 20%)"
    lbl_modelo["text"] = cadena
    lbl_modelo["bg"] = '#CFD7FF'
    lbl_modelo.place(x=0,y=20,width=500,height=40)
    #Entrada de texto para el porcentaje de datos
    text_porcentaje = tk.Entry(window_modelo,justify=tk.CENTER)
    text_porcentaje.place(x=200,y=70,width=100,height=40)
    #Boton para confirmar la generacion del modelo
    border_conf_modelo = LabelFrame(window_modelo,bd = 6, bg = '#D8D8E3')
    border_conf_modelo.place(x=175,y=130,width=150,height=40)
    btn_conf_modelo = tk.Button(window_modelo)
    btn_conf_modelo["text"] = "Generar Modelo"
    btn_conf_modelo["font"] = smallfont
    btn_conf_modelo["bg"] = '#D8D8E3'
    btn_conf_modelo["command"] = gen_modelo
    btn_conf_modelo.place(x=180,y=135,width=140,height=30)

def gen_ecuacion():
    cadena = "\n\n"
    cadena += "COEFICIENTES DE LA ECUACIÓN\n\n"
    #Ecuacion del modelo
    cadena += "Intercept: "
    cadena += str(Clasificacion.intercept_[0])
    cadena += "\n\n"
    cadena += 'Coeficientes:\n\n'
    ecuacion_formateada = "a+bX = "
    ecuacion_formateada += "{:.4f}".format(Clasificacion.intercept_[0])
    ecuacion_formateada += "\n"
    #Se obtiene una lista del coeficiente y su variable asociada
    for x in range (0,len(Clasificacion.coef_[0])):
        cadena += "Variable: "
        cadena += vars_clasificacion_entrenamiento[x]
        cadena += "\n"
        cadena += "Coeficiente: "
        cadena += str(Clasificacion.coef_[0][x])
        cadena +="\n\n"
        ecuacion_formateada += "{:.4f}".format(Clasificacion.coef_[0][x])
        ecuacion_formateada += "*"
        ecuacion_formateada += vars_clasificacion_entrenamiento[x]
        ecuacion_formateada += "\n"
    cadena += "\nECUACION DE LA FORMA Y = A + BX\n\n"
    cadena += ecuacion_formateada
    cadena += "\n\n"
    show_Data_Frame(cadena,"\n\nECUACIÓN DEL MODELO","tag_center")

#Boton empleado para seleccionar las variables predictorias
border_var_predic = LabelFrame(tab_7,bd = 6, bg = '#D8D8E3')
border_var_predic.place(x=310,y=60,width=180,height=40)
btn_var_predic = tk.Button(tab_7)
btn_var_predic["text"] = "Variables Predictorias"
btn_var_predic["font"] = smallfont
btn_var_predic["bg"] = '#D8D8E3'
btn_var_predic["command"] = select_vars_clasificacion
btn_var_predic.place(x=315,y=65,width=170,height=30)

#Boton empleado para seleccionar la variable a predecir
border_var_predecir = LabelFrame(tab_7,bd = 6, bg = '#D8D8E3')
border_var_predecir.place(x=310,y=120,width=180,height=40)
btn_var_predecir = tk.Button(tab_7)
btn_var_predecir["text"] = "Variable Predecida"
btn_var_predecir["font"] = smallfont
btn_var_predecir["bg"] = '#D8D8E3'
btn_var_predecir["command"] = select_var_prediccion
btn_var_predecir.place(x=315,y=125,width=170,height=30)

#Boton empleado para generar el modelo de regresion logistica
border_modelo = LabelFrame(tab_7,bd = 6, bg = '#D8D8E3')
border_modelo.place(x=310,y=180,width=180,height=40)
btn_var_modelo = tk.Button(tab_7)
btn_var_modelo["text"] = "Generar Modelo"
btn_var_modelo["font"] = smallfont
btn_var_modelo["bg"] = '#D8D8E3'
btn_var_modelo["command"] = def_modelo
btn_var_modelo.place(x=315,y=185,width=170,height=30)

#Boton empleado para generar la ecuacion del modelo
border_ecuacion = LabelFrame(tab_7,bd = 6, bg = '#D8D8E3')
border_ecuacion.place(x=310,y=240,width=180,height=40)
btn_ecuacion = tk.Button(tab_7)
btn_ecuacion["text"] = "Mostrar Ecuación"
btn_ecuacion["font"] = smallfont
btn_ecuacion["bg"] = '#D8D8E3'
btn_ecuacion["command"] = gen_ecuacion
btn_ecuacion.place(x=315,y=245,width=170,height=30)

################################################################################################
################################################################################################
#################################### PESTAÑA PREDICCION ########################################
################################################################################################
################################################################################################

def gen_prediccion():
    #Primero se verifica que el diccionario de datos contenga
    #la cantidad de datos adecuada, es decir la misma cantidad que el 
    #numero de variables predictorias
    if len(Diccionario_Datos) < len(vars_clasificacion_entrenamiento):
        messagebox.showerror("ERROR", "No se han definido todos los valores necesarios")
    else:
        Diccionario_Datos_Framed = pd.DataFrame(Diccionario_Datos)
        Prediccion = Clasificacion.predict(Diccionario_Datos_Framed)
        cadena = "\n\n"
        cadena += "En base a los datos: \n\n"
        for x in range(0,len(Diccionario_Datos)):
            key_var = vars_clasificacion_entrenamiento[x]
            cadena += "Variable: "
            cadena += str(key_var)
            cadena += "\n"
            cadena += "Valor: "
            cadena += str(Diccionario_Datos[key_var][0])
            cadena += "\n\n"
        cadena += "El valor predecido para la variable "
        cadena += str(vars_clasificacion_prediccion[0])
        cadena += " es: "
        cadena += str(Prediccion[0])
        cadena += "\n\n\n"
        show_Data_Frame(cadena,"\n\nRESULTADOS DE LA PREDICCIÓN","tag_center")

Diccionario_Datos = {}
def act_datos_pred():
    float_input = text_pred_var.get()
    try:
        float(float_input)
    except ValueError:
        messagebox.showerror("ERROR", "Ingrese un valor valido (float o int)")
    new_data = float(float_input)
    #Se añade o reemplaza el valor de la varible en el diccionario de datos
    #Primero se selecciona la llave que corresponde a la variable seleccionada en el momento 
    key_var = valores_val_prediccion.get()
    data_list = []
    data_list.append(new_data)
    Diccionario_Datos[key_var] = data_list

def insert_values_pred():
    global valores_val_prediccion
    global text_pred_var
    #Creación y definición de ventana emergente
    window = tk.Toplevel(app)
    window.title("INSERTAR VALORES PARA PREDICCION")
    window.geometry("500x200+433+284")
    window.maxsize(500,200)
    window.configure(bg=color_fondo)
    #Label del menu
    lbl_menu = tk.Label(window)
    lbl_menu["font"] =  smallfont
    lbl_menu["text"] = "Ingrese el valor para cada variable"
    lbl_menu["bg"] = '#CFD7FF'
    lbl_menu.place(x=0,y=20,width=500,height=40)
    #Menu para seleccionar la variable
    valores_val_prediccion = tk.StringVar(window)
    valores_val_prediccion.set(vars_clasificacion_entrenamiento[0])
    menu_var = tk.OptionMenu(window, valores_val_prediccion, *vars_clasificacion_entrenamiento)
    menu_var.place(x=50,y=70,width=230,height=40)
    #Entrada de texto para el valor de la variable elegida en el men
    text_pred_var = tk.Entry(window,justify=tk.CENTER)
    text_pred_var.place(x=330,y=70,width=120,height=40)
    #Boton empleado para confirmar el valor de la variable
    border_1 = LabelFrame(window,bd = 6, bg = '#D8D8E3')
    border_1.place(x=70,y=130,width=150,height=40)
    btn_conf_1 = tk.Button(window)
    btn_conf_1["text"] = "Ingresar valor"
    btn_conf_1["font"] = smallfont
    btn_conf_1["bg"] = '#D8D8E3'
    btn_conf_1["command"] = act_datos_pred
    btn_conf_1.place(x=75,y=135,width=140,height=30)
    #Boton para confirmar la generacion de la nueva matriz con variables eliminadas
    border_2 = LabelFrame(window,bd = 6, bg = '#D8D8E3')
    border_2.place(x=280,y=130,width=150,height=40)
    btn_conf_2 = tk.Button(window)
    btn_conf_2["text"] = "Obtener Predicción    "
    btn_conf_2["font"] = smallfont
    btn_conf_2["bg"] = '#D8D8E3'
    btn_conf_2["command"] = gen_prediccion
    btn_conf_2.place(x=285,y=135,width=140,height=30)

#Label con el titulo de la pestaña
lbl_titulo_pred = tk.Label(tab_8)
lbl_titulo_pred["text"] = "Predicción de Valores"
lbl_titulo_pred["font"] = fontTitle
lbl_titulo_pred["bg"] = '#CFD7FF'
lbl_titulo_pred.place(x=0,y=40,width=800,height=40)

#Label con la descripcion para insertar datos 
descripcion_vals_pred = "Presione el botón Insertar Valores para añadir los valores \n\
deseados y obtener una predicción del campo seleccionado\n" 
lbl_vals_pred = tk.Label(tab_8)
lbl_vals_pred["text"] = descripcion_vals_pred
lbl_vals_pred["font"] =  pathFont
lbl_vals_pred["bg"] = '#CFD7FF'
lbl_vals_pred.place(x=0,y=130,width=800,height=60)

#Boton empleado para ingresar los datos correspondientes a cada campo de las variables
#seleccionadas para la prediccion 
border_vals_pred = LabelFrame(tab_8,bd = 6, bg = '#D8D8E3')
border_vals_pred.place(x=310,y=230,width=180,height=40)
btn_vals_pred = tk.Button(tab_8)
btn_vals_pred["text"] = "Insertar Valores"
btn_vals_pred["font"] = smallfont
btn_vals_pred["bg"] = '#D8D8E3'
btn_vals_pred["command"] = insert_values_pred
btn_vals_pred.place(x=315,y=235,width=170,height=30)

app.mainloop()