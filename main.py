gastos = []

def registrar_gasto():

    print("\n--- REGISTRAR GASTO ---")

    placa = input("Ingrese la placa del vehículo: ")

    concepto = input("Ingrese el concepto: ")

    valor = float(input("Ingrese el valor del gasto: "))

    gasto = {
        "placa": placa,
        "concepto": concepto,
        "valor": valor
    }

    gastos.append(gasto)

    print("Gasto registrado correctamente")


while True:

    print("\n====== GESTOR DE GASTOS ======")
    print("1. Registrar gasto")
    print("2. Mostrar total de gastos")
    print("3. Buscar gastos por placa")
    print("4. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        registrar_gasto()

    elif opcion == "2":
        pass

    elif opcion == "3":
        pass

    elif opcion == "4":
        print("Saliendo del programa...")
        break

    else:
        print("Opción inválida")