"""
Sistema de Monitoreo con Selenium - Zhao Chi E-Commerce
Monitorea el rendimiento, disponibilidad y funcionalidad del sitio
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
import time
import json
from datetime import datetime, timedelta
import statistics
import os
import sys

# Configuración
URL_BASE = 'http://127.0.0.1:5000'
INTERVALO_MONITOREO = 60  # segundos entre cada chequeo
TIEMPO_MAX_CARGA = 5  # segundos

class MonitoreoZhaoChi:
    """Clase principal para monitoreo del sitio Zhao Chi"""
    
    def __init__(self, url_base=URL_BASE):
        self.url_base = url_base
        self.driver = None
        self.resultados = []
        self.alertas = []
        self.metricas = {
            "tiempos_carga": [],
            "errores_detectados": 0,
            "paginas_monitore adas": 0,
            "ultima_ejecucion": None
        }
    
    def iniciar_navegador(self):
        """Inicializa el navegador Chrome para monitoreo"""
        print("[INICIO] Inicializando navegador Chrome...")
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--start-maximized')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--headless')  # Modo sin interfaz gráfica
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            
            # Buscar ChromeDriver
            chromedriver_path = self._buscar_chromedriver()
            
            if chromedriver_path:
                service = Service(chromedriver_path)
                self.driver = webdriver.Chrome(service=service, options=options)
            else:
                self.driver = webdriver.Chrome(options=options)
            
            print("[OK] Navegador iniciado correctamente")
            return True
        except Exception as e:
            print(f"[ERROR] No se pudo iniciar el navegador: {str(e)}")
            return False
    
    def _buscar_chromedriver(self):
        """Busca ChromeDriver en ubicaciones comunes"""
        rutas_posibles = [
            'chromedriver-win64/chromedriver-win64/chromedriver.exe',
            '../Semana 6/chromedriver-win64/chromedriver-win64/chromedriver.exe',
            '../Semana 3/chromedriver-win64/chromedriver-win64/chromedriver.exe',
            'chromedriver.exe'
        ]
        
        for ruta in rutas_posibles:
            if os.path.exists(ruta):
                return ruta
        
        return None
    
    def cerrar_navegador(self):
        """Cierra el navegador"""
        if self.driver:
            self.driver.quit()
            print("[CIERRE] Navegador cerrado")
    
    def monitorear_disponibilidad(self):
        """Verifica si el sitio está disponible (up/down)"""
        print("\n[TEST] Monitoreando disponibilidad...")
        inicio = time.time()
        
        try:
            self.driver.get(self.url_base)
            tiempo_carga = time.time() - inicio
            
            # Verificar que la página cargó
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            estado = "UP"
            if tiempo_carga > TIEMPO_MAX_CARGA:
                self._generar_alerta(
                    nivel="WARNING",
                    mensaje=f"Sitio lento: {tiempo_carga:.2f}s (límite: {TIEMPO_MAX_CARGA}s)",
                    metrica="tiempo_carga",
                    valor=tiempo_carga
                )
            
            resultado = {
                "test": "Disponibilidad",
                "estado": estado,
                "tiempo_carga": tiempo_carga,
                "timestamp": datetime.now().isoformat(),
                "url": self.url_base
            }
            
            self.metricas["tiempos_carga"].append(tiempo_carga)
            self.metricas["paginas_monitoreadas"] += 1
            
            print(f"[OK] Sitio disponible - Tiempo de carga: {tiempo_carga:.2f}s")
            return resultado
            
        except TimeoutException:
            print("[CRITICAL] Sitio no responde - TIMEOUT")
            self._generar_alerta(
                nivel="CRITICAL",
                mensaje="Sitio web no responde (timeout)",
                metrica="disponibilidad",
                valor=0
            )
            self.metricas["errores_detectados"] += 1
            return {
                "test": "Disponibilidad",
                "estado": "DOWN",
                "error": "Timeout",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"[ERROR] Error en verificación: {str(e)}")
            self._generar_alerta(
                nivel="ERROR",
                mensaje=f"Error al verificar disponibilidad: {str(e)}",
                metrica="disponibilidad",
                valor=0
            )
            self.metricas["errores_detectados"] += 1
            return {
                "test": "Disponibilidad",
                "estado": "ERROR",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def monitorear_funcionalidad_busqueda(self):
        """Verifica que la funcionalidad de búsqueda funcione"""
        print("\n[TEST] Monitoreando funcionalidad de búsqueda...")
        inicio = time.time()
        
        try:
            # Navegar a productos
            self.driver.get(f"{self.url_base}/productos")
            
            # Esperar que cargue la página
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            tiempo_carga = time.time() - inicio
            
            # Verificar que hay productos mostrados
            try:
                productos = self.driver.find_elements(By.CLASS_NAME, "producto")
                cantidad_productos = len(productos)
                
                if cantidad_productos > 0:
                    print(f"[OK] Búsqueda funcionando - {cantidad_productos} productos encontrados")
                    print(f"     Tiempo de carga: {tiempo_carga:.2f}s")
                    
                    self.metricas["tiempos_carga"].append(tiempo_carga)
                    self.metricas["paginas_monitoreadas"] += 1
                    
                    return {
                        "test": "Funcionalidad Búsqueda",
                        "estado": "OK",
                        "tiempo_carga": tiempo_carga,
                        "productos_encontrados": cantidad_productos,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    print("[WARNING] No se encontraron productos")
                    self._generar_alerta(
                        nivel="WARNING",
                        mensaje="Catálogo de productos vacío",
                        metrica="productos",
                        valor=0
                    )
                    return {
                        "test": "Funcionalidad Búsqueda",
                        "estado": "WARNING",
                        "mensaje": "No hay productos",
                        "timestamp": datetime.now().isoformat()
                    }
            except NoSuchElementException:
                print("[ERROR] No se pudo encontrar la lista de productos")
                self.metricas["errores_detectados"] += 1
                return {
                    "test": "Funcionalidad Búsqueda",
                    "estado": "ERROR",
                    "error": "Elementos no encontrados",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f"[ERROR] Error en búsqueda: {str(e)}")
            self._generar_alerta(
                nivel="ERROR",
                mensaje=f"Error en funcionalidad de búsqueda: {str(e)}",
                metrica="funcionalidad",
                valor=0
            )
            self.metricas["errores_detectados"] += 1
            return {
                "test": "Funcionalidad Búsqueda",
                "estado": "ERROR",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def monitorear_carrito_compras(self):
        """Verifica que el carrito de compras funcione"""
        print("\n[TEST] Monitoreando funcionalidad del carrito...")
        inicio = time.time()
        
        try:
            # Ir a la página del carrito
            self.driver.get(f"{self.url_base}/carrito")
            
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            tiempo_carga = time.time() - inicio
            
            print(f"[OK] Carrito accesible")
            print(f"     Tiempo de carga: {tiempo_carga:.2f}s")
            
            self.metricas["tiempos_carga"].append(tiempo_carga)
            self.metricas["paginas_monitoreadas"] += 1
            
            if tiempo_carga > TIEMPO_MAX_CARGA:
                self._generar_alerta(
                    nivel="WARNING",
                    mensaje=f"Carrito lento: {tiempo_carga:.2f}s",
                    metrica="tiempo_carga_carrito",
                    valor=tiempo_carga
                )
            
            return {
                "test": "Funcionalidad Carrito",
                "estado": "OK",
                "tiempo_carga": tiempo_carga,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"[ERROR] Error en carrito: {str(e)}")
            self._generar_alerta(
                nivel="ERROR",
                mensaje=f"Error en carrito de compras: {str(e)}",
                metrica="funcionalidad_carrito",
                valor=0
            )
            self.metricas["errores_detectados"] += 1
            return {
                "test": "Funcionalidad Carrito",
                "estado": "ERROR",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def monitorear_checkout(self):
        """Verifica que el proceso de checkout funcione"""
        print("\n[TEST] Monitoreando proceso de checkout...")
        inicio = time.time()
        
        try:
            self.driver.get(f"{self.url_base}/checkout")
            
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            tiempo_carga = time.time() - inicio
            
            print(f"[OK] Checkout accesible")
            print(f"     Tiempo de carga: {tiempo_carga:.2f}s")
            
            self.metricas["tiempos_carga"].append(tiempo_carga)
            self.metricas["paginas_monitoreadas"] += 1
            
            if tiempo_carga > TIEMPO_MAX_CARGA:
                self._generar_alerta(
                    nivel="WARNING",
                    mensaje=f"Checkout lento: {tiempo_carga:.2f}s (CRÍTICO para conversiones)",
                    metrica="tiempo_carga_checkout",
                    valor=tiempo_carga
                )
            
            return {
                "test": "Proceso Checkout",
                "estado": "OK",
                "tiempo_carga": tiempo_carga,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"[ERROR] Error en checkout: {str(e)}")
            self._generar_alerta(
                nivel="CRITICAL",
                mensaje=f"Checkout NO FUNCIONA - Pérdida de ventas: {str(e)}",
                metrica="funcionalidad_checkout",
                valor=0
            )
            self.metricas["errores_detectados"] += 1
            return {
                "test": "Proceso Checkout",
                "estado": "ERROR",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def monitorear_health_endpoint(self):
        """Verifica el endpoint de health check"""
        print("\n[TEST] Monitoreando health endpoint...")
        
        try:
            self.driver.get(f"{self.url_base}/health")
            
            # Obtener el contenido JSON
            body = self.driver.find_element(By.TAG_NAME, "body").text
            
            if "healthy" in body:
                print("[OK] Health check: Sistema saludable")
                return {
                    "test": "Health Check",
                    "estado": "OK",
                    "respuesta": body,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                print("[WARNING] Health check reporta problemas")
                self._generar_alerta(
                    nivel="WARNING",
                    mensaje="Health check reporta sistema unhealthy",
                    metrica="health",
                    valor=0
                )
                return {
                    "test": "Health Check",
                    "estado": "WARNING",
                    "respuesta": body,
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f"[ERROR] Health endpoint no responde: {str(e)}")
            self._generar_alerta(
                nivel="ERROR",
                mensaje="Health endpoint no accesible",
                metrica="health",
                valor=0
            )
            return {
                "test": "Health Check",
                "estado": "ERROR",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _generar_alerta(self, nivel, mensaje, metrica, valor):
        """Genera una alerta y la guarda"""
        alerta = {
            "nivel": nivel,
            "mensaje": mensaje,
            "metrica": metrica,
            "valor": valor,
            "timestamp": datetime.now().isoformat()
        }
        
        self.alertas.append(alerta)
        
        # Imprimir con formato según el nivel
        simbolo = {
            "INFO": "[INFO]",
            "WARNING": "[ADVERTENCIA]",
            "ERROR": "[ERROR]",
            "CRITICAL": "[CRÍTICO]"
        }.get(nivel, "[ALERTA]")
        
        print(f"{simbolo} {mensaje}")
    
    def ejecutar_ciclo_monitoreo(self):
        """Ejecuta un ciclo completo de monitoreo"""
        print("\n" + "=" * 70)
        print("INICIANDO CICLO DE MONITOREO")
        print(f"Fecha/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        if not self.iniciar_navegador():
            print("[ERROR] No se pudo iniciar el navegador. Abortando monitoreo.")
            return None
        
        try:
            # Ejecutar todas las pruebas
            resultados_ciclo = {
                "inicio": datetime.now().isoformat(),
                "pruebas": []
            }
            
            # 1. Disponibilidad
            resultados_ciclo["pruebas"].append(self.monitorear_disponibilidad())
            time.sleep(1)
            
            # 2. Búsqueda
            resultados_ciclo["pruebas"].append(self.monitorear_funcionalidad_busqueda())
            time.sleep(1)
            
            # 3. Carrito
            resultados_ciclo["pruebas"].append(self.monitorear_carrito_compras())
            time.sleep(1)
            
            # 4. Checkout
            resultados_ciclo["pruebas"].append(self.monitorear_checkout())
            time.sleep(1)
            
            # 5. Health Check
            resultados_ciclo["pruebas"].append(self.monitorear_health_endpoint())
            
            resultados_ciclo["fin"] = datetime.now().isoformat()
            resultados_ciclo["alertas_generadas"] = len(self.alertas)
            
            # Guardar resultados
            self.resultados.append(resultados_ciclo)
            self.metricas["ultima_ejecucion"] = datetime.now().isoformat()
            
            # Mostrar resumen
            self._mostrar_resumen_ciclo(resultados_ciclo)
            
            return resultados_ciclo
            
        finally:
            self.cerrar_navegador()
    
    def _mostrar_resumen_ciclo(self, resultados):
        """Muestra un resumen del ciclo de monitoreo"""
        print("\n" + "-" * 70)
        print("RESUMEN DEL CICLO DE MONITOREO")
        print("-" * 70)
        
        total_pruebas = len(resultados["pruebas"])
        pruebas_ok = sum(1 for p in resultados["pruebas"] if p.get("estado") == "OK")
        pruebas_warning = sum(1 for p in resultados["pruebas"] if p.get("estado") == "WARNING")
        pruebas_error = sum(1 for p in resultados["pruebas"] if p.get("estado") in ["ERROR", "DOWN"])
        
        print(f"Total de pruebas: {total_pruebas}")
        print(f"  OK: {pruebas_ok}")
        print(f"  WARNING: {pruebas_warning}")
        print(f"  ERROR: {pruebas_error}")
        
        if self.metricas["tiempos_carga"]:
            promedio = statistics.mean(self.metricas["tiempos_carga"])
            print(f"\nTiempo promedio de carga: {promedio:.2f}s")
        
        print(f"Alertas generadas en este ciclo: {resultados['alertas_generadas']}")
        
        # Estado general
        if pruebas_error > 0:
            print("\nESTADO GENERAL: CRÍTICO")
        elif pruebas_warning > 0:
            print("\nESTADO GENERAL: ADVERTENCIA")
        else:
            print("\nESTADO GENERAL: TODO OK")
        
        print("=" * 70)
    
    def generar_reporte(self):
        """Genera un reporte completo en JSON"""
        if not self.metricas["tiempos_carga"]:
            promedio_tiempo = 0
            min_tiempo = 0
            max_tiempo = 0
        else:
            promedio_tiempo = statistics.mean(self.metricas["tiempos_carga"])
            min_tiempo = min(self.metricas["tiempos_carga"])
            max_tiempo = max(self.metricas["tiempos_carga"])
        
        reporte = {
            "fecha_generacion": datetime.now().isoformat(),
            "resumen": {
                "total_ciclos": len(self.resultados),
                "paginas_monitoreadas": self.metricas["paginas_monitoreadas"],
                "errores_detectados": self.metricas["errores_detectados"],
                "alertas_totales": len(self.alertas)
            },
            "rendimiento": {
                "tiempo_promedio_carga": f"{promedio_tiempo:.2f}s",
                "tiempo_min_carga": f"{min_tiempo:.2f}s",
                "tiempo_max_carga": f"{max_tiempo:.2f}s"
            },
            "alertas_recientes": self.alertas[-10:] if self.alertas else [],
            "ultimos_resultados": self.resultados[-5:] if self.resultados else []
        }
        
        # Guardar en archivo
        nombre_archivo = f"reporte_monitoreo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)
        
        print(f"\n[GUARDADO] Reporte generado: {nombre_archivo}")
        return reporte
    
    def monitoreo_continuo(self, duracion_minutos=60):
        """Ejecuta monitoreo continuo por un período determinado"""
        print("=" * 70)
        print("MONITOREO CONTINUO INICIADO")
        print(f"Duración: {duracion_minutos} minutos")
        print(f"Intervalo: {INTERVALO_MONITOREO} segundos entre ciclos")
        print("Presiona Ctrl+C para detener el monitoreo")
        print("=" * 70)
        
        tiempo_fin = datetime.now() + timedelta(minutes=duracion_minutos)
        ciclo_numero = 1
        
        try:
            while datetime.now() < tiempo_fin:
                print(f"\n\n{'#' * 70}")
                print(f"CICLO #{ciclo_numero}")
                print(f"{'#' * 70}")
                
                self.ejecutar_ciclo_monitoreo()
                ciclo_numero += 1
                
                if datetime.now() < tiempo_fin:
                    print(f"\n[ESPERA] Próximo ciclo en {INTERVALO_MONITOREO} segundos...")
                    time.sleep(INTERVALO_MONITOREO)
                    
        except KeyboardInterrupt:
            print("\n\n[INTERRUPCIÓN] Monitoreo detenido por el usuario")
        
        # Generar reporte final
        print("\n[FINALIZANDO] Generando reporte final...")
        self.generar_reporte()
        print("\n[COMPLETADO] Monitoreo finalizado")


def main():
    """Función principal"""
    print("""
    ================================================================================
                    SISTEMA DE MONITOREO - ZHAO CHI E-COMMERCE
                           Monitoreo con Selenium
    ================================================================================
    
    Este sistema monitorea:
    - Disponibilidad del sitio (up/down)
    - Tiempos de carga de páginas
    - Funcionalidad de búsqueda y catálogo
    - Funcionalidad del carrito de compras
    - Proceso de checkout
    - Health checks del sistema
    
    ================================================================================
    """)
    
    print("\n[IMPORTANTE] Asegúrate de que el sitio web esté ejecutándose")
    print("             Ejecuta primero: python sitio_zhao_chi.py")
    print()
    
    # Menú de opciones
    print("Opciones de monitoreo:")
    print("1. Ejecutar un ciclo único de monitoreo")
    print("2. Monitoreo continuo (60 minutos)")
    print("3. Monitoreo continuo personalizado")
    print()
    
    opcion = input("Selecciona una opción (1-3): ").strip()
    
    monitor = MonitoreoZhaoChi()
    
    if opcion == "1":
        monitor.ejecutar_ciclo_monitoreo()
        monitor.generar_reporte()
    elif opcion == "2":
        monitor.monitoreo_continuo(duracion_minutos=60)
    elif opcion == "3":
        try:
            duracion = int(input("Duración en minutos: "))
            monitor.monitoreo_continuo(duracion_minutos=duracion)
        except ValueError:
            print("[ERROR] Duración inválida")
    else:
        print("[ERROR] Opción inválida")
    
    print("\n[FIN] Programa terminado")


if __name__ == '__main__':
    main()
