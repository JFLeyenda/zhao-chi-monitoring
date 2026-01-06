# 🔧 Runbook: Sitio Web Lento

**Sistema:** Zhao Chi E-commerce  
**Última actualización:** 2026-01-06  
**Responsable:** Equipo de Operaciones

---

## 📋 Descripción del Problema

El sitio web está respondiendo lentamente, con tiempos de carga superiores a 5 segundos. Los usuarios reportan experiencia degradada.

**Síntomas:**
- Tiempo de carga de páginas > 5 segundos
- Alertas de monitoreo sintético
- Quejas de usuarios en redes sociales
- Aumento en tasa de rebote

---

## 🚨 Nivel de Severidad

**Alta** - Afecta experiencia de todos los usuarios y puede impactar ventas.

---

## 🔍 Pasos de Diagnóstico

### 1. Verificar Estado General del Sistema

```bash
# Revisar estado de servidores
ssh web-server-01
top -n 1
free -h
df -h
```

**¿Qué buscar?**
- CPU > 80%: Problema de procesamiento
- RAM > 90%: Posible memory leak
- Disco > 85%: Falta de espacio

### 2. Revisar Logs de Aplicación

```bash
# Ver últimos errores
tail -n 100 /var/log/zhao-chi/app.log | grep ERROR
tail -n 100 /var/log/zhao-chi/app.log | grep SLOW
```

**Buscar:**
- Consultas SQL lentas
- Timeouts de APIs externas
- Excepciones no manejadas

### 3. Verificar Base de Datos

```sql
-- Consultas activas
SHOW PROCESSLIST;

-- Consultas lentas recientes
SELECT * FROM mysql.slow_log ORDER BY start_time DESC LIMIT 10;
```

**Indicadores de problema:**
- Consultas corriendo > 10 segundos
- Muchas consultas en estado "Locked"
- Conexiones activas > 80% del límite

### 4. Revisar Monitoreo APM

- Abrir dashboard de APM
- Identificar funciones con tiempo > 2 segundos
- Revisar trace de la transacción más lenta

---

## 🛠️ Pasos de Resolución

### Caso 1: CPU Alta

**Causa:** Muchas peticiones concurrentes o proceso consumiendo recursos

**Solución:**
1. Identificar proceso con `top` o `htop`
2. Si es la aplicación web:
   ```bash
   # Reiniciar servicio
   sudo systemctl restart zhao-chi-web
   ```
3. Si es consulta SQL lenta:
   - Identificar query en logs
   - Agregar índice necesario
   - Optimizar consulta

### Caso 2: Memoria Llena

**Causa:** Memory leak o cache sin limpiar

**Solución:**
1. Reiniciar aplicación para liberar memoria:
   ```bash
   sudo systemctl restart zhao-chi-web
   ```
2. Limpiar cache de Redis:
   ```bash
   redis-cli FLUSHDB
   ```
3. Monitorear si vuelve a llenarse (indica memory leak)

### Caso 3: Base de Datos Lenta

**Causa:** Consultas sin optimizar, falta de índices, tabla bloqueada

**Solución:**
1. Matar consultas muy largas:
   ```sql
   KILL [process_id];
   ```
2. Revisar plan de ejecución de queries lentas:
   ```sql
   EXPLAIN SELECT * FROM productos WHERE categoria = 'electronicos';
   ```
3. Agregar índices faltantes:
   ```sql
   CREATE INDEX idx_categoria ON productos(categoria);
   ```

### Caso 4: API Externa Lenta

**Causa:** Servicio de terceros (pasarela de pago, envíos) con problemas

**Solución:**
1. Verificar status del servicio externo
2. Aumentar timeout temporalmente
3. Implementar fallback o cache
4. Contactar soporte del proveedor

---

## ✅ Verificación de Solución

Después de aplicar corrección, verificar:

1. **Monitoreo sintético:** Tiempo de carga < 3 segundos
2. **Métricas de servidor:** CPU < 70%, RAM < 80%
3. **Logs:** Sin errores nuevos en últimos 5 minutos
4. **Usuarios:** Confirmar que reportes de lentitud cesaron

---

## 📝 Post-Resolución

1. Documentar causa raíz en post-mortem
2. Crear ticket para prevención permanente
3. Actualizar alertas si fue falso positivo
4. Notificar a equipo de desarrollo si requiere fix en código

---

## 🔗 Enlaces Relacionados

- Dashboard APM: http://monitoring.zhaochi.com/apm
- Logs centralizados: http://logs.zhaochi.com
- Runbook: Alta Demanda
- Runbook: Base de Datos Caída

---

## 👥 Contactos de Escalamiento

- **Nivel 1:** Equipo de Operaciones (Slack: #ops)
- **Nivel 2:** Desarrolladores Backend (Slack: #dev-backend)
- **Nivel 3:** CTO (solo incidentes críticos)
