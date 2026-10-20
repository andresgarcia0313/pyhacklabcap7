"""
Paso 4: el flujo integrado (integracion.py): escanear y después rotar.
Necesita los dos simuladores corriendo.
Uso: python3 pasos/paso4_integracion.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import integracion  # noqa: E402
import msf_cliente  # noqa: E402
import tor_control  # noqa: E402

cliente = msf_cliente.conectar()
controlador = tor_control.conectar()
print("Ejecutando el flujo: primero escaneo, después camino nuevo...")
resultado = integracion.flujo("127.0.0.1", cliente, controlador)
print(f"Puertos abiertos (del escaneo): {resultado.get('lab_puertos_abiertos')}")
print("El camino nuevo ya se pidió después del escaneo.")
controlador.close()
