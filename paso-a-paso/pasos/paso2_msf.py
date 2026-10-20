"""
Paso 2: conectar al panel de Metasploit y escanear (msf_cliente.py).
Necesita el simulador del panel corriendo en otra terminal.
Uso: python3 pasos/paso2_msf.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import msf_cliente  # noqa: E402

print("Conectando al panel de Metasploit...")
cliente = msf_cliente.conectar()
print("Conectado. Lanzando el escáner de puertos sobre 127.0.0.1...")
resultado = msf_cliente.ejecutar_portscan(cliente, "127.0.0.1")
print(f"Puertos abiertos: {resultado.get('lab_puertos_abiertos')}")

print("\nAhora con un objetivo NO permitido (debe ser rechazado):")
try:
    msf_cliente.ejecutar_portscan(cliente, "203.0.113.10")
except PermissionError as e:
    print(f"  Rechazado correctamente: {e}")
