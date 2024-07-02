import sympy as sp

def Calcular_P (Modulo_V, Y_modulos_matriz, Y_angulos_matriz, angulos_radianes, S_esp, k,  P_esp):
    Result = 0
    Valor_1 = (Modulo_V[k] ** 2) * (Y_modulos_matriz[k, k]) * sp.cos(Y_angulos_matriz[k, k]) # Calculamos el termino que es cuadratico.
    for i in range(len(S_esp)):
        if i != k:
            Valores_2 = Modulo_V[k] * Modulo_V[i] * Y_modulos_matriz[k, i] * sp.cos(
                angulos_radianes[k] - angulos_radianes[i] - Y_angulos_matriz[k, i]) # Calculamos los terminos que varian los indices.
            Valor_1 += Valores_2 # Sumamos todos los terminos variables con el cuadratico.
    Result = P_esp[k] - Valor_1 # Sustituimos el valor de P.
    return Result 

def Calcular_Q(Modulo_V, Y_modulos_matriz, Y_angulos_matriz, angulos_radianes, S_esp , k, Q_esp):
    Valor_3 = - (Modulo_V [k]**2)*Y_modulos_matriz[k,k]*sp.sin(Y_angulos_matriz[k,k]) # Calculamos el termino que es cuadratico.
    for h in range(len(S_esp)):
        if h != k:
            Valores_4 = Modulo_V[k]*Modulo_V[h]*Y_modulos_matriz[k,h]*sp.sin(
                angulos_radianes[k] - angulos_radianes[h] - Y_angulos_matriz[k,h]) # Calculamos los terminos que varian los indices.
            Valor_3 += Valores_4 # Sumamos todos los terminos variables con el cuadratico.
    Result = Q_esp[k] - Valor_3 # Sustituimos el valor de P.
    return Result
