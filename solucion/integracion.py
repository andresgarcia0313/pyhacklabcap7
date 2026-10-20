"""
integracion.py - Flujo que une las dos piezas (Paso 4).

Primero le pide el escaneo al panel de Metasploit y después le pide un camino
nuevo al puerto de control de la red de anonimato. El orden importa: primero se
mira el objetivo y luego se cambia de camino.

Las dos acciones llegan como PARÁMETROS (escanear y rotar) con un valor por
defecto. Así, en las pruebas podemos pasar piezas de mentira y comprobar el flujo
sin abrir ninguna conexión de red.
"""
# Funciones reales que se usarán si quien llama no indica otras.
from msf_cliente import ejecutar_portscan
from tor_control import rotar_circuito


def flujo(objetivo, cliente_msf, controlador_tor,
          escanear=ejecutar_portscan, rotar=rotar_circuito) -> dict:
    """Escanea el objetivo, rota el circuito y devuelve el resultado del escaneo."""
    resultado = escanear(cliente_msf, objetivo)  # 1. primero el escaneo
    rotar(controlador_tor)                        # 2. después el camino nuevo
    return resultado                              # 3. entrega lo que halló el escaneo
