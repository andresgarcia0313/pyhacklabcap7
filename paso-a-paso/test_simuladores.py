"""
Prueba de ronda local: levanta los dos simuladores DENTRO del proceso, en puertos
libres que asigna el sistema y con su propia clave. Así pasa aunque usted haya
dejado encendidos los simuladores de los pasos anteriores. Todo en 127.0.0.1.
"""
import socket
import threading
import unittest
import warnings
from unittest import mock

import msf_cliente
import simulador_msfrpcd
import simulador_tor
import tor_control

CLAVE = "clave-de-prueba-local"


def puerto_libre() -> int:
    """Pide al sistema un puerto TCP libre y lo devuelve."""
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def abrir_victima() -> tuple:
    """Deja escuchando un puerto (devuelve su número y el socket para cerrarlo luego)."""
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 0))
    s.listen(8)
    threading.Thread(target=_aceptar, args=(s,), daemon=True).start()
    return s.getsockname()[1], s


def _aceptar(s: socket.socket) -> None:
    while True:
        try:
            conexion, _ = s.accept()
            conexion.close()
        except OSError:
            break


def servir(servidor) -> None:
    threading.Thread(target=servidor.serve_forever, daemon=True).start()


class SimuladoresTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # stem imprime un DeprecationWarning propio (setDaemon) en Python nuevo; se silencia.
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        cls.sockets = []
        cls.va, sa = abrir_victima()
        cls.vb, sb = abrir_victima()
        cls.sockets += [sa, sb]
        cls.vc = puerto_libre()  # puerto sin nadie escuchando: debe quedar cerrado
        # Panel de Metasploit simulado, en un puerto libre y con su propia clave.
        cls.msf = simulador_msfrpcd.Servidor(("127.0.0.1", puerto_libre()),
                                             simulador_msfrpcd.Manejador)
        cls.puerto_msf = cls.msf.server_address[1]
        servir(cls.msf)
        # Control de anonimato simulado, en otro puerto libre.
        cls.tor = simulador_tor.Servidor(("127.0.0.1", puerto_libre()), simulador_tor.Manejador)
        cls.puerto_tor = cls.tor.server_address[1]
        servir(cls.tor)

    @classmethod
    def tearDownClass(cls):
        for servidor in (getattr(cls, "msf", None), getattr(cls, "tor", None)):
            if servidor is not None:
                servidor.shutdown()
                servidor.server_close()
        for s in getattr(cls, "sockets", []):
            s.close()

    def test_escaneo_encuentra_puertos_abiertos(self):
        with mock.patch.dict("os.environ", {"LAB07_MSF_PASSWORD": CLAVE}), \
             mock.patch.object(msf_cliente, "MSF_PORT", self.puerto_msf):
            cliente = msf_cliente.conectar()
            puertos = f"{self.va},{self.vb},{self.vc}"
            resultado = msf_cliente.ejecutar_portscan(cliente, "127.0.0.1", puertos=puertos)
        self.assertEqual(sorted(resultado["lab_puertos_abiertos"]), sorted([self.va, self.vb]))

    def test_control_de_anonimato_responde(self):
        with mock.patch.dict("os.environ", {"LAB07_TOR_PASSWORD": CLAVE}):
            controlador = tor_control.conectar(puerto=self.puerto_tor)
        self.assertEqual(tor_control.version(controlador), "0.4.8.10")
        tor_control.rotar_circuito(controlador)  # no debe lanzar error
        controlador.close()


if __name__ == "__main__":
    unittest.main()
