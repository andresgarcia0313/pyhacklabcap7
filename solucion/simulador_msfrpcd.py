#!/usr/bin/env python3
"""
simulador_msfrpcd.py - Panel de control de Metasploit, simulado y local.

Ya viene listo: NO lo modifique. Hace de "panel de Metasploit" sin instalar
Metasploit. Escucha en 127.0.0.1:55553 y habla el mismo lenguaje que el panel
real (RPC con mensajes empaquetados en formato msgpack), así la librería
pymetasploit3 se conecta igual que en una máquina de verdad.

Además deja abiertos tres puertos del "objetivo" (10021, 10022 y 10080) para que
el escáner encuentre algo. Todo en 127.0.0.1: ningún paquete sale de su equipo.

Uso:  python3 simulador_msfrpcd.py      (Ctrl+C para detener)
"""
import http.server
import os
import socket
import socketserver
import threading
import uuid

import msgpack

PUERTO_PANEL = 55553                       # donde escucha el panel simulado
PUERTOS_ABIERTOS = [10021, 10022, 10080]   # puertos "abiertos" del objetivo

# Opciones del módulo de escaneo, como las publica el panel real.
OPCIONES = {
    "RHOSTS": {"type": "string", "required": True, "advanced": False, "evasion": False},
    "PORTS": {"type": "string", "required": True, "advanced": False, "evasion": False,
              "default": "1-10000"},
    "THREADS": {"type": "integer", "required": False, "advanced": False, "evasion": False,
                "default": 1},
}
INFO = {"name": "TCP Port Scanner", "description": "escáner de puertos TCP (simulado)",
        "rank": "normal"}


def _expandir(ports: str) -> list:
    """Convierte '10021,10025,10080-10081' en una lista de números de puerto."""
    numeros = []
    for parte in str(ports).split(","):
        if "-" in parte:
            desde, hasta = parte.split("-")
            numeros += list(range(int(desde), int(hasta) + 1))
        elif parte.strip():
            numeros.append(int(parte))
    return numeros


def _escanear(rhosts: str, ports: str) -> list:
    """Hace un escaneo TCP real de loopback y devuelve los puertos que aceptan conexión."""
    abiertos = []
    for puerto in _expandir(ports):
        try:
            with socket.create_connection((rhosts, puerto), timeout=0.3):
                abiertos.append(puerto)
        except OSError:
            pass  # cerrado o sin respuesta: no se agrega
    return abiertos


def _despachar(cuerpo: list) -> dict:
    """Responde a cada método RPC. El cliente manda [metodo, token, ...datos]."""
    metodo = cuerpo[0]
    if metodo == "auth.login":
        clave_enviada = cuerpo[2] if len(cuerpo) > 2 else None
        esperada = os.environ.get("LAB07_MSF_PASSWORD")
        if esperada and clave_enviada != esperada:  # clave incorrecta
            return {"error": True, "error_message": "clave invalida"}
        return {"result": "success", "token": "lab07-" + uuid.uuid4().hex[:8]}
    if metodo == "auth.token_add":
        return {"result": "success"}
    if metodo == "core.version":
        return {"version": "6.4.0-lab", "ruby": "3.3.0", "api": "1.0"}
    if metodo == "module.info":
        return dict(INFO)
    if metodo == "module.options":
        return dict(OPCIONES)
    if metodo == "module.execute":
        # El último dato es el diccionario de opciones configuradas.
        runopts = cuerpo[-1] if isinstance(cuerpo[-1], dict) else {}
        abiertos = _escanear(runopts.get("RHOSTS", "127.0.0.1"), runopts.get("PORTS", ""))
        return {"job_id": 0, "uuid": uuid.uuid4().hex, "lab_puertos_abiertos": abiertos}
    return {"error": True, "error_message": f"metodo no simulado: {metodo}"}


class Manejador(http.server.BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass  # silencia el registro de cada petición

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        cuerpo = msgpack.unpackb(self.rfile.read(n), raw=False, strict_map_key=False)
        respuesta = msgpack.packb(_despachar(cuerpo), use_bin_type=True)
        self.send_response(200)
        self.send_header("Content-type", "binary/message-pack")
        self.send_header("Content-Length", str(len(respuesta)))
        self.end_headers()
        self.wfile.write(respuesta)


class Servidor(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def _abrir_puertos_objetivo(puertos: list) -> None:
    """Deja escuchando los puertos 'abiertos' del objetivo, cada uno en su hilo."""
    for puerto in puertos:
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("127.0.0.1", puerto))
        sock.listen(8)
        threading.Thread(target=_aceptar_siempre, args=(sock,), daemon=True).start()


def _aceptar_siempre(sock: socket.socket) -> None:
    """Acepta conexiones y las cierra de inmediato: basta para parecer 'abierto'."""
    while True:
        try:
            conexion, _ = sock.accept()
            conexion.close()
        except OSError:
            break


def main() -> None:
    _abrir_puertos_objetivo(PUERTOS_ABIERTOS)
    servidor = Servidor(("127.0.0.1", PUERTO_PANEL), Manejador)
    print(f"[sim-msf] Panel de Metasploit simulado en 127.0.0.1:{PUERTO_PANEL}")
    print(f"[sim-msf] Objetivo con puertos abiertos: {PUERTOS_ABIERTOS}")
    print("[sim-msf] Ctrl+C para detener")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n[sim-msf] Detenido")


if __name__ == "__main__":
    main()
