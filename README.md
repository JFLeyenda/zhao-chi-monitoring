# 🛡️ Sistema de Monitoreo Zhao Chi E-commerce

Sistema de monitoreo en tiempo real para detectar y prevenir problemas de rendimiento y disponibilidad en el sitio web de Zhao Chi durante eventos de alta demanda.

## 🎯 Objetivo

Implementar monitoreo proactivo que detecte problemas antes de que afecten a los clientes, especialmente durante Black Friday, Cyber Monday y promociones especiales.

## 📋 Contexto del Proyecto

Zhao Chi es una empresa de e-commerce que experimenta problemas de rendimiento y caídas del sistema durante eventos de alta demanda. Este proyecto implementa un sistema de monitoreo completo para:

- Detectar problemas de rendimiento antes de que afecten a usuarios
- Generar alertas automáticas con diferentes niveles de severidad
- Analizar tendencias para predecir problemas futuros
- Proporcionar métricas en tiempo real del sistema

## 🛠️ Tecnologías Utilizadas

- **Python 3.11+**
- **Flask 3.0.0** - Framework web para simulación del sitio
- **Selenium 4.15.0** - Monitoreo sintético automatizado
- **ChromeDriver** - Driver para automatización de navegador

## 📦 Instalación

```bash
# Clonar repositorio
git clone https://github.com/TU-USUARIO/zhao-chi-monitoring.git
cd zhao-chi-monitoring

# Instalar dependencias
pip install -r requirements.txt
```

## 🚀 Uso

### 1. Iniciar el sitio web simulado

```bash
python sitio_zhao_chi.py
```

El sitio estará disponible en: http://localhost:5000

### 2. Ejecutar el sistema de monitoreo

En otra terminal:

```bash
python monitoreo_selenium.py
```

Opciones disponibles:
- **Opción 1**: Ejecutar un ciclo único de monitoreo
- **Opción 2**: Monitoreo continuo por 60 minutos
- **Opción 3**: Monitoreo continuo con duración personalizada

## 📊 Características

- ✅ **Monitoreo Sintético**: Simula comportamiento de usuarios reales
- ✅ **Sistema de Alertas Multi-nivel**: INFO, WARNING, ERROR, CRITICAL
- ✅ **Análisis de Tendencias**: Detecta patrones y predice problemas
- ✅ **Reportes JSON**: Exporta métricas y estadísticas
- ✅ **Medición de Rendimiento**: Tiempos de carga, disponibilidad, errores

## 🔔 Sistema de Alertas

### Niveles de Severidad

| Nivel | Color | Descripción | Acción |
|-------|-------|-------------|--------|
| **INFO** | 🔵 Azul | Eventos informativos | Registro únicamente |
| **WARNING** | 🟡 Amarillo | Degradación de rendimiento | Revisar cuando sea conveniente |
| **ERROR** | 🟠 Naranja | Problemas que requieren atención | Revisar en próximas horas |
| **CRITICAL** | 🔴 Rojo | Fallas críticas del sistema | Atención inmediata |

### Umbrales Configurados

- **Verde (OK)**: Tiempo de carga < 2 segundos
- **Amarillo (WARNING)**: Tiempo de carga 2-4 segundos
- **Rojo (ERROR)**: Tiempo de carga > 4 segundos
- **Crítico**: Sitio no responde

## 📈 Tipos de Monitoreo Implementados

1. **Monitoreo Sintético**: Verifica funcionalidad del sitio simulando usuarios
2. **Monitoreo de Disponibilidad**: Verifica que el sitio esté accesible
3. **Monitoreo de Funcionalidad**: Prueba búsqueda, carrito, checkout
4. **Monitoreo de Rendimiento**: Mide tiempos de respuesta
5. **Health Checks**: Verifica estado del endpoint /health

## 📁 Estructura del Proyecto

```
zhao-chi-monitoring/
├── sitio_zhao_chi.py          # Aplicación web Flask simulada
├── monitoreo_selenium.py       # Sistema de monitoreo con Selenium
├── requirements.txt            # Dependencias Python
├── templates/                  # Plantillas HTML
│   ├── index.html             # Página principal
│   ├── productos.html         # Catálogo de productos
│   ├── producto.html          # Detalle de producto
│   ├── carrito.html           # Carrito de compras
│   └── checkout.html          # Proceso de pago
├── chromedriver-win64/        # ChromeDriver para Selenium
├── Informe_Tarea_Semana7.txt  # Informe completo del proyecto
├── GUIA_CAPTURAS.txt          # Guía para capturas de pantalla
└── README.md                  # Este archivo
```

## 📖 Documentación Adicional

- **Informe completo**: Ver `Informe_Tarea_Semana7.txt` para análisis detallado
- **Guía de capturas**: Ver `GUIA_CAPTURAS.txt` para documentación visual
- **Guía GitHub**: Ver `GUIA_GITHUB_CAPTURAS.txt` para integración con GitHub

## 🎯 Plan de Implementación

El proyecto sigue un plan de 4 fases:

1. **Fase 1** (Semana 1-2): Definir qué monitorear
2. **Fase 2** (Semana 3-5): Implementar herramientas
3. **Fase 3** (Semana 6): Configurar alertas y visualización
4. **Fase 4** (Semana 7+): Preparación y mejora continua

## 🧪 Pruebas Implementadas

El sistema ejecuta las siguientes pruebas automáticas:

- ✅ Verificación de disponibilidad del sitio
- ✅ Medición de tiempo de carga de páginas
- ✅ Prueba de funcionalidad de búsqueda
- ✅ Verificación de carrito de compras
- ✅ Prueba de proceso de checkout
- ✅ Validación de health endpoint

## 📊 Métricas y Reportes

El sistema genera reportes JSON con:

- Tiempos de carga por página
- Número de errores detectados
- Disponibilidad del sistema
- Alertas generadas
- Análisis de tendencias

## 🎓 Contexto Académico

Este proyecto fue desarrollado como parte de la asignatura **Evaluación de Sistemas QA** en el Instituto IACC, para la Semana 7: "Monitoreo de Sistemas en Producción".

### Indicadores de Evaluación Cubiertos

- ✅ Comprensión de monitoreo en tiempo real
- ✅ Implementación de diferentes tipos de monitoreo
- ✅ Configuración de alertas proactivas
- ✅ Análisis de tendencias y predicción
- ✅ Prácticas recomendadas de SRE

## 👤 Autor

Proyecto académico desarrollado para IACC  
Asignatura: Evaluación de Sistemas QA  
Semana 7 - Enero 2026

## 📄 Licencia

Proyecto académico con fines educativos.

---

**Nota**: Este es un proyecto de demostración académica. El sitio web y el sistema de monitoreo son simulaciones para propósitos educativos.
