import numpy as np
import Lectura
import Extras
import math
import GAUSS
import time
import sympy as sp
from Calculos import Calcular_P
from Calculos import Calcular_Q

# Marcamos el inicio del tiempo de la rutina.
inicio = time.time()

Error, Max_Iter,GS,NR,FD,DC = Lectura.Configuracion ()

Barra_i_lineas, Barra_j_lineas, Bshunt_lineas, R_Lineas, X_Lineas = Lectura.Lineas ()

BUS_I, R_tierra, X_tierra = Lectura.Cargas ()

Bus_i_Barras,Tipo_Barra, Modulo_V, Angulo_grados,P_generada ,  Q_generada ,  P_demanda , Q_demanda,Z_zip,I_zip, P_zip, difV, difA = Lectura.Barras ()

""" Creamos la matriz de Incidencia Nodal que parte de las pestañas del excel
que tienen nombres des Barra, Lineas y Tierra, para cálcular la matriz, se 
crearon las condiciones para que el codigo genera la matriz de incidencia sin
cargas a tierra o sin cargas a tierra."""

# Creamos la matriz de Incidencia Nodal.

Matriz_A = Extras.Incidencia_Nodal(Barra_i_lineas, Barra_j_lineas, BUS_I)

# Creamos la matriz Z_rama.

Z_rama = Extras.Z_rama (Barra_i_lineas, Barra_j_lineas, Bshunt_lineas, R_Lineas, X_Lineas, BUS_I, R_tierra, X_tierra)

# Creamos la matriz de admitancias.

Y_bus = Extras.Y_BUS (Matriz_A, Z_rama)

# Extraemos los resultados del GS. 

Resultados_GS, angulos_grados_GS, iteracion_GS, S_esp_GS = GAUSS.METODO_GS(Angulo_grados,Modulo_V,P_generada,Q_generada,P_demanda, Q_demanda,Max_Iter,Bus_i_Barras, Tipo_Barra, Y_bus, Error)

# METODO DE NR

# Inicializa las listas para almacenar los módulos y ángulos
Y_modulos = []
Y_angulos = []

#Recorre la matriz Y_bus de forma lineal, gracias al .flat, y crea un vector fila con todas las operaciones.
for z in Y_bus.flat:
    modulo = abs(z)
    angulo = np.angle(z)  # Calcula el ángulo en radianes
    Y_modulos.append(modulo)
    Y_angulos.append(angulo)

# Convierte las listas en matrices con la misma disposición matricial de la Y_bus.
Y_modulos_matriz = np.array(Y_modulos).reshape(Y_bus.shape)
Y_angulos_matriz = np.array(Y_angulos).reshape(Y_bus.shape)

# Transformamos el angulo de los fasores en grad a rad.
angulos_radianes = np.deg2rad(Angulo_grados)

# Calculamos la S especificada desde el excel.
S_esp = (P_generada + Q_generada) - (P_demanda + Q_demanda)

# Listas a utilizar.
P_activa = []
Q_reactiva = []

# Separamos la Potencia Activa y Reactiva de S_esp.
P_esp = [np.real(z) for z in S_esp]
Q_esp = [np.imag(z) for z in S_esp]

for k in range(len(S_esp)):
    # Creamos las rutinas de calculo según el tipo de barra.
    if Tipo_Barra[k] == "SL":
        P_activa.append(0)
        Q_reactiva.append(0)
        continue
            
    if Tipo_Barra[k] == "PV":
        # Asegurar que k+1 no exceda el rango
        #Para efectos prácticos se desglazaron los diferentes terminos en diferentes variables, para 
        #visualizar de manera más completa la rutina, por lo que procedemos a realizar los cálculos según
        #el tipo de barra que tengamos.
        Result = Calcular_P(Modulo_V, Y_modulos_matriz, Y_angulos_matriz, angulos_radianes, S_esp, k,  P_esp)
        P_activa.append(Result)
        Q_reactiva.append(0)


    if Tipo_Barra[k] == "PQ":
        Result = Calcular_P(Modulo_V, Y_modulos_matriz, Y_angulos_matriz, angulos_radianes, S_esp, k,  P_esp)
        P_activa.append(Result)

        Result = Calcular_Q(Modulo_V, Y_modulos_matriz, Y_angulos_matriz, angulos_radianes, S_esp, k, Q_esp)
        Q_reactiva.append(Result)

# Imprimimos los resultados de las potencias activas y reactivas.
print("P_activa =", P_activa)
print("Q_reactiva =", Q_reactiva)

#Derivadas
# Definir las variables como símbolos
V_diff= []
A_diff = []
Variables = []

for i, dif in enumerate(difV):
    if not dif:
        Modulo_V[i] = sp.symbols(f'V{i+1}')
        Variables.append(Modulo_V[i])
    V_diff.append(Modulo_V[i])

for i, dif in enumerate(difA):
    if not dif:
        angulos_radianes[i] = sp.symbols(f'delta{i+1}')
        Variables.append(angulos_radianes[i])
    A_diff.append(angulos_radianes[i])

Variables = np.array(Variables, dtype=object)
V_diff = np.array(V_diff, dtype=object)
A_diff = np.array(A_diff, dtype=object)

#Definimos las expresiones a derivar
P_diff = []

for k in range(len(S_esp)):
    if Tipo_Barra[k] == "SL":
        continue
    Result = Calcular_P(V_diff, Y_modulos_matriz, Y_angulos_matriz, A_diff, S_esp, k,  P_esp)
    P_diff.append(Result)

Q_diff = []

for k in range(len(S_esp)):
    if Tipo_Barra[k] == "SL" or Tipo_Barra[k]== "PV":
        continue   
    Result = Calcular_Q(V_diff, Y_modulos_matriz, Y_angulos_matriz, A_diff, S_esp , k, Q_esp)
    Q_diff.append(Result)

# Derivamos las expresiones
# Inicializar listas para almacenar las derivadas
Jacobiana =  [[0 for _ in range(len(S_esp))] for _ in range(len(S_esp))]


# Iterar sobre el rango de P_diff y Q_diff para calcular las derivadas
for i in range(len(Variables)):
    for j in range(len(P_diff)):
        derivada = sp.diff(P_diff[j],Variables[i])
        Jacobiana[i][j] = sp.simplify(derivada)
    for k in range(len(P_diff), len(P_diff) + len(Q_diff)):
        derivada = sp.diff(Q_diff[k - len(P_diff)], Variables[i])
        Jacobiana[i][k] = sp.simplify(derivada)

# Asignar valores a las variables
# Crear un diccionario vacío
valores = {}

# Asignar 1 a cada valor en V_diff si es una variable de SymPy
for valor in V_diff:
    if isinstance(valor, sp.Symbol):
        valores[valor] = 1

# Asignar 0 a cada valor en A_diff si es una variable de SymPy
for valor in A_diff:
    if isinstance(valor, sp.Symbol):
        valores[valor] = 0

valores_vector = sp.Matrix([valores[var] for var in Variables])
        

# Convertir Jacobiana a una matriz de SymPy
Jacobiana_sp = sp.Matrix(Jacobiana)

# Evaluar la matriz Jacobiana con los valores asignados
Jacobiana_evaluada = Jacobiana_sp.subs(valores)

cont = 0
while cont <= Max_Iter:
    cont += 1
    # Filtrar P_vector para excluir filas que contienen solo 0
    P_vector = sp.Matrix(P_activa)
    filtered_P_vector = sp.Matrix([row for row in P_vector.tolist() if sum(abs(i) for i in row) > 0])
    # Filtrar Q_vector para excluir filas que contienen solo 0
    Q_vector = sp.Matrix(Q_reactiva)
    filtered_Q_vector = sp.Matrix([row for row in Q_vector.tolist() if sum(abs(i) for i in row) > 0])

    # Crear S_vector usando el P_vector filtrado y Q_vector
    S_vector = sp.Matrix.vstack(filtered_P_vector, filtered_Q_vector)

    # Calcular la inversa de la matriz Jacobiana
    Jacobiana_inversa = Jacobiana_evaluada.inv()

    # Calcular el vector de correcciones
    multMatrices = Jacobiana_inversa * S_vector
    X = valores_vector - multMatrices

    #Hallar el error
    error = X - valores_vector

    error_T = max(abs(error))
    if error_T <= 0.0001:
        break
    print(error_T)

    # Actualizar los valores de las variables
    for i in range(len(valores)):
        valores[Variables[i]] = X[i]
    valores_vector = sp.Matrix([valores[var] for var in Variables])

    # Actualizar las listas de potencias activas y reactivas
    P_activa = []
    Q_reactiva = []

    Modulo_V_Nuevo =[]
    Modulo_V_Nuevo = Modulo_V.copy()
    for i, key in enumerate(Modulo_V_Nuevo):
        if key in valores:
            Modulo_V_Nuevo[i] = valores[key]

    angulos_radianes_Nuevo = []
    angulos_radianes_Nuevo = angulos_radianes.copy()
    for i, key in enumerate(angulos_radianes_Nuevo):
        if key in valores:
            angulos_radianes_Nuevo[i] = valores[key]

    for k in range(len(S_esp)):
        if Tipo_Barra[k] == "SL":
            P_activa.append(0)
            Q_reactiva.append(0)
            continue
                
        if Tipo_Barra[k] == "PV":
            Result = Calcular_P(Modulo_V_Nuevo, Y_modulos_matriz, Y_angulos_matriz, angulos_radianes_Nuevo, S_esp, k,  P_esp)
            P_activa.append(Result)
            Q_reactiva.append(0)


        if Tipo_Barra[k] == "PQ":
            Result = Calcular_P(Modulo_V_Nuevo, Y_modulos_matriz, Y_angulos_matriz, angulos_radianes_Nuevo, S_esp, k,  P_esp)
            P_activa.append(Result)

            Result = Calcular_Q(Modulo_V_Nuevo, Y_modulos_matriz, Y_angulos_matriz, angulos_radianes_Nuevo, S_esp, k, Q_esp)
            Q_reactiva.append(Result)

    V_diff= []
    A_diff = []
    Variables = []

    for i, dif in enumerate(difV):
        if not dif:
            Modulo_V_Nuevo[i] = sp.symbols(f'V{i+1}')
            Variables.append(Modulo_V_Nuevo[i])
        V_diff.append(Modulo_V_Nuevo[i])

    for i, dif in enumerate(difA):
        if not dif:
            angulos_radianes_Nuevo[i] = sp.symbols(f'delta{i+1}')
            Variables.append(angulos_radianes_Nuevo[i])
        A_diff.append(angulos_radianes_Nuevo[i])

    Variables = np.array(Variables, dtype=object)
    V_diff = np.array(V_diff, dtype=object)
    A_diff = np.array(A_diff, dtype=object)

    #Definimos las expresiones a derivar
    P_diff = []

    for k in range(len(S_esp)):
        if Tipo_Barra[k] == "SL":
            continue
        Result = Calcular_P(V_diff, Y_modulos_matriz, Y_angulos_matriz, A_diff, S_esp, k,  P_esp)
        P_diff.append(Result)

    Q_diff = []

    for k in range(len(S_esp)):
        if Tipo_Barra[k] == "SL" or Tipo_Barra[k]== "PV":
            continue   
        Result = Calcular_Q(V_diff, Y_modulos_matriz, Y_angulos_matriz, A_diff, S_esp , k, Q_esp)
        Q_diff.append(Result)

    # Inicializar listas para almacenar las derivadas
    Jacobiana =  [[0 for _ in range(len(S_esp))] for _ in range(len(S_esp))]


    # Iterar sobre el rango de P_diff y Q_diff para calcular las derivadas
    for i in range(len(Variables)):
        for j in range(len(P_diff)):
            derivada = sp.diff(P_diff[j],Variables[i])
            Jacobiana[i][j] = sp.simplify(derivada)
        for k in range(len(P_diff), len(P_diff) + len(Q_diff)):
            derivada = sp.diff(Q_diff[k - len(P_diff)], Variables[i])
            Jacobiana[i][k] = sp.simplify(derivada)

    # Convertir Jacobiana a una matriz de SymPy
    Jacobiana_sp = sp.Matrix(Jacobiana)

    # Evaluar la matriz Jacobiana con los valores asignados
    Jacobiana_evaluada = Jacobiana_sp.subs(valores)

print('Final')
