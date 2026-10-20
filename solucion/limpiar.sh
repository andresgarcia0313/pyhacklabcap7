#!/usr/bin/env bash
# Deja el entorno limpio: detiene los simuladores si quedaron corriendo.
# Uso: ./limpiar.sh
set -euo pipefail
cd "$(dirname "$0")"

if pkill -f '^python[0-9.]* (\./)?(simulador_msfrpcd|simulador_tor)\.py'; then
  for _ in $(seq 1 20); do  # espera hasta 5 s a que terminen
    pgrep -f '^python[0-9.]* (\./)?(simulador_msfrpcd|simulador_tor)\.py' >/dev/null || break
    sleep 0.25
  done
  echo "[+] Simuladores detenidos"
else
  echo "[=] Los simuladores no estaban corriendo"
fi

pgrep -af '^python[0-9.]* (\./)?(simulador_msfrpcd|simulador_tor)\.py' || echo "[+] Sin procesos del laboratorio activos"
