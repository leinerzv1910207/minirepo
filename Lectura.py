import pandas as pd
import math
import Extras

# Leemos el Excel de datos.

def Configuracion ():
    
    # Leemos los valores del excel.
    CONFIG = pd.read_excel('data_io2.xlsx', sheet_name='CONFIG')
    
    # Extraemos los valores que nos interesan.
    Error = CONFIG.iloc [5,1]
    Max_Iter = CONFIG.iloc [6,1]
    GS = CONFIG.iloc  [0,1]
    NR = CONFIG.iloc  [1,1]
    FD = CONFIG.iloc  [2,1]
    DC = CONFIG.iloc  [3,1]
    
    return Error, Max_Iter, GS, NR, FD, DC

def Lineas (): 
    
    # Leemos los valores del excel.
    Lineas = pd.read_excel('data_io2.xlsx', sheet_name='LINES')
    
    # Eliminamos las barras que esten apagadas, para simplificar la cuentas.
    Lineas = Lineas[Lineas.iloc[:, 0] != 'OFF']
    
    # Ordenamos la columna Bus i, por si hace falta.
    Lineas = Lineas.sort_values(by='Bus i')
    
    # Extraemos los valores que nos interesan.     
    Barra_i_lineas = Lineas ['Bus i']
    Barra_j_lineas = Lineas ['Bus j']
    Bshunt_lineas =  Lineas ['Bshunt (p.u.)']
    R_Lineas = Lineas ['R (pu)']
    X_Lineas = Lineas ['X (p.u.)']
    
    return Barra_i_lineas, Barra_j_lineas, Bshunt_lineas, R_Lineas, X_Lineas

def Cargas ():
    
    # Leemos los datos del excel.
    Elementos_Tierra = pd.read_excel('data_io2.xlsx', sheet_name='SHUNT_ELEMENTS')
    
    # Ordenamos la columna Bus i, por si hace falta.
    Elementos_Tierra = Elementos_Tierra.sort_values(by='Bus i')
    
    # Eliminamos las barras que esten apagadas, para simplificar la cuentas.
    Elementos_Tierra = Elementos_Tierra[Elementos_Tierra.iloc[:, 0] != 'OFF'] 
    
    # Extraemos los elementos que nos interesa.
    
    BUS_I = Elementos_Tierra ['Bus i']
    R_tierra = Elementos_Tierra ['R (pu)']
    X_tierra = Elementos_Tierra ['X (pu)']
    
    return BUS_I, R_tierra, X_tierra

def Barras ():
    
    # Leemos los datos del excel.
    Barras = pd.read_excel('data_io2.xlsx', sheet_name='BUS')
    
    # Ordenamos la columna Bus i, por si hace falta.
    Barras = Barras.sort_values(by='ID')
    
    # Eliminamos las barras que esten apagadas, para simplificar la cuentas.
    Barras = Barras[Barras.iloc[:, 0] != 'OFF'] 
    
    # Extraimos los datos que necesitamos. 
    Bus_i_Barras = Barras ['Bus i']
    Tipo_Barra = Barras ['Bus type']
    Modulo_V = Barras ['|V| (pu)']
    Angulo_grados = Barras ['<V (degrees)']
    P_generada = Barras['Pgen (pu)']
    Q_generada = Barras['Qgen (pu)'] * 1j
    P_demanda = Barras['Po load (pu)']
    Q_demanda = Barras['Qo load (pu)'] * 1j
    Z_zip = Barras['%Z']
    I_zip = Barras['%I']
    P_zip = Barras['%P']
    
    #Listas con las diferencias entre varriable y constante
    difV = []
    difA= []

    # Bucle para Modulo_V: Si el valor es 0 o None, reemplaza con 1
    for i in range(len(Modulo_V)):
        if Modulo_V[i] == 0 or Modulo_V[i] is None:
            Modulo_V[i] = 1
            difV.append(False)
        else:
            difV.append(True)
            
    # Bucle para Angulo_grados: Si el valor es None, reemplaza con 0
    for i in range(len(Angulo_grados)):
        if math.isnan(Angulo_grados[i]):
            Angulo_grados[i] = 0
            difA.append(False)
        else:
            difA.append(True)
    
    return Bus_i_Barras,Tipo_Barra, Modulo_V, Angulo_grados,P_generada ,  Q_generada ,  P_demanda , Q_demanda,Z_zip,I_zip, P_zip, difV, difA
