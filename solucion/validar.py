#!/usr/bin/env python3
"""
validar.py - Comprobaciones finales del laboratorio 7 (que SÍ pueden fallar).

Parte A (sin red): el control de objetivo acepta 127.0.0.1 y rechaza otras IP y
  redes enteras; el escáner se niega a tocar el panel con un objetivo no permitido.
Parte B (local): con los dos simuladores corriendo, el escaneo encuentra los
  puertos abiertos esperados, el servicio de anonimato reporta su versión y el
  flujo integrado devuelve el resultado del escaneo.

Uso: python3 validar.py   (los simuladores deben estar corriendo para la Parte B)
Sale con código 0 si todo pasa y 1 si algo falla.
"""
import sys

import config
import integracion
import msf_cliente
import tor_control

fallos = []


def comprobar(nombre: str, obtenido, esperado) -> None:
    ok = obtenido == esperado
    print(f"  {'PASS' if ok else 'FAIL'} | {nombre}: obtenido={obtenido!r} esperado={esperado!r}")
    if not ok:
        fallos.append(nombre)


class ClienteProhibido:
    """Cliente de mentira: si el escáner lo toca, la prueba falla."""

    def __getattr__(self, nombre):
        raise AssertionError(f"el escáner tocó el panel ('{nombre}') pese a un objetivo no permitido")


def validar_a() -> None:
    print("\nParte A: control de uso responsable (sin red)")
    comprobar("127.0.0.1 permitido", config.objetivo_permitido("127.0.0.1"), True)
    comprobar("203.0.113.10 permitido", config.objetivo_permitido("203.0.113.10"), False)
    comprobar("red entera 127.0.0.0/8 permitida", config.objetivo_permitido("127.0.0.0/8"), False)
    try:
        msf_cliente.ejecutar_portscan(ClienteProhibido(), "203.0.113.10")
        comprobar("escáner rechaza objetivo ajeno", "no lanzó error", "PermissionError")
    except PermissionError:
        comprobar("escáner rechaza objetivo ajeno", "PermissionError", "PermissionError")


def validar_b() -> None:
    print("\nParte B: ronda local contra los simuladores")
    try:
        cliente = msf_cliente.conectar()
        controlador = tor_control.conectar()
    except Exception as e:  # noqa: BLE001
        sys.exit(f"FAIL | no hay simuladores corriendo: {e}\n"
                 "Arranque simulador_msfrpcd.py y simulador_tor.py antes de validar.")
    resultado = msf_cliente.ejecutar_portscan(cliente, "127.0.0.1")
    comprobar("puertos abiertos del escaneo", resultado.get("lab_puertos_abiertos"),
              [10021, 10022, 10080])
    comprobar("versión del servicio de anonimato", tor_control.version(controlador), "0.4.8.10")
    flujo = integracion.flujo("127.0.0.1", cliente, controlador)
    comprobar("el flujo devuelve el resultado del escaneo",
              flujo.get("lab_puertos_abiertos"), [10021, 10022, 10080])
    controlador.close()


if __name__ == "__main__":
    validar_a()
    validar_b()
    print(f"\nResultado final: {'TODO PASA' if not fallos else f'{len(fallos)} FALLO(S): {fallos}'}")
    sys.exit(1 if fallos else 0)
