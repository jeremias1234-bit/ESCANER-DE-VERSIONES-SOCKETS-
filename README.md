# Auditoría de Versiones - Banner Grabbing CLI 🤖🔍

Este proyecto es una herramienta de consola interactiva (CLI) desarrollada en **Python** utilizando la librería nativa **`socket`**. La herramienta automatiza el proceso de auditoría y reconocimiento de red profunda, implementando técnicas de **Banner Grabbing** y **Fingerprinting** de servicios para extraer de forma precisa las versiones de software que corren detrás de los puertos abiertos en un servidor o router.

## ⚙️ ¿Cómo funciona la arquitectura lógica?

El script inicia el saludo de tres vías completo (TCP Three-Way Handshake) para abrir un canal de comunicación real y analiza el comportamiento del puerto según el tipo de protocolo:

```
[ Tu Script Python ] ─── TCP (Handshake Completo) ───> [ Puerto Objetivo ]
         │                                                      │
         ├─── Caso A (SSH/FTP): Escupe el banner solo ──────────┤
         │    (Captura directa de los primeros 1024 bytes)     │
         │                                                      │
         └─── Caso B (Web 80/443/8080): Puerto tímido ──────────┤
              (Envía HEAD / HTTP/1.1 -> Filtra cabecera Server) │
```

1. **Conexión Orientada a Flujo (TCP):** Utiliza un socket configurado con los parámetros `AF_INET` y `SOCK_STREAM` para garantizar conexiones confiables.
2. **Escenario A (Servicios Expositivos):** Captura y decodifica (`utf-8`) la cadena de bienvenida que servicios como SSH o FTP arrojan de manera automática inmediatamente después de conectar.
3. **Escenario B (Servicios Web Tímidos):** Si el banner inicial es nulo pero el puerto coincide con el espectro web estándar, el script inyecta de forma manual una cabecera de petición HTTP. Luego procesa la respuesta en búfer para extraer el valor exacto de la cabecera `"Server:"`.

## 🛠️ Atributos y Características Técnicas

* **Controles Interactivos (CLI):** Captura de datos dinámica mediante consola admitiendo filtrado estricto de tipos (`String` para IP, `Int` para rangos y `Float` para tiempos máximos).
* **Gestión de Latencia Dinámica (`settimeout`):** Permite configurar el umbral de espera por conexión para acelerar el escaneo en redes locales estables o ampliarlo ante auditorías remotas.
* **Manejador de Conexiones Silencioso:** Captura excepciones de red y puertos cerrados de manera transparente, imprimiendo en pantalla únicamente los objetivos que contienen información valiosa de versiones.

---
*Desarrollado de forma autodidacta como laboratorio práctico de análisis de cabeceras de red, protocolos de aplicación y ciberseguridad defensiva.*
