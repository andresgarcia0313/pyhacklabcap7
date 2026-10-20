"""Prueba del flujo integrado. Usa piezas de mentira: nada sale a la red."""
import unittest

import integracion


class IntegracionTest(unittest.TestCase):
    def test_escanea_antes_de_rotar(self):
        orden = []

        def escanear_falso(cliente, objetivo):
            orden.append("escanear")
            return {"lab_puertos_abiertos": [10021, 10080], "objetivo": objetivo}

        def rotar_falso(controlador):
            orden.append("rotar")

        resultado = integracion.flujo("127.0.0.1", "cliente", "controlador",
                                      escanear=escanear_falso, rotar=rotar_falso)
        # El escaneo debe ocurrir ANTES que la rotación del camino.
        self.assertEqual(orden, ["escanear", "rotar"])
        # El flujo devuelve lo que halló el escaneo.
        self.assertEqual(resultado["lab_puertos_abiertos"], [10021, 10080])
        self.assertEqual(resultado["objetivo"], "127.0.0.1")


if __name__ == "__main__":
    unittest.main()
