# Ejercicio 9 - Admisión a colegio privado


COSTO_ANUAL = 18000000


def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            break
        print("Error: este dato no puede estar vacío. Escriba un nombre.")
    return texto.title()


def pedir_entero(mensaje, minimo, maximo=None):
    while True:
        texto = input(mensaje).strip()
        if not texto.isdigit():
            print(f"Error: se esperaba un número entero, sin letras, signos ni decimales. Recibido: '{texto}'")
            continue
        numero = int(texto)
        if maximo is None and numero < minimo:
            print(f"Error: el valor debe ser mayor o igual a {minimo}. Recibido: {numero}")
        elif maximo is not None and (numero < minimo or numero > maximo):
            print(f"Error: el valor debe estar entre {minimo} y {maximo}. Recibido: {numero}")
        else:
            break
    return numero

    #FUNCIONES PARA PEDIR OPCIONES SI/NO 

def pedir_opcion(mensaje, opciones):
    while True:
        texto = input(mensaje).strip().upper()
        if texto in opciones:
            break
        print(f"Error: escriba una de estas opciones: {', '.join(opciones)}. Recibido: '{texto}'")
    return texto


def pedir_si_no(mensaje):
    while True:
        texto = input(mensaje).strip().upper()
        if texto in ["S", "SI", "N", "NO"]:
            break
        print(f"Error: responda S, SI, N o NO. Recibido: '{texto}'")
    return texto in ["S", "SI"]

#CICLO DE LOS APORTANTES 

def capturar_ingresos(num_aportantes):
    ingreso_familiar = 0
    for i in range(1, num_aportantes +1 ):
        ingreso = pedir_entero(f"Ingreso mensual del aportante {i}: ", 1)
        ingreso_familiar = ingreso_familiar + ingreso
    return ingreso_familiar

#  FUNCIONES DE PUNTAJES

def puntos_excedente(excedente_anual):
    if excedente_anual >= COSTO_ANUAL:
        return 30
    elif excedente_anual >= COSTO_ANUAL * 0.6:
        return 20
    elif excedente_anual >= COSTO_ANUAL * 0.3:
        return 10
    else:
        return 0

def puntos_tipo_familia(tipo_familia):
    if tipo_familia == "NUCLEAR":
        return 15
    elif tipo_familia == "EXTENSA":
        return 12
    elif tipo_familia == "MONOPARENTAL":
        return 10
    else:
        return 8

def puntos_estado_civil(estado_civil):
    if estado_civil == "CASADOS" or estado_civil == "UNION_LIBRE":
        return 10
    else:
        return 5

def puntos_promedio(promedio):
    if promedio >= 90:
        return 15
    elif promedio >= 80:
        return 12
    elif promedio >= 70:
        return 8
    else:
        return 3

#Descuento y beca

def calcular_descuento(hermanos):
    descuento = hermanos * 10
    if descuento > 25:
        descuento = 25
    return descuento


def calcular_beca(excedente_anual, costo_con_descuento):
    for beca in [20, 35, 50]:
        costo_con_beca = costo_con_descuento - (costo_con_descuento * beca / 100)
        if excedente_anual >= costo_con_beca:
            return beca
    return 0

def pesos(valor):
    return f"${valor:,.0f}".replace(",", ".")

def main():
    print("===== ADMISIÓN A COLEGIO PRIVADO =====")

    # PROGRAMA PRICIPAL CON TODOS LOS DATOS A SOLICITAR. 


    nombre = pedir_texto("Nombre del aspirante: ")
    edad = pedir_entero("Edad del aspirante (5 a 18): ", 5, 18)
    grado = pedir_entero("Grado al que aspira (1 a 11): ", 1, 11)
    acudiente = pedir_texto("Nombre del acudiente: ")
    tipo_familia = pedir_opcion("Tipo de familia (NUCLEAR, MONOPARENTAL, SEPARADA, EXTENSA): ",
    ["NUCLEAR", "MONOPARENTAL", "SEPARADA", "EXTENSA"])
    estado_civil = pedir_opcion("Estado civil de los padres (CASADOS, UNION_LIBRE, SEPARADOS, NO_APLICA): ",
    ["CASADOS", "UNION_LIBRE", "SEPARADOS", "NO_APLICA"])
    num_aportantes = pedir_entero("Número de aportantes económicos (1 a 4): ", 1, 4)
    ingreso_familiar = capturar_ingresos(num_aportantes)
    gastos = pedir_entero("Gastos mensuales de la familia: ", 0)
    vivienda_propia = pedir_si_no("¿Vivienda propia? (S/N): ")
    hermanos = pedir_entero("Hermanos ya matriculados (0 a 5): ", 0, 5)
    promedio = pedir_entero("Promedio académico del año anterior (0 a 100): ", 0, 100)
    observaciones = pedir_si_no("¿Tuvo observaciones disciplinarias? (S/N): ")

    excedente_mensual = ingreso_familiar - gastos
    excedente_anual = excedente_mensual * 12

    pts_excedente = puntos_excedente(excedente_anual)
    if vivienda_propia:
        pts_vivienda = 10
    else:
        pts_vivienda = 0
    if num_aportantes >= 2:
        pts_aportantes = 10
    else:
        pts_aportantes = 0

    pts_tipo = puntos_tipo_familia(tipo_familia)
    pts_estado = puntos_estado_civil(estado_civil)
    if hermanos >= 1:
        pts_hermanos = 5
    else:
        pts_hermanos = 0

    pts_promedio = puntos_promedio(promedio)
    if not observaciones:
        pts_conducta = 5
    else:
        pts_conducta = 0

    puntaje_economico = pts_excedente + pts_vivienda + pts_aportantes
    puntaje_familiar = pts_tipo + pts_estado + pts_hermanos
    puntaje_academico = pts_promedio + pts_conducta
    puntaje_total = puntaje_economico + puntaje_familiar + puntaje_academico

    criterios = [
        ("Económico - Excedente frente al costo", pts_excedente, 30),
        ("Económico - Vivienda propia", pts_vivienda, 10),
        ("Económico - Dos o más aportantes", pts_aportantes, 10),
        ("Familiar - Tipo de familia", pts_tipo, 15),
        ("Familiar - Estado civil de los padres", pts_estado, 10),
        ("Familiar - Hermano matriculado", pts_hermanos, 5),
        ("Académico - Promedio", pts_promedio, 15),
        ("Conductual - Sin observaciones", pts_conducta, 5),
    ]

    descuento = calcular_descuento(hermanos)
    costo_con_descuento = COSTO_ANUAL - (COSTO_ANUAL * descuento / 100)

  # Decisión y carta de resultado

    beca_otorgada = 0
    costo_final = costo_con_descuento

    if puntaje_total >= 70:
        if excedente_anual >= costo_con_descuento:
            decision = "ADMITIDO"
            justificacion = (f"Obtuvo {puntaje_total} puntos (mínimo 70) y su excedente anual de "
                             f"{pesos(excedente_anual)} cubre el costo de {pesos(costo_con_descuento)}.")
        else:
            beca_otorgada = calcular_beca(excedente_anual, costo_con_descuento)
            if beca_otorgada > 0:
                costo_final = costo_con_descuento - (costo_con_descuento * beca_otorgada / 100)
                decision = "ADMITIDO CON BECA PARCIAL"
                justificacion = (f"Obtuvo {puntaje_total} puntos (mínimo 70). Su excedente anual de "
                                 f"{pesos(excedente_anual)} no cubría {pesos(costo_con_descuento)}, "
                                 f"pero con una beca del {beca_otorgada} % sí cubre {pesos(costo_final)}.")
            else:
                decision = "LISTA DE ESPERA POR CAPACIDAD DE PAGO"
                justificacion = (f"Obtuvo {puntaje_total} puntos (mínimo 70), pero su excedente anual de "
                                 f"{pesos(excedente_anual)} no cubre el costo ni con la beca del 50 %.")
    elif puntaje_total >= 50:
        decision = "LISTA DE ESPERA"
        justificacion = f"Obtuvo {puntaje_total} puntos, que está entre 50 y 69."
    else:
        decision = "NO ADMITIDO"
        justificacion = f"Obtuvo {puntaje_total} puntos, que es menor a 50."

    pension_mensual = costo_final / 12

    print()
    print("========== CARTA DE RESULTADO ==========")
    print(f"Aspirante: {nombre}")
    print(f"Edad: {edad} años    Grado al que aspira: {grado}")
    print(f"Acudiente: {acudiente}")
    print(f"Ingreso familiar: {pesos(ingreso_familiar)}    Gastos: {pesos(gastos)}")
    print(f"Excedente anual: {pesos(excedente_anual)}")
    print()
    print("----- Desglose del puntaje -----")
    for nombre_criterio, puntos, maximo in criterios:
        print(f"{nombre_criterio}: {puntos} de {maximo}")
    print(f"Puntaje económico: {puntaje_economico} de 50")
    print(f"Puntaje familiar: {puntaje_familiar} de 30")
    print(f"Puntaje académico y conductual: {puntaje_academico} de 20")
    print(f"PUNTAJE TOTAL: {puntaje_total} de 100")
    print()
    print("----- Costos -----")
    print(f"Costo anual: {pesos(COSTO_ANUAL)}")
    print(f"Descuento por hermanos: {descuento} %")
    print(f"Costo con descuento: {pesos(costo_con_descuento)}")
    print(f"Beca otorgada: {beca_otorgada} %")
    print(f"Costo anual final: {pesos(costo_final)}")
    print(f"Pensión mensual: {pesos(pension_mensual)}")
    print()
    print("----- Resultado -----")
    print(f"Decisión: {decision}")
    print(f"Justificación: {justificacion}")

main()

