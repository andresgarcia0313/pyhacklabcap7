"""Pruebas del control de uso responsable y de la lectura de claves. Usan mocks: nada sale a la red."""
import os
import unittest
from unittest import mock

import config
import msf_cliente

FUERA_DE_LISTA = "203.0.113.10"  # TEST-NET-3 (RFC 5737): reservada para documentación


class ClienteProhibido:
    """Si el escáner intenta usar este cliente, la prueba falla."""

    def __getattr__(self, nombre):
        raise AssertionError(f"se tocó el panel ('{nombre}') con un objetivo no permitido")


class RedPermitidaTest(unittest.TestCase):
    def test_solo_loopback_permitido(self):
        self.assertTrue(config.objetivo_permitido("127.0.0.1"))

    def test_rechaza_ip_ajena(self):
        self.assertFalse(config.objetivo_permitido(FUERA_DE_LISTA))

    def test_rechaza_red_entera(self):  # un objetivo no puede ser una red completa
        self.assertFalse(config.objetivo_permitido("127.0.0.0/8"))

    def test_rechaza_texto_invalido(self):
        self.assertFalse(config.objetivo_permitido("no-es-una-ip"))

    def test_escaner_no_toca_panel_con_objetivo_ajeno(self):
        with self.assertRaises(PermissionError):
            msf_cliente.ejecutar_portscan(ClienteProhibido(), FUERA_DE_LISTA)

    def test_conectar_lee_clave_del_entorno(self):
        with mock.patch.dict(os.environ, {"LAB07_MSF_PASSWORD": "clave-del-entorno"}), \
             mock.patch.object(msf_cliente, "MsfRpcClient") as falso:
            msf_cliente.conectar()
        falso.assert_called_once_with("clave-del-entorno", server="127.0.0.1",
                                      port=55553, ssl=False)

    def test_conectar_falla_sin_clave(self):  # sin variable de entorno, no arranca
        with mock.patch.dict(os.environ, {}, clear=True), \
             mock.patch.object(msf_cliente, "MsfRpcClient"):
            with self.assertRaises(SystemExit):
                msf_cliente.conectar()


if __name__ == "__main__":
    unittest.main()
