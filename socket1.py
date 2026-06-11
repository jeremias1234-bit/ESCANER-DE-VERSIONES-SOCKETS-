import socket
import time

def obtener_version_servicio(ip, puerto, tiempo_espera):
    # Creamos un socket estándar TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Aplicamos el timeout dinámico que ingresó el usuario
    s.settimeout(tiempo_espera)
    
    try:
        # Intenta conectar de verdad al puerto
        s.connect((ip, puerto))
        
        # ESCENARIO A: Captura rápida del banner de entrada (SSH, FTP, etc.)
        banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
        
        # ESCENARIO B: Petición HTTP manual para servidores web
        if not banner and puerto in [80,443,8080,8888]:
            s.sendall(b"HEAD / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
            respuesta_http = s.recv(1024).decode('utf-8', errors='ignore')
            
            for linea in respuesta_http.split("\n"):
                if "Server:" in linea:
                    return linea.replace("Server:", "").strip()
            return "Servicio Web (No especificó versión en la cabecera)"
            
        if banner:
            return banner
        else:
            return "Servicio activo (No expone Banner de versión público)"
            
    except Exception:
        return None  # Si tira error o está cerrado, devolvemos None para no llenar la pantalla
    finally:
        s.close()

# ==============================================================================
#   PANEL DE CONTROL INTERACTIVO (INPUTS DEL USUARIO)
# ==============================================================================
print("==================================================")
print("   AUDITORÍA DE VERSIONES - BANNER GRABBING CLI")
print("==================================================")
ip_objetivo = input("[>] Ingrese la IP OBJETIVO (ej: 192.168.1.1): ")
puerto_inicio = int(input("[>] Ingrese el puerto de INICIO (ej: 20): "))
puerto_fin = int(input("[>] Ingrese el puerto de FIN (ej: 85): "))
tiempo_maximo = float(input("[>] Ingrese el tiempo de espera por puerto en seg (ej: 1.0): "))
print("==================================================\n")

# Estructuración del rango numérico sumando 1 para incluir el último puerto
puertos_a_escanear = range(puerto_inicio, puerto_fin + 1)

print(f"[+] Iniciando análisis de servicios sobre {ip_objetivo}...")
print(f"[+] Escaneando rango {puerto_inicio}-{puerto_fin} | Timeout: {tiempo_maximo}s\n")

tiempo_inicio = time.time()

#  BUCLE DE AUTOMATIZACIÓN DE AUDITORÍA
for puerto in puertos_a_escanear:
    info_servicio = obtener_version_servicio(ip_objetivo, puerto, tiempo_maximo)
    
    # Si la función nos devolvió datos (el puerto estaba abierto y respondió)
    if info_servicio is not None:
        print(f"[>] PUERTO {puerto} ABIERTO -> Información detectada: {info_servicio}")

# Cierre del proceso y cálculo de rendimiento temporal
tiempo_total = time.time() - tiempo_inicio
print(f"\n[+] Auditoría finalizada con éxito en {tiempo_total:.2f} segundos.")
