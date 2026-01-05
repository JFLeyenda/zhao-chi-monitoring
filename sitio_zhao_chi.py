"""
Sitio Web Simulado - Zhao Chi E-Commerce
Sistema web básico para probar el monitoreo
"""

from flask import Flask, render_template, request, jsonify
import time
import random
from datetime import datetime

app = Flask(__name__)

# Simulación de base de datos de productos
PRODUCTOS = [
    {"id": 1, "nombre": "Laptop HP Pavilion", "precio": 599999, "stock": 15, "categoria": "Computadores"},
    {"id": 2, "nombre": "Mouse Logitech MX Master", "precio": 59990, "stock": 50, "categoria": "Accesorios"},
    {"id": 3, "nombre": "Teclado Mecánico Razer", "precio": 89990, "stock": 30, "categoria": "Accesorios"},
    {"id": 4, "nombre": "Monitor Samsung 27\"", "precio": 199990, "stock": 20, "categoria": "Monitores"},
    {"id": 5, "nombre": "Auriculares Sony WH-1000XM4", "precio": 249990, "stock": 25, "categoria": "Audio"},
    {"id": 6, "nombre": "Webcam Logitech C920", "precio": 79990, "stock": 40, "categoria": "Accesorios"},
    {"id": 7, "nombre": "SSD Samsung 1TB", "precio": 89990, "stock": 60, "categoria": "Almacenamiento"},
    {"id": 8, "nombre": "RAM Corsair 16GB", "precio": 59990, "stock": 45, "categoria": "Componentes"}
]

# Carrito de compras en memoria
carritos = {}

# Estadísticas de rendimiento
estadisticas = {
    "visitas": 0,
    "productos_vistos": 0,
    "agregados_al_carrito": 0,
    "compras": 0,
    "tiempo_respuesta_promedio": []
}


def simular_carga_bd():
    """Simula consulta a base de datos con latencia variable"""
    # 80% del tiempo es rápido, 20% es lento
    if random.random() < 0.8:
        time.sleep(random.uniform(0.01, 0.05))  # 10-50ms
    else:
        time.sleep(random.uniform(0.5, 1.0))  # 500-1000ms (lento)


@app.before_request
def registrar_inicio():
    """Registra el tiempo de inicio de cada petición"""
    request.start_time = time.time()


@app.after_request
def registrar_fin(response):
    """Registra el tiempo de respuesta después de cada petición"""
    if hasattr(request, 'start_time'):
        tiempo_respuesta = time.time() - request.start_time
        estadisticas["tiempo_respuesta_promedio"].append(tiempo_respuesta)
        
        # Mantener solo las últimas 100 mediciones
        if len(estadisticas["tiempo_respuesta_promedio"]) > 100:
            estadisticas["tiempo_respuesta_promedio"] = estadisticas["tiempo_respuesta_promedio"][-100:]
    
    return response


@app.route('/')
def home():
    """Página principal"""
    estadisticas["visitas"] += 1
    simular_carga_bd()  # Simula consulta a BD
    return render_template('index.html', productos=PRODUCTOS[:4])


@app.route('/productos')
def productos():
    """Catálogo completo de productos"""
    estadisticas["visitas"] += 1
    simular_carga_bd()
    
    # Simular búsqueda
    categoria = request.args.get('categoria', None)
    if categoria:
        productos_filtrados = [p for p in PRODUCTOS if p['categoria'] == categoria]
    else:
        productos_filtrados = PRODUCTOS
    
    return render_template('productos.html', productos=productos_filtrados)


@app.route('/producto/<int:producto_id>')
def detalle_producto(producto_id):
    """Detalle de un producto específico"""
    estadisticas["productos_vistos"] += 1
    simular_carga_bd()
    
    producto = next((p for p in PRODUCTOS if p['id'] == producto_id), None)
    if not producto:
        return "Producto no encontrado", 404
    
    return render_template('producto.html', producto=producto)


@app.route('/carrito', methods=['GET'])
def ver_carrito():
    """Ver carrito de compras"""
    estadisticas["visitas"] += 1
    session_id = request.cookies.get('session_id', 'default')
    carrito = carritos.get(session_id, [])
    
    total = sum(item['precio'] * item['cantidad'] for item in carrito)
    
    return render_template('carrito.html', carrito=carrito, total=total)


@app.route('/api/carrito/agregar', methods=['POST'])
def agregar_al_carrito():
    """Agregar producto al carrito"""
    estadisticas["agregados_al_carrito"] += 1
    simular_carga_bd()
    
    data = request.json
    producto_id = data.get('producto_id')
    cantidad = data.get('cantidad', 1)
    
    # Buscar producto
    producto = next((p for p in PRODUCTOS if p['id'] == producto_id), None)
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404
    
    # Agregar al carrito
    session_id = request.cookies.get('session_id', 'default')
    if session_id not in carritos:
        carritos[session_id] = []
    
    # Verificar si ya está en el carrito
    item_existente = next((item for item in carritos[session_id] if item['id'] == producto_id), None)
    if item_existente:
        item_existente['cantidad'] += cantidad
    else:
        carritos[session_id].append({
            'id': producto['id'],
            'nombre': producto['nombre'],
            'precio': producto['precio'],
            'cantidad': cantidad
        })
    
    return jsonify({
        "success": True,
        "mensaje": "Producto agregado al carrito",
        "items_en_carrito": len(carritos[session_id])
    })


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Proceso de pago"""
    if request.method == 'GET':
        estadisticas["visitas"] += 1
        session_id = request.cookies.get('session_id', 'default')
        carrito = carritos.get(session_id, [])
        total = sum(item['precio'] * item['cantidad'] for item in carrito)
        return render_template('checkout.html', carrito=carrito, total=total)
    
    # POST - Procesar pago
    estadisticas["compras"] += 1
    simular_carga_bd()
    
    # Simular procesamiento de pago (puede ser lento)
    time.sleep(random.uniform(0.5, 2.0))
    
    # Vaciar carrito
    session_id = request.cookies.get('session_id', 'default')
    if session_id in carritos:
        carritos[session_id] = []
    
    return jsonify({
        "success": True,
        "mensaje": "Compra realizada exitosamente",
        "numero_orden": f"ZC-{random.randint(10000, 99999)}"
    })


@app.route('/api/estadisticas')
def get_estadisticas():
    """Endpoint para obtener estadísticas del sistema"""
    tiempos = estadisticas["tiempo_respuesta_promedio"]
    
    if tiempos:
        promedio = sum(tiempos) / len(tiempos)
        minimo = min(tiempos)
        maximo = max(tiempos)
    else:
        promedio = minimo = maximo = 0
    
    return jsonify({
        "visitas_total": estadisticas["visitas"],
        "productos_vistos": estadisticas["productos_vistos"],
        "agregados_carrito": estadisticas["agregados_al_carrito"],
        "compras_realizadas": estadisticas["compras"],
        "rendimiento": {
            "tiempo_respuesta_promedio": f"{promedio*1000:.2f}ms",
            "tiempo_respuesta_min": f"{minimo*1000:.2f}ms",
            "tiempo_respuesta_max": f"{maximo*1000:.2f}ms"
        },
        "timestamp": datetime.now().isoformat()
    })


@app.route('/health')
def health_check():
    """Health check para monitoreo"""
    # Simular ocasionalmente un health check "unhealthy"
    if random.random() < 0.05:  # 5% de probabilidad
        return jsonify({"status": "unhealthy", "error": "Database connection slow"}), 503
    
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": "OK"
    })


@app.route('/simular-carga')
def simular_carga():
    """Endpoint para simular carga alta (para testing)"""
    # Simula una operación pesada
    duracion = float(request.args.get('duracion', 2.0))
    time.sleep(duracion)
    return jsonify({
        "mensaje": f"Operación completada después de {duracion} segundos"
    })


@app.route('/simular-error')
def simular_error():
    """Endpoint para simular errores (para testing)"""
    tipo = request.args.get('tipo', '500')
    
    if tipo == '404':
        return "Página no encontrada", 404
    elif tipo == '503':
        return "Servicio no disponible", 503
    else:
        return "Error interno del servidor", 500


if __name__ == '__main__':
    print("=" * 70)
    print("ZHAO CHI E-COMMERCE - SITIO WEB DE PRUEBA")
    print("=" * 70)
    print("\nSitio web iniciado en: http://127.0.0.1:5000")
    print("\nEndpoints disponibles:")
    print("  / - Página principal")
    print("  /productos - Catálogo")
    print("  /carrito - Ver carrito")
    print("  /checkout - Proceso de pago")
    print("  /api/estadisticas - Estadísticas del sistema")
    print("  /health - Health check")
    print("  /simular-carga - Simular carga alta")
    print("  /simular-error - Simular errores")
    print("\nPresiona Ctrl+C para detener el servidor")
    print("=" * 70)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
