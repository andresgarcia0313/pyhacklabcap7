"""
Prueba de ronda local: levanta los dos simuladores y se conecta con las librerías
reales (pymetasploit3 y stem). Todo en 127.0.0.1; nada sale del equipo.
"""
import os
import socket
import subprocess
import sys
import time
import unittest

import msf_cliente
import tor_control

AQUI = os.path.dirname(os.path.abspath(__file__))
CLAVE = "clave-de-prueba-local"


def puerto_abierto(puerto: int) -> bool:
    try:
        with socket.create_connection(("127.0.0.1", puerto), timeout=0.3):
            return True
    except OSError:
        return False


def esperar(puerto: int, abierto: bool, intentos: int = 40) -> bool:
    for _ in range(intentos):
        if puerto_abierto(puerto) == abierto:
            return True
        time.sleep(0.25)
    return False


def lanzar(nombre: str) -> subprocess.Popen:
    entorno = dict(os.environ, LAB07_MSF_PASSWORD=CLAVE, LAB07_TOR_PASSWORD=CLAVE)
    return subprocess.Popen([sys.executable, os.path.join(AQUI, nombre)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=entorno)


class SimuladoresTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["LAB07_MSF_PASSWORD"] = CLAVE
        os.environ["LAB07_TOR_PASSWORD"] = CLAVE
        cls.procesos = [lanzar("simulador_msfrpcd.py"), lanzar("simulador_tor.py")]
        if not (esperar(55553, True) and esperar(9051, True) and esperar(10021, True)):
            cls.tearDownClass()
            raise unittest.SkipTest("los simuladores no arrancaron a tiempo")

    @classmethod
    def tearDownClass(cls):
        for proceso in getattr(cls, "procesos", []):
            proceso.terminate()
        for proceso in getattr(cls, "procesos", []):
            try:
                proceso.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proceso.kill()
        esperar(55553, False)  # espera a que el panel libere el puerto

    def test_escaneo_encuentra_puertos_abiertos(self):
        cliente = msf_cliente.conectar()
        resultado = msf_cliente.ejecutar_portscan(cliente, "127.0.0.1")
        self.assertEqual(resultado["lab_puertos_abiertos"], [10021, 10022, 10080])

    def test_control_de_anonimato_responde(self):
        controlador = tor_control.conectar()
        self.assertEqual(tor_control.version(controlador), "0.4.8.10")
        tor_control.rotar_circuito(controlador)  # no debe lanzar error
        controlador.close()


if __name__ == "__main__":
    unittest.main()
