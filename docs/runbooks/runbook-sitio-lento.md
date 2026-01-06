# Runbook: Sitio Web Lento

**Sistema:** Zhao Chi E-commerce  
**Actualizado:** 06/01/2026

## Descripción

Qué hacer cuando el sitio está lento (más de 5 segundos para cargar páginas).

**Síntomas:**
- Páginas demoran mucho en cargar
- Monitoreo muestra alertas de lentitud
- Usuarios se quejan

## Diagnóstico Rápido

### 1. Revisar servidor

Conectarse al servidor y ver recursos:

```bash
top
free -h
df -h
```

Si CPU > 80% o RAM > 90% hay problema.

### 2. Revisar logs

Ver si hay errores:

```bash
tail -100 /var/log/app.log | grep ERROR
```

### 3. Revisar base de datos

Conectar a MySQL y ver qué consultas están corriendo:

```sql
SHOW PROCESSLIST;
```

Si hay consultas con más de 10 segundos es problema de BD.

## Soluciones

### Si el problema es CPU alta

Reiniciar la aplicación:

```bash
sudo systemctl restart zhao-chi-web
```

Esto suele solucionar el problema temporalmente.

### Si el problema es memoria

Reiniciar aplicación:

```bash
sudo systemctl restart zhao-chi-web
```

También se puede limpiar el cache:

```bash
redis-cli FLUSHDB
```

### Si el problema es base de datos

Matar consultas lentas:

```sql
KILL [id];
```

Revisar si falta algún índice en las tablas que están lentas.

### Si el problema es API externa

Revisar si el servicio externo (pagos, envíos) está funcionando bien. A veces hay que esperar a que se recupere o contactar soporte.

## Verificar que se solucionó

Después de aplicar alguna solución revisar:

- Tiempo de carga del sitio (debe ser < 3 segundos)
- CPU y RAM del servidor (deben bajar)
- Logs sin errores nuevos

## Contactos

- Operaciones: #ops en Slack
- Desarrollo: #dev-backend en Slack

## Notas

Si el problema persiste después de reiniciar, escalar a desarrollo.

Documentar qué se hizo en el ticket correspondiente.
