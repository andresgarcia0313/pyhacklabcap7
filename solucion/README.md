<!-- Idioma del documento: es-CO (español de Colombia) -->
# Solución del laboratorio 7

Esta carpeta es **la respuesta**: la herramienta terminada y funcionando. Si todavía no hace la práctica, empiece por la guía [`../paso-a-paso/README.md`](../paso-a-paso/README.md) y vuelva aquí solo para comparar.

## Ejecutarla

```bash
./ejecutar_laboratorio.sh
```

Prepara el entorno, corre las 10 pruebas, enciende los dos simuladores, ejecuta el programa principal, valida la ronda local y limpia. Debe terminar con `LABORATORIO COMPLETADO`. Las salidas reales de cada paso están en [`output.md`](output.md).

## Los cinco archivos de la respuesta

| Archivo | Paso de la guía | Qué hace |
|---|---|---|
| `config.py` | 1 | Datos de los servicios, objetivo permitido, nombres de las variables de entorno con las claves. |
| `msf_cliente.py` | 2 | Conexión al panel de Metasploit por RPC (Remote Procedure Call, llamada a procedimiento remoto) y escáner de puertos con control de objetivo. |
| `tor_control.py` | 3 | Control de la red de anonimato: versión y señal de camino nuevo. Solo órdenes de control, sin tráfico. |
| `integracion.py` | 4 | Flujo que escanea y después rota el circuito. |
| `lab07.py` | 5 | Programa principal: conecta, escanea, muestra y rota. |

El resto de archivos es el mismo material de apoyo de `paso-a-paso/`: los dos simuladores, las comprobaciones por paso, la validación, las pruebas y los scripts.

## Comparar con su trabajo

Desde `paso-a-paso/`:

```bash
diff msf_cliente.py ../solucion/msf_cliente.py
```

Si no hay salida, su archivo es idéntico a la respuesta. Si hay diferencias, no siempre son errores: lo que cuenta es que `python3 validar.py` y las pruebas pasen.

## Qué se corrigió frente al material original

- La clave del panel ya no aparece en el código ni en el comando de arranque: se lee de `LAB07_MSF_PASSWORD` y `LAB07_TOR_PASSWORD`.
- El escáner valida el objetivo contra la red permitida antes de tocar el panel, así nunca actúa sobre equipos ajenos.
- Todo corre en `127.0.0.1` con simuladores propios: no hace falta Metasploitable, ni máquinas virtuales, ni salida a Internet, ni tráfico real por la red de anonimato.
- Las dependencias quedan fijadas en `requirements.txt` con las versiones probadas.

## Control de cambios

| Versión | Fecha | Autor | Descripción del cambio |
|---|---|---|---|
| 1.0.0 | 2026-10-20 | Andrés García | Laboratorio 7 en ejecución local, con panel de Metasploit y puerto de control de anonimato simulados, pruebas automáticas, validación y guía paso a paso. |
