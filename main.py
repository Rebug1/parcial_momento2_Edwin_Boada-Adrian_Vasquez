gastos = []

CONCEPTOS_VALIDOS = {
    "combustible",
    "mantenimiento",
    "peaje",
    "parqueadero",
    "lavado",
    "soat",
    "tecnomecanica",
    "seguro",
    "impuesto",
    "multa",
    "repuestos",
    "llantas",
    "otro",
}

VALOR_MAXIMO_GASTO = 100_000_000

def formatear_pesos_colombianos(valor):
    valor_formateado = f"{valor:,.2f}"
    valor_formateado = valor_formateado.replace(",", "#").replace(".", ",").replace("#", ".")
    return f"${valor_formateado} COP"

def valor_tiene_formato_colombiano(entrada):
    partes_decimales = entrada.split(",")

    if len(partes_decimales) > 2:
        return False

    parte_entera = partes_decimales[0]
    parte_decimal = partes_decimales[1] if len(partes_decimales) == 2 else ""

    if parte_decimal and (not parte_decimal.isdigit() or len(parte_decimal) > 2):
        return False

    if "." not in parte_entera:
        return parte_entera.isdigit()

    grupos = parte_entera.split(".")

    if not grupos[0].isdigit() or len(grupos[0]) < 1 or len(grupos[0]) > 3:
        return False

    for grupo in grupos[1:]:
        if not grupo.isdigit() or len(grupo) != 3:
            return False

    return True

def convertir_valor_pesos(entrada):
    entrada = entrada.replace("$", "").replace("COP", "").replace("cop", "")
    entrada = entrada.replace(" ", "")

    if not valor_tiene_formato_colombiano(entrada):
        raise ValueError

    if "," in entrada:
        entrada = entrada.replace(".", "").replace(",", ".")
    else:
        entrada = entrada.replace(".", "")

    return float(entrada)

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

        except Exception as error:
            print(f"Error inesperado al leer {nombre_campo}: {error}")
            return None

def normalizar_placa(placa):
    return placa.strip().upper().replace(" ", "").replace("-", "")

def placa_tiene_formato_colombiano(placa):
    placa_carro = (
        len(placa) == 6
        and placa[:3].isalpha()
        and placa[3:].isdigit()
    )
    placa_moto = (
        len(placa) == 6
        and placa[:3].isalpha()
        and placa[3:5].isdigit()
        and placa[5].isalpha()
    )

    return placa_carro or placa_moto

def pedir_placa():
    while True:
        placa = pedir_texto("Ingrese la placa del vehiculo: ", "placa")
        if placa is None:
            return None

        placa = normalizar_placa(placa)

        if not placa.isalnum():
            print("Error: la placa solo puede contener letras y numeros.")
            continue

        if not placa_tiene_formato_colombiano(placa):
            print("Error: formato de placa invalido para Colombia.")
            print("Ejemplos validos: ABC123 para carros o ABC12D para motos.")
            continue

        return placa

def pedir_concepto():
    while True:
        concepto = pedir_texto("Ingrese el concepto: ", "concepto")
        if concepto is None:
            return None

        concepto_normalizado = concepto.strip().lower()

        if any(caracter.isdigit() for caracter in concepto_normalizado):
            print("Error: el concepto no debe contener numeros.")
            continue

        if concepto_normalizado not in CONCEPTOS_VALIDOS:
            print("Error: concepto no valido para el gestor de gastos vehiculares.")
            print("Conceptos validos:", ", ".join(sorted(CONCEPTOS_VALIDOS)))
            continue

        return concepto_normalizado

def pedir_valor_gasto():
    while True:
        try:
            entrada = input("Ingrese el valor del gasto en pesos colombianos: ").strip()

            if not entrada:
                print("Error: el valor del gasto no puede estar vacio.")
                continue

            valor = convertir_valor_pesos(entrada)

            if valor <= 0:
                print("Error: el valor del gasto debe ser mayor que cero.")
                continue

            if valor > VALOR_MAXIMO_GASTO:
                print(f"Error: el valor no puede superar {formatear_pesos_colombianos(VALOR_MAXIMO_GASTO)}.")
                continue

            return valor

        except ValueError:
            print("Error: ingrese un valor numerico valido. Ejemplo: 85000 o $85.000.")

        except (KeyboardInterrupt, EOFError):
            print("\nOperacion cancelada por el usuario.")
            return None

        except Exception as error:
            print(f"Error inesperado al leer el valor del gasto: {error}")
            return None

def registrar_gasto():
    try:
        print("\n--- REGISTRAR GASTO ---")

        placa = pedir_placa()
        if placa is None:
            return

        concepto = pedir_concepto()
        if concepto is None:
            return

        valor = pedir_valor_gasto()
        if valor is None:
            return

        gasto = {
            "placa": placa,
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

        for posicion, gasto in enumerate(gastos, start=1):
            if not isinstance(gasto, dict):
                print(f"Error: el registro #{posicion} tiene una estructura invalida.")
                return

            valor = gasto.get("valor")

            if not isinstance(valor, (int, float)) or valor <= 0:
                print(f"Error: el registro #{posicion} tiene un valor invalido.")
                return

            total += valor

        print(f"El gasto total es: {formatear_pesos_colombianos(total)}")

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

        placa_buscar = pedir_placa()
        if placa_buscar is None:
            return

        encontrado = False

        for posicion, gasto in enumerate(gastos, start=1):
            if not isinstance(gasto, dict):
                print(f"Advertencia: se omitio el registro #{posicion} porque esta corrupto.")
                continue

            placa = gasto.get("placa")
            concepto = gasto.get("concepto", "Sin concepto")
            valor = gasto.get("valor")

            if placa == placa_buscar:
                if not isinstance(valor, (int, float)) or valor <= 0:
                    print(f"Advertencia: el registro #{posicion} tiene un valor invalido y fue omitido.")
                    continue

                print("\nGasto encontrado")
                print(f"Concepto: {concepto}")
                print(f"Valor: {formatear_pesos_colombianos(valor)}")

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