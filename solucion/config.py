"""
config.py - Configuración central del laboratorio 7 (Paso 1).

Este texto entre tres comillas dobles es un DOCSTRING: una nota que describe el
archivo. Python no la ejecuta; está ahí para quien lee el código.

Qué hace: reúne en un solo lugar los datos que podrían cambiar (dónde escucha el
panel de control de Metasploit, dónde escucha el puerto de control de la red de
anonimato, qué objetivo está permitido y qué puertos se revisan). Los demás
archivos toman estos valores de aquí.

Regla de oro del laboratorio: las claves NUNCA se escriben en el código. Se leen
de variables de entorno (se explican más abajo). Todo ocurre en 127.0.0.1, que es
SU PROPIO equipo: ningún paquete sale de su computador.
"""
# "import" trae código ya escrito. Estos dos módulos vienen incluidos con Python.
import ipaddress  # entiende direcciones y redes IP (Internet Protocol)
import os          # permite leer variables de entorno del sistema

# Un nombre en MAYÚSCULAS, por costumbre, guarda un valor que no cambia.
# Lo que va entre comillas es un TEXTO; un número sin comillas es un ENTERO.

# --- Panel de control de Metasploit (servicio RPC simulado) ----------------
# RPC = Remote Procedure Call (llamada a procedimiento remoto): pedirle a un
# programa que ejecute una función por la red, como si la llamáramos en local.
MSF_HOST = "127.0.0.1"  # el panel simulado corre en su propio equipo
MSF_PORT = 55553        # puerto donde escucha el panel (el que usa msfrpcd)
# SSL = Secure Sockets Layer (capa de conexión segura): cifra lo que viaja por la red.
MSF_SSL = False         # False = sin cifrado: es local y de práctica

# --- Puerto de control de la red de anonimato (simulado) -------------------
TOR_HOST = "127.0.0.1"  # el control simulado corre en su propio equipo
TOR_PORT = 9051         # puerto de control estándar de ese servicio

# --- Dónde están las claves (variables de entorno, nunca en el código) -----
# Una VARIABLE DE ENTORNO es un dato que el sistema guarda fuera del programa.
# Aquí solo anotamos sus NOMBRES; los valores los pone usted antes de ejecutar.
VAR_MSF_PASSWORD = "LAB07_MSF_PASSWORD"  # clave del panel de Metasploit
VAR_TOR_PASSWORD = "LAB07_TOR_PASSWORD"  # clave del puerto de control

# --- Objetivo permitido ----------------------------------------------------
# Solo se permite escanear esta red. "127.0.0.1/32" es UNA sola dirección: la suya.
# El control rechaza cualquier otra IP y rechaza pedir una red entera como objetivo.
RED_PERMITIDA = "127.0.0.1/32"

# Puertos que se revisan en el objetivo, separados por comas. El simulador deja
# ABIERTOS el 10021, el 10022 y el 10080 y deja CERRADOS el 10025 y el 13306, para
# que el escaneo note la diferencia. Los abiertos imitan tres servicios comunes:
# FTP (File Transfer Protocol, transferencia de archivos), SSH (Secure Shell,
# consola remota cifrada) y un servidor web.
PUERTOS_OBJETIVO = "10021,10022,10025,10080,13306"


# "def" define una FUNCIÓN: un bloque con nombre que se ejecuta al llamarlo.
# "(objetivo: str)" es el dato que recibe; "-> bool" avisa que devuelve verdadero
# o falso. Todo lo SANGRADO (4 espacios) pertenece a la función.
def objetivo_permitido(objetivo: str) -> bool:
    """Indica si el objetivo es UNA sola IP y pertenece a la red permitida."""
    # "try" intenta algo; si falla, Python salta al "except" en vez de detenerse.
    try:
        # ip_address acepta una sola dirección; si recibe una red (con "/") falla.
        # "in" pregunta si esa dirección pertenece a la red permitida.
        return ipaddress.ip_address(objetivo) in ipaddress.ip_network(RED_PERMITIDA)
    except ValueError:
        return False  # cualquier texto que no sea una sola IP válida se rechaza


def clave_requerida(nombre_variable: str) -> str:
    """Devuelve la clave guardada en una variable de entorno o detiene el programa."""
    valor = os.environ.get(nombre_variable)  # lee la variable; None si no existe
    # "not valor" es verdadero si está vacía o no existe.
    if not valor:
        # "raise SystemExit(...)" detiene el programa con un mensaje claro.
        raise SystemExit(f"Falta la variable de entorno {nombre_variable}. "
                         f"Expórtela antes de ejecutar: export {nombre_variable}='su-clave'")
    return valor  # "return" entrega el valor a quien llamó la función
