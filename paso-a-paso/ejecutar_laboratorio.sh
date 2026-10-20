#!/usr/bin/env bash
# Ejecuta el laboratorio 7 completo en local y se detiene en el primer fallo:
# entorno -> pruebas -> simuladores -> programa principal -> validación -> limpieza.
# Uso: ./ejecutar_laboratorio.sh
set -euo pipefail
cd "$(dirname "$0")"

# Archivos que construye el estudiante y el paso de la guía que los crea.
faltan=0
for par in config.py:1 msf_cliente.py:2 tor_control.py:3 integracion.py:4 lab07.py:5; do
  if [[ ! -f "${par%%:*}" ]]; then
    echo "[!] Falta ${par%%:*}: se crea en el Paso ${par##*:} de la guía"
    faltan=1
  fi
done
[[ $faltan -eq 0 ]] || exit 1

# Claves solo para esta sesión local; en un equipo real use claves propias.
export LAB07_MSF_PASSWORD="${LAB07_MSF_PASSWORD:-clave-local-de-practica}"
export LAB07_TOR_PASSWORD="${LAB07_TOR_PASSWORD:-clave-local-de-practica}"

PIDS_SIM=()
detener_simuladores() {
  for pid in "${PIDS_SIM[@]:-}"; do
    if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
      kill "$pid" && wait "$pid" 2>/dev/null || true
    fi
  done
  PIDS_SIM=()
}
trap detener_simuladores EXIT

puerto_abierto() { python3 -c "import socket,sys; socket.create_connection(('127.0.0.1', int(sys.argv[1])), 1)" "$1" 2>/dev/null; }

esperar_puerto() {  # $1 puerto, espera hasta 10 s
  for _ in $(seq 1 40); do
    if puerto_abierto "$1"; then return 0; fi
    sleep 0.25
  done
  echo "[!] El puerto $1 no abrió"; exit 1
}

iniciar_simuladores() {
  if puerto_abierto 55553 || puerto_abierto 9051; then
    echo "[!] Los puertos 55553 o 9051 ya están en uso. Ejecute ./limpiar.sh y reintente."; exit 1
  fi
  python3 simulador_msfrpcd.py & PIDS_SIM+=("$!")
  python3 simulador_tor.py & PIDS_SIM+=("$!")
  esperar_puerto 55553; esperar_puerto 9051; esperar_puerto 10021
}

titulo() { printf '\n========== %s ==========\n' "$1"; }

titulo "Paso 0: entorno virtual y dependencias"
[[ -d .venv ]] || python3 -m venv --system-site-packages .venv
# shellcheck disable=SC1091
source .venv/bin/activate
python3 -m pip install -q -r requirements.txt
python3 -c "import pymetasploit3, stem, msgpack; print('Dependencias OK, stem', stem.__version__)"

titulo "Pruebas automáticas (cada prueba de red levanta sus propios simuladores)"
python3 -m unittest test_red_permitida test_integracion test_simuladores

titulo "Simuladores + programa principal (Paso 5)"
iniciar_simuladores
python3 lab07.py

titulo "Validación final"
python3 validar.py

titulo "Limpieza"
detener_simuladores
pgrep -af '^python[0-9.]* (\./)?(simulador_msfrpcd|simulador_tor)\.py' || echo "Sin procesos del laboratorio activos"
echo; echo "LABORATORIO COMPLETADO"
