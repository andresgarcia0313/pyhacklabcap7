"""
tor_control.py - Puerto de control de la red de anonimato (Paso 3).

Una red de anonimato (como la red Tor) tiene un "puerto de control": un canal de
texto por el que se le dan órdenes al servicio, por ejemplo pedirle un camino
nuevo. La librería stem habla ese lenguaje por nosotros.

IMPORTANTE: aquí solo enviamos SEÑALES de control (consultar la versión, pedir un
camino nuevo). NO enrutamos tráfico: en este laboratorio nada sale por la red de
anonimato. Es la forma segura y local de practicar el control del servicio.
"""
# Signal es el catálogo de señales de control; Controller es el cliente del puerto.
from stem import Signal
from stem.control import Controller

# Datos y ayudante de nuestro config.py (Paso 1).
from config import TOR_PORT, VAR_TOR_PASSWORD, clave_requerida


def conectar(puerto: int = TOR_PORT) -> Controller:
    """Abre el puerto de control y se autentica con la clave del entorno."""
    # from_port abre la conexión al puerto de control en 127.0.0.1.
    controlador = Controller.from_port(port=puerto)
    # authenticate se identifica ante el servicio. La clave sale de LAB07_TOR_PASSWORD.
    controlador.authenticate(password=clave_requerida(VAR_TOR_PASSWORD))
    return controlador


def version(controlador: Controller) -> str:
    """Devuelve, como texto, la versión del servicio de anonimato."""
    # get_version pregunta la versión; str(...) la convierte en texto legible.
    return str(controlador.get_version())


def rotar_circuito(controlador: Controller) -> None:
    """Pide un camino nuevo con la señal NEWNYM (new identity, identidad nueva)."""
    # signal envía una orden al servicio; NEWNYM le dice "arma un camino nuevo".
    controlador.signal(Signal.NEWNYM)
