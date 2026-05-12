gastos = []

def pedir_texto(mensaje, nombre_campo):
    while True:
        try:
            texto = input(mensaje).strip()

            if not texto:
                print(f"Error: el campo {nombre_campo} no puede estar vacio.")
                continue

            return texto

        except (KeyboardInterrupt, EOFError):
            print("\nOperacion cancelada por el usuario.")
            return None

def pedir_valor_gasto():
    while True:
        try:
            valor = float(input("Ingrese el valor del gasto: "))

            if valor <= 0:
                print("Error: el valor del gasto debe ser mayor que cero.")
                continue

            return valor

        except ValueError:
            print("Error: ingrese un valor numerico valido.")

        except (KeyboardInterrupt, EOFError):
            print("\nOperacion cancelada por el usuario.")
            return None

def registrar_gasto():
    try:
        print("\n--- REGISTRAR GASTO ---")

        placa = pedir_texto("Ingrese la placa del vehiculo: ", "placa")
        if placa is None:
            return

        concepto = pedir_texto("Ingrese el concepto: ", "concepto")
        if concepto is None:
            return

        valor = pedir_valor_gasto()
        if valor is None:
            return

        gasto = {
            "placa": placa.upper(),
            "concepto": concepto,
            "valor": valor
        }

        gastos.append(gasto)

        print("Gasto registrado correctamente")

    except Exception as error:
        print(f"Error inesperado al registrar el gasto: {error}")

def mostrar_total_gastos():
    try:
        print("\n--- TOTAL DE GASTOS ---")

        if not gastos:
            print("No hay gastos registrados.")
            return

        total = 0

        for gasto in gastos:
            total += gasto.get("valor", 0)

        print(f"El gasto total es: ${total:.2f}")

    except TypeError:
        print("Error: hay un gasto registrado con un valor invalido.")

    except Exception as error:
        print(f"Error inesperado al calcular el total: {error}")

def buscar_por_placa():
    try:
        print("\n--- BUSCAR GASTOS ---")

        if not gastos:
            print("No hay gastos registrados para buscar.")
            return

        placa_buscar = pedir_texto("Ingrese la placa: ", "placa")
        if placa_buscar is None:
            return

        encontrado = False

        for gasto in gastos:
            if gasto.get("placa") == placa_buscar.upper():
                print("\nGasto encontrado")
                print(f"Concepto: {gasto.get('concepto', 'Sin concepto')}")
                print(f"Valor: ${gasto.get('valor', 0):.2f}")

                encontrado = True

        if not encontrado:
            print("No se encontraron gastos para esa placa")

    except (ValueError, TypeError):
        print("Error: existe un gasto con informacion invalida.")

    except Exception as error:
        print(f"Error inesperado al buscar por placa: {error}")

def mostrar_menu():
    print("\n====== GESTOR DE GASTOS ======")
    print("1. Registrar gasto")
    print("2. Mostrar total de gastos")
    print("3. Buscar gastos por placa")
    print("4. Salir")

def main():
    while True:
        try:
            mostrar_menu()
            opcion = input("Seleccione una opcion: ").strip()

            if opcion == "1":
                registrar_gasto()

            elif opcion == "2":
                mostrar_total_gastos()

            elif opcion == "3":
                buscar_por_placa()

            elif opcion == "4":
                print("Saliendo del programa...")
                break

            else:
                print("Error: opcion invalida. Seleccione un numero del 1 al 4.")

        except (KeyboardInterrupt, EOFError):
            print("\nSaliendo del programa...")
            break

        except Exception as error:
            print(f"Error inesperado en el menu principal: {error}")

if __name__ == "__main__":
    main()