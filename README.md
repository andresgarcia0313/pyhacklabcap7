<!-- Idioma del documento: es-CO (español de Colombia) -->
# Laboratorio 7: controlar Metasploit y una red de anonimato desde Python

Curso Seguridad informática con Python (PYT_HACK), capítulo 7: integración práctica.

En este laboratorio usted controla, desde Python, el panel de Metasploit por RPC (Remote Procedure Call, llamada a procedimiento remoto): le pide que cargue su escáner de puertos y lo ejecute contra un objetivo del laboratorio. Luego gobierna el puerto de control de una red de anonimato: consulta su versión y le pide un camino nuevo.

Todo ocurre **en su propio equipo, sin máquinas virtuales**. Dos simuladores incluidos hacen de "panel de Metasploit" y de "puerto de control": escuchan en `127.0.0.1`, hablan los mismos protocolos que los servicios reales y no dejan salir ni un paquete. Nada de tráfico real por la red de anonimato: solo se envían órdenes de control.

## Dos lados: la práctica y la respuesta

| Carpeta | Qué contiene | Quién la usa |
|---|---|---|
| [`paso-a-paso/`](paso-a-paso/) | **La práctica.** La guía [`paso-a-paso/README.md`](paso-a-paso/README.md) y el material de apoyo (los dos simuladores, comprobaciones por paso, validación y pruebas). Usted crea los cinco archivos de la herramienta pegando el código de la guía, comentado línea a línea para quien ve Python por primera vez. | Estudiante |
| [`solucion/`](solucion/) | **La respuesta.** Los cinco archivos terminados y el laboratorio completo funcionando, con sus salidas reales en [`solucion/output.md`](solucion/output.md). | Estudiante que quiera comparar, e instructor |

Recomendación: haga primero la práctica y abra la solución solo para comparar cuando algo no le funcione (`diff config.py ../solucion/config.py`).

## Empezar

```bash
git clone https://github.com/andresgarcia0313/pyhacklabcap7.git
cd pyhacklabcap7/paso-a-paso
```

Luego abra [`paso-a-paso/README.md`](paso-a-paso/README.md) y siga el Paso 0.

¿Solo quiere ver la herramienta funcionando? Desde la carpeta `pyhacklabcap7`, ejecute la solución:

```bash
cd solucion
./ejecutar_laboratorio.sh
```

## Qué va a aprender

1. Conectarse al panel de Metasploit por RPC con la librería `pymetasploit3`.
2. Cargar un módulo auxiliar y ejecutarlo con sus opciones desde Python.
3. Controlar una red de anonimato por su puerto de control con la librería `stem`.
4. Pedir un camino nuevo con la señal NEWNYM, sin enrutar tráfico.
5. Encadenar las dos piezas en un flujo: primero escanear, después rotar.
6. Aplicar controles de uso responsable: objetivo permitido y claves en variables de entorno.

No necesita saber Python: la guía y los comentarios del código lo explican desde cero. Requisitos: Python 3.10 o superior en Linux, macOS o Windows con WSL (Windows Subsystem for Linux, subsistema de Linux para Windows). El detalle está en la guía.

## Para el instructor

- `./comprobar_repositorio.sh`: verifica que el material de apoyo sea igual en ambas carpetas y que el código de la guía sea idéntico al de la solución. Además ejecuta el laboratorio completo dos veces, con la solución y con el código copiado de la guía, como lo haría un estudiante. Debe terminar en `REPOSITORIO CORRECTO`.
- `herramientas/comprobar_guia.py`: la parte de esa verificación que compara la guía con la solución y cuenta las líneas de código de cada archivo.

## Uso responsable

Use estas herramientas solo sobre sistemas con autorización escrita. No escanee redes ajenas ni la red de su casa u oficina. El control de objetivo del laboratorio acepta solo `127.0.0.1`, y las claves siempre se leen de variables de entorno.

## Control de cambios

| Versión | Fecha | Autor | Descripción del cambio |
|---|---|---|---|
| 1.0.0 | 2026-10-20 | Andrés García | Laboratorio 7 de integración con Metasploit por RPC y control de una red de anonimato, en ejecución local, con dos simuladores, pruebas automáticas y guía paso a paso. |
