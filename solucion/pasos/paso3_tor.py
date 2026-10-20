"""
Paso 3: conectar al puerto de control de anonimato y rotar el circuito (tor_control.py).
Necesita el simulador del control corriendo en otra terminal.
Uso: python3 pasos/paso3_tor.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tor_control  # noqa: E402

print("Conectando al puerto de control...")
controlador = tor_control.conectar()
print(f"Versión del servicio: {tor_control.version(controlador)}")
print("Pidiendo un camino nuevo (señal NEWNYM)...")
tor_control.rotar_circuito(controlador)
print("Camino nuevo solicitado. Sin tráfico real por la red de anonimato.")
controlador.close()
