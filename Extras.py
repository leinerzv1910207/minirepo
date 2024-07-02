import pandas as pd
import numpy as np
import itertools
# ======================================== Sección de Matriz de incidencia Nodal ====================================   
def Incidencia_Nodal (Barra_i_lineas, Barra_j_lineas,BUS_I):
    # Seleccionamos los valores de datos.
    Barra_i = Barra_i_lineas
    Barra_j = Barra_j_lineas
    BUS_I = BUS_I
    # Encuentra el valor máximo entre ambas listas.
    max_value = len(Barra_i)
    # Filtrar las líneas con BUS_I diferente de cero.
    Salida = len (BUS_I)
    # Filas Totales con las conexiones a tierra.
    Filas_totales = (max_value + Salida)
    # Crea una matriz de ceros con el tamaño máximo.
    MatrizA = np.zeros((Filas_totales, max_value))
    # Inicializar el contador para las conexiones a tierra
        
    contador_tierra = len(Barra_i)  # Comienza después del último valor de Bus i
    # Llenar la matriz según las conexiones. 
        
    # Combinar las listas con zip_longest
    for idx, (valor_i, valor_j) in enumerate(itertools.zip_longest(Barra_i, Barra_j, fillvalue=None)):
        if valor_i is not None and valor_j is not None:
            # Realiza las operaciones necesarias con los valores
            Barra_i = int(valor_i)
            Barra_j = int(valor_j)
            MatrizA[idx, Barra_i - 1] = (1)
            MatrizA[idx, Barra_j - 1] = (-1)
    # Manejo de conexiones a tierra (si es necesario)
    for contador_tierrax, BUS_I in enumerate(BUS_I):
        BUS_I = int(BUS_I)
        MatrizA[contador_tierra, BUS_I - 1] = 1
        contador_tierra += 1
        
    return MatrizA
def Z_rama (Barra_i_lineas, Barra_j_lineas, Bshunt_lineas, R_Lineas, X_Lineas, BUS_I, R_tierra, X_tierra):
        # Extramos las columnas que deseamos.
        Barra_i = Barra_i_lineas
        Barra_j = Barra_j_lineas
        Bshunt =  Bshunt_lineas
        BUS_I = BUS_I
        R_Lineas = R_Lineas
        X_Lineas = X_Lineas
        R_tierra = R_tierra
        X_tierra = X_tierra
        
        if BUS_I.empty:
            
            # Encuentra el valor máximo entre ambas listas.
            max_value = max(int(max(Barra_i)), int(max(Barra_j)))
            # Filas Totales con las conexiones a tierra.
            Filas_totales = (max_value)
            
            # Crea una matriz de ceros con el tamaño máximo.
            MatrizZ_RAMA = np.zeros((Filas_totales, Filas_totales), dtype= complex)
            # Seleccionamos los parametros deseados.
            Z_lineas = R_Lineas + X_Lineas* 1j
            
            Y_lineas = np.reciprocal(Z_lineas)
            
            # Crear la nueva lista combinando Z_lineas y Z_cargas
            Z_total = list(Y_lineas)
            # Actualizar la diagonal principal de MatrizZ_RAMA con los valores de nueva_lista
            for i in range(Filas_totales):
                MatrizZ_RAMA[i, i] = Z_total[i]
            
            
            
        
        else:
            # Encuentra el valor máximo entre ambas listas.
            max_value = max(int(max(Barra_i)), int(max(Barra_j)))
            
            # Filtrar las líneas con BUS_I diferente de cero.
            Salida = np.count_nonzero (BUS_I)
            # Filas Totales con las conexiones a tierra.
            Filas_totales = (max_value + Salida)
            # Crea una matriz de ceros con el tamaño máximo.
            MatrizZ_RAMA = np.zeros((Filas_totales, Filas_totales), dtype= complex)
            # Seleccionamos los parametros deseados.
            Z_lineas = R_Lineas + X_Lineas* 1j
            Z_cargas = R_tierra + X_tierra*1j
            # Crear la nueva lista combinando Z_lineas y Z_cargas
            Z_total = list(Z_lineas) + list(Z_cargas)

            Z_total = np.reciprocal(Z_total)
            #Z_total = np.reciprocal(Z_total)

            # Actualizar la diagonal principal de MatrizZ_RAMA con los valores de nueva_lista
            for i in range(Filas_totales):
                MatrizZ_RAMA[i, i] = Z_total[i]

            MatrizZ_RAMA = np.invert(MatrizZ_RAMA)

        return MatrizZ_RAMA

def Y_BUS (Matriz_A, Z_rama):
    A_T = np.transpose(Matriz_A)
    
    y_bus = A_T@Z_rama@Matriz_A    
    return y_bus