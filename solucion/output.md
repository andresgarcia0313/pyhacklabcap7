<!-- Idioma del documento: es-CO (español de Colombia) -->
# Salidas reales del laboratorio 7

Ejecución del 2026-10-20 en Linux con Python 3.14 y stem 1.8.2. Cada bloque muestra el comando y su salida sin editar. Los identificadores internos (como el `uuid` de cada ejecución) cambian en cada corrida.

## Paso 0: dependencias

```bash
python3 -c "import pymetasploit3, stem, msgpack; print('Dependencias OK')"
```

```text
Dependencias OK
```

## Paso 1: configuración

```bash
python3 pasos/paso1_configuracion.py
```

```text
Panel de Metasploit: 127.0.0.1:55553 (ssl=False)
Control de anonimato: 127.0.0.1:9051
Red permitida: 127.0.0.1/32
Puertos del objetivo: 10021,10022,10025,10080,13306
Clave del panel en la variable: LAB07_MSF_PASSWORD
Clave del control en la variable: LAB07_TOR_PASSWORD

Prueba del control de objetivo:
  127.0.0.1        permitido=True
  203.0.113.10     permitido=False
  127.0.0.0/8      permitido=False
```

## Paso 2: panel de Metasploit y escaneo

```bash
python3 pasos/paso2_msf.py
```

```text
Conectando al panel de Metasploit...
Conectado. Lanzando el escáner de puertos sobre 127.0.0.1...
Puertos abiertos: [10021, 10022, 10080]

Ahora con un objetivo NO permitido (debe ser rechazado):
  Rechazado correctamente: 203.0.113.10 no pertenece a la red permitida (127.0.0.1/32)
```

## Paso 3: control de la red de anonimato

```bash
python3 pasos/paso3_tor.py
```

```text
Conectando al puerto de control...
Versión del servicio: 0.4.8.10
Pidiendo un camino nuevo (señal NEWNYM)...
Camino nuevo solicitado. Sin tráfico real por la red de anonimato.
```

## Paso 4: flujo integrado

```bash
python3 pasos/paso4_integracion.py
```

```text
Ejecutando el flujo: primero escaneo, después camino nuevo...
Puertos abiertos (del escaneo): [10021, 10022, 10080]
El camino nuevo ya se pidió después del escaneo.
```

## Paso 5: programa principal

```bash
python3 lab07.py
```

```text
== Laboratorio 7: Metasploit por RPC y control de anonimato (local) ==
[*] Objetivo: 127.0.0.1 | Puertos: 10021,10022,10025,10080,13306
[*] Versión del servicio de anonimato: 0.4.8.10
[+] Puertos abiertos en el objetivo: [10021, 10022, 10080]
[+] Se pidió un camino nuevo (señal NEWNYM)
LABORATORIO COMPLETADO
```

## Pruebas automáticas

```bash
python3 -m unittest test_red_permitida test_integracion test_simuladores
```

```text
----------------------------------------------------------------------
Ran 10 tests in 0.30s

OK
```

## Validación final

```bash
python3 validar.py
```

```text
Parte A: control de uso responsable (sin red)
  PASS | 127.0.0.1 permitido: obtenido=True esperado=True
  PASS | 203.0.113.10 permitido: obtenido=False esperado=False
  PASS | red entera 127.0.0.0/8 permitida: obtenido=False esperado=False
  PASS | escáner rechaza objetivo ajeno: obtenido='PermissionError' esperado='PermissionError'

Parte B: ronda local contra los simuladores
  PASS | puertos abiertos del escaneo: obtenido=[10021, 10022, 10080] esperado=[10021, 10022, 10080]
  PASS | versión del servicio de anonimato: obtenido='0.4.8.10' esperado='0.4.8.10'
  PASS | el flujo devuelve el resultado del escaneo: obtenido=[10021, 10022, 10080] esperado=[10021, 10022, 10080]

Resultado final: TODO PASA
```
