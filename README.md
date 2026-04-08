# PRODE Riesgos - Sistema de Gestión de Riesgos

## 📋 Descripción
App Streamlit para gestionar los riesgos de la organización PRODE.

## 🚀 Desplegar

1. Ir a: https://share.streamlit.io
2. Conectar con GitHub
3. Seleccionar este repositorio
4. Deploy

## 📁 Estructura

```
├── app.py              # Aplicación principal
├── requirements.txt    # Dependencias
├── .env.example       # Variables de ejemplo
└── README.md          # Este archivo
```

## ⚙️ Configuración

### Opción 1: Supabase (ya configurado)
- Empleados se leen de Supabase

### Opción 2: SharePoint/OneDrive (pendiente)
- Crear carpeta compartida `PRODE_Riesgos`
- Exportar empleados y fichajes desde BC a Excel
- Configurar variables de entorno

## 🔐 Credenciales

- **Usuario admin:** danielgilabert@prode.es
- **Contraseña:** admin

## 👥 Roles

- **GESTOR** — Acceso total + administración
- **COMITÉ** — Ver todos los módulos y métricas
- **RESPONSABLE** — Solo módulos asignados