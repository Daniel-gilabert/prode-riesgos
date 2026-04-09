# PRODE Riesgos - Guía Técnica Completa

## 📋 Resumen

**PRODE Riesgos** es una aplicación web Streamlit para gestionar los riesgos organizacionales de la Fundación PRODE. Permite control de empleados, reconocimientos médicos, métricas de riesgos y administración de usuarios.

---

## 🛠️ Tecnología

| Componente | Tecnología |
|------------|------------|
| Frontend | Streamlit (Python) |
| Base de datos | Supabase (PostgreSQL) |
| Hospedaje | Streamlit Cloud |
| Control de versiones | GitHub |
| Autenticación | Propia (usuarios_db.json) |

---

## 📁 Estructura del Proyecto

```
prode-riesgos-deploy/
├── app.py               # Aplicación principal (720 líneas)
├── requirements.txt     # Dependencias Python
├── .env.example         # Variables de entorno de ejemplo
├── .gitignore           # Archivos a ignorar en Git
└── README.md            # Instrucciones básicas
```

---

## 🔐 Autenticación y Roles

### Usuarios
Los usuarios se guardan en `users_db.json` (archivo local, no en la nube por seguridad).

**Usuario por defecto:**
- Email: `danielgilabert@prode.es`
- Contraseña: `admin`

### Roles definidos

| Rol | Descripción | Permisos |
|-----|-------------|----------|
| **GESTOR** | Administrador total | Todos los módulos + administración + gestión de usuarios |
| **COMITÉ** | Acceso completo sin administración | Todos los módulos + métricas globales |
| **RESPONSABLE** | Solo módulos asignados | Los que se le asignen manualmente |

### Gestión de usuarios
- Crear usuario → genera password automática
- Reset de contraseña → requiere contacto con admin (no hay email automático)
- Cambiar rol → en tiempo real
- Asignar módulos → solo para RESPONSABLE

### Auditoría
Todas las acciones se registran en `audit_log.json`:
- LOGIN
- CREAR_USUARIO
- CAMBIAR_ROL
- ACTUALIZAR_MODULOS
- REGENERAR_PASSWORD
- ELIMINAR_USUARIO
- BACKUP_RESTORE
- CLEAR_LOGS

---

## 📊 Módulos de la App

### 1. Inicio
- Muestra empleados activos (lee de Supabase)
- Muestra departamentos

### 2. Riesgos de Capital Humano
**Pestaña Resumen:**
- Total empleados
- Empleados activos
- Departamentos

**Pestaña Reconocimientos Médicos:**
- Subir Excel con columnas: `fecha`, `persona trabajadora`, `asistencia`, `anulada`
- Calcula costo: 20€ por cada cita perdida (no asistida y no anulada)
- Muestra desglose por empleado y departamento
- Exportar a CSV

### 3. Control Horario
- Link externo a app WorkTime: `https://worktime-asisten.streamlit.app`
- Muestra empleados activos desde Supabase

### 4-8. Módulos en desarrollo
- Riesgo Financiero
- Riesgo Psicosocial
- Riesgo Seguridad Informatica
- CCTV
- Repositorio Pildoras
- Repositorio Documentos
- Repositorio Riesgos

(Mostrar "en desarrollo" hasta que se conecten datos reales)

### 9. Métricas de Riesgos
- Resumen global de todos los riesgos
- Pestañas por categoría: Capital Humano, Financiero, Psicosocial, Seguridad
- Gráficos y métricas

### 10. Administración (solo GESTOR)

**Pestaña Usuarios:**
- Crear usuario con rol y módulos
- Ver usuarios registrados
- Cambiar rol
- Eliminar usuario

**Pestaña Histórico:**
- Tabla de acciones (audit log)
- Estadísticas de uso

**Pestaña Sistema:**
- Estado de servicios
- Versión, uptime, usuarios
- Backup: exportar/importar usuarios y auditoría
- Gestión de logs (filtrar por días, borrar)
- Sesiones activas (quién está conectado)
- Módulos disponibles

---

## 🔗 Conexiones de Datos

### Supabase (actual)
- URL: `https://gqfiarxccbaznjxispsv.supabase.co`
- Tabla `empleados`: id, nombre, email, departamento, jornada_semanal, activo, etc.

### SharePoint (pendiente)
- Planeado para leer empleados y fichajes desde Excel
- Necesita: carpeta compartida + exportar desde Business Central

### Business Central (futuro)
- API REST posible pero requiere credenciales de Azure
- Alternativa: Exportar Excel daily a SharePoint

---

## 🚀 Cómo Desplegar

### Requisitos previos
- Cuenta GitHub
- Cuenta Streamlit Cloud (gratis)

### Pasos

1. **Subir código a GitHub**
   ```
   git add .
   git commit -m "mensaje"
   git push origin main
   ```

2. **Deploy en Streamlit Cloud**
   - Ir a: https://share.streamlit.io
   - New App
   - Seleccionar repo: `Daniel-gilabert/prode-riesgos`
   - Branch: `main`
   - Main file: `app.py`
   - Deploy

3. **URL resultante**
   - Ejemplo: `https://gestion-riesgos.streamlit.app`

---

## 🔧 Mantenimiento

### Actualizar la app
1. Editar `app.py` en local
2. Subir a GitHub
3. Streamlit Cloud detecta cambios automáticamente

### Backup de usuarios
- Ir a Administración → Sistema → Backup
- Descargar `users_backup.json`

### Restaurar usuarios
- Administración → Sistema → Backup
- Subir archivo JSON → click "Restaurar"

### Ver logs de errores
- Ir a Administración → Sistema → Estado
- Sección "Últimos errores"

---

## 📝 Formato de Archivos

### Excel Reconocimientos Médicos
Columnas obligatorias:
| Columna | Ejemplo |
|---------|---------|
| fecha | 15/03/2024 |
| persona которая trabaja | Juan García |
| asistencia | Sí / No |
| anulada | Sí / No |

---

## ⚠️ Notas Importantes

1. **Seguridad**: El archivo `users_db.json` se guarda en el servidor de Streamlit Cloud. No subir a GitHub (está en .gitignore).

2. **Límites**: Streamlit Cloud tiene límites gratuitos (ciertas horas/mes). Para uso intensivo, considerar versión de pago.

3. **Sesiones**: Las sesiones se guardan en `active_sessions.json` pero se pierden al reiniciar la app en la nube.

4. **Email**: No hay sistema de email real. El "envío de contraseña" solo muestra la password en pantalla.

---

## 📞 Soporte

Para dudas técnicas:
- Revisar este documento
- Consultar código en `app.py`
- Contactar al desarrollador original

---

*Documento generado el 09/04/2026*
