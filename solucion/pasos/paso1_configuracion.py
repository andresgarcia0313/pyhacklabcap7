"""
Paso 1: revisar la configuración central (config.py). No usa red.
Uso (desde la carpeta de trabajo): python3 pasos/paso1_configuracion.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config  # noqa: E402  (va después de ajustar sys.path)

print(f"Panel de Metasploit: {config.MSF_HOST}:{config.MSF_PORT} (ssl={config.MSF_SSL})")
print(f"Control de anonimato: {config.TOR_HOST}:{config.TOR_PORT}")
print(f"Red permitida: {config.RED_PERMITIDA}")
print(f"Puertos del objetivo: {config.PUERTOS_OBJETIVO}")
print(f"Clave del panel en la variable: {config.VAR_MSF_PASSWORD}")
print(f"Clave del control en la variable: {config.VAR_TOR_PASSWORD}")
print("\nPrueba del control de objetivo:")
for objetivo in ["127.0.0.1", "203.0.113.10", "127.0.0.0/8"]:
    print(f"  {objetivo:<16} permitido={config.objetivo_permitido(objetivo)}")
