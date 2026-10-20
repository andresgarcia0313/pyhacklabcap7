#!/usr/bin/env python3
"""
simulador_tor.py - Puerto de control de la red de anonimato, simulado y local.

Ya viene listo: NO lo modifique. Hace de "puerto de control" sin instalar ningún
servicio de anonimato. Escucha en 127.0.0.1:9051 y responde el mismo protocolo de
texto que el servicio real, así la librería stem se conecta, se autentica, pide la
versión y envía la señal de camino nuevo igual que en una instalación de verdad.

No enruta tráfico: solo responde a las órdenes de control. Nada sale de su equipo.

Uso:  python3 simulador_tor.py      (Ctrl+C para detener)
"""
import socketserver

PUERTO_CONTROL = 9051        # puerto de control estándar
VERSION = "0.4.8.10"         # versión que anuncia el servicio simulado


class Manejador(socketserver.StreamRequestHandler):
    """Atiende una conexión: lee una orden por línea y responde según el protocolo."""

    def handle(self):
        salida = self.wfile
        while True:
            crudo = self.rfile.readline()
            if not crudo:
                break  # el cliente cerró la conexión
            linea = crudo.decode("utf-8", "replace").strip()
            mayus = linea.upper()
            if mayus.startswith("PROTOCOLINFO"):
                # Anuncia qué método de autenticación se usa (clave).
                salida.write(b"250-PROTOCOLINFO 1\r\n")
                salida.write(b"250-AUTH METHODS=HASHEDPASSWORD\r\n")
                salida.write(f'250-VERSION Tor="{VERSION}"\r\n'.encode())
                salida.write(b"250 OK\r\n")
            elif mayus.startswith("AUTHENTICATE"):
                salida.write(b"250 OK\r\n")  # acepta la autenticación del laboratorio
            elif mayus.startswith("GETINFO"):
                clave = linea.split(None, 1)[1] if " " in linea else ""
                if clave == "version":
                    salida.write(f"250-version={VERSION}\r\n250 OK\r\n".encode())
                else:
                    salida.write(b"552 Unrecognized key\r\n")
            elif mayus.startswith("SIGNAL"):
                salida.write(b"250 OK\r\n")   # acepta la señal (por ejemplo NEWNYM)
            elif mayus.startswith("SETEVENTS"):
                salida.write(b"250 OK\r\n")
            elif mayus.startswith("QUIT"):
                salida.write(b"250 closing connection\r\n")
                salida.flush()
                break
            else:
                salida.write(b"250 OK\r\n")   # cualquier otra orden simple
            salida.flush()


class Servidor(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main() -> None:
    servidor = Servidor(("127.0.0.1", PUERTO_CONTROL), Manejador)
    print(f"[sim-tor] Control de anonimato simulado en 127.0.0.1:{PUERTO_CONTROL}")
    print(f"[sim-tor] Versión anunciada: {VERSION}")
    print("[sim-tor] Ctrl+C para detener")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n[sim-tor] Detenido")


if __name__ == "__main__":
    main()
