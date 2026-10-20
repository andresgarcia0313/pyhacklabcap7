"""
lab07.py - Programa principal del laboratorio 7 (Paso 5).

Une todo: se conecta al panel de Metasploit, escanea el objetivo del laboratorio,
muestra los puertos abiertos, se conecta al puerto de control de la red de
anonimato, muestra su versión y pide un camino nuevo. Todo ocurre en 127.0.0.1.
"""
import sys  # incluido en Python: permite salir con un código de resultado

from config import MSF_HOST, MSF_PORT, PUERTOS_OBJETIVO, TOR_PORT
from integracion import flujo
# Dos funciones se llaman igual (conectar) en archivos distintos; "as" les da un
# nombre nuevo para no confundirlas.
from msf_cliente import conectar as conectar_msf
from tor_control import conectar as conectar_tor
from tor_control import version

OBJETIVO = "127.0.0.1"  # el único objetivo permitido en el laboratorio


def main() -> int:
    """Ejecuta el laboratorio completo y devuelve 0 si todo salió bien."""
    print("== Laboratorio 7: Metasploit por RPC y control de anonimato (local) ==")
    try:
        cliente = conectar_msf()  # abre sesión con el panel (clave del entorno)
    except Exception as e:        # el panel no responde o la clave es inválida
        print(f"[!] No se pudo conectar al panel en {MSF_HOST}:{MSF_PORT}: {e}")
        print("    Arranque el simulador: python3 simulador_msfrpcd.py")
        return 1
    try:
        controlador = conectar_tor()  # abre el puerto de control (clave del entorno)
    except Exception as e:
        print(f"[!] No se pudo conectar al control en el puerto {TOR_PORT}: {e}")
        print("    Arranque el simulador: python3 simulador_tor.py")
        return 1
    print(f"[*] Objetivo: {OBJETIVO} | Puertos: {PUERTOS_OBJETIVO}")
    print(f"[*] Versión del servicio de anonimato: {version(controlador)}")
    resultado = flujo(OBJETIVO, cliente, controlador)  # escanea y luego rota
    # .get("clave", valor) lee del diccionario; si la clave falta, usa el valor.
    abiertos = resultado.get("lab_puertos_abiertos", [])
    print(f"[+] Puertos abiertos en el objetivo: {abiertos}")
    print("[+] Se pidió un camino nuevo (señal NEWNYM)")
    controlador.close()  # cierra el puerto de control
    print("LABORATORIO COMPLETADO")
    return 0


# Esta línea hace que main() se ejecute solo cuando se corre el archivo directamente.
if __name__ == "__main__":
    sys.exit(main())
