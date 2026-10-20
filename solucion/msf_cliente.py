"""
msf_cliente.py - Conexión al panel de Metasploit y escáner de puertos (Paso 2).

Metasploit tiene un "panel de control" al que se le pueden dar órdenes por la red
mediante RPC (Remote Procedure Call, llamada a procedimiento remoto). La librería
pymetasploit3 habla ese lenguaje por nosotros. Aquí hacemos dos cosas:
  1. Abrir la sesión con el panel, usando una clave que sale del entorno.
  2. Pedirle al panel que ejecute su escáner de puertos contra el objetivo.

Antes de tocar el panel, comprobamos que el objetivo esté permitido. Así la
herramienta nunca actúa sobre equipos ajenos, aunque alguien le pase otra IP.
"""
# "from X import Y" trae solo el nombre Y. Esta clase viene de la librería externa
# pymetasploit3 (se instala con pip; ver requirements.txt).
from pymetasploit3.msfrpc import MsfRpcClient

# También importamos de nuestro propio config.py (Paso 1): varios nombres a la vez,
# separados por comas, entre paréntesis para repartirlos en varias líneas.
from config import (MSF_HOST, MSF_PORT, MSF_SSL, PUERTOS_OBJETIVO, RED_PERMITIDA,
                    VAR_MSF_PASSWORD, clave_requerida, objetivo_permitido)


def conectar() -> MsfRpcClient:
    """Abre la sesión con el panel. La clave sale del entorno, nunca del código."""
    clave = clave_requerida(VAR_MSF_PASSWORD)  # lee LAB07_MSF_PASSWORD del entorno
    # MsfRpcClient(clave, server=..., port=..., ssl=...) crea el cliente y entra.
    # ssl indica si la conexión va cifrada (SSL, Secure Sockets Layer); aquí no.
    return MsfRpcClient(clave, server=MSF_HOST, port=MSF_PORT, ssl=MSF_SSL)


def ejecutar_portscan(cliente, objetivo: str, puertos: str = PUERTOS_OBJETIVO,
                      hilos: int = 10) -> dict:
    """Pide al panel el escáner de puertos TCP contra un objetivo permitido."""
    # Control de uso responsable: si el objetivo no está permitido, se corta aquí,
    # ANTES de enviar ninguna orden al panel. "raise" lanza un error que detiene todo.
    if not objetivo_permitido(objetivo):
        raise PermissionError(f"{objetivo} no pertenece a la red permitida ({RED_PERMITIDA})")
    # modules.use carga un módulo del panel. "auxiliary" es la familia de utilidades;
    # "scanner/portscan/tcp" es el escáner de puertos TCP.
    modulo = cliente.modules.use("auxiliary", "scanner/portscan/tcp")
    # El módulo se configura como un diccionario: cada opción entre corchetes.
    modulo["RHOSTS"] = objetivo   # RHOSTS = Remote Hosts: a quién escanear
    modulo["PORTS"] = puertos     # qué puertos revisar
    modulo["THREADS"] = hilos     # cuántas revisiones en paralelo (un entero)
    return modulo.execute()       # ejecuta el módulo y devuelve el resultado
