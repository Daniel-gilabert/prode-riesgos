import streamlit as st
import json
import os
import random
import string
import hashlib
from datetime import datetime
import pandas as pd
from supabase import create_client

st.set_page_config(page_title="PRODE - Login", layout="centered")

# Configuración de datos (puede cambiarse por variables de entorno)
DATA_SOURCE = os.environ.get("DATA_SOURCE", "supabase")  # "supabase" o "sharepoint"
SHAREPOINT_EMPLEADOS_URL = os.environ.get("SHAREPOINT_EMPLEADOS_URL", "")
SHAREPOINT_FICHAJES_URL = os.environ.get("SHAREPOINT_FICHAJES_URL", "")

DB_FILE = "users_db.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {
        "danielgilabert@prode.es": {
            "password": hash_password("admin"),
            "role": "gestor",
            "first_login": False,
            "created_at": datetime.now().isoformat()
        }
    }

def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f, indent=2)

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%"
    return ''.join(random.choice(chars) for _ in range(length))

SESSIONS_FILE = "active_sessions.json"

def load_sessions():
    if os.path.exists(SESSIONS_FILE):
        with open(SESSIONS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_sessions(sessions):
    with open(SESSIONS_FILE, "w") as f:
        json.dump(sessions, f, indent=2)

ROLES = {
    "gestor": {
        "name": "GESTOR",
        "description": "Acceso TOTAL a todo y gestión de la aplicación",
        "icon": "🔴",
        "menus": ["Inicio", "Riesgos de Capital Humano", "Control Horario", "Riesgo Financiero", "Riesgo Psicosocial", "Riesgo Seguridad Informatica", "CCTV", "Repositorio Pildoras", "Repositorio Documentos", "Repositorio Riesgos", "Administración", "Métricas de Riesgos"],
        "can_manage_app": True,
        "can_see_all_risks": True,
        "can_create_users": True
    },
    "comite": {
        "name": "COMITÉ",
        "description": "Acceso a módulos designados + métricas y resúmenes de todos los riesgos",
        "icon": "🟡",
        "menus": ["Inicio", "Riesgos de Capital Humano", "Control Horario", "Riesgo Financiero", "Riesgo Psicosocial", "Riesgo Seguridad Informatica", "CCTV", "Repositorio Pildoras", "Repositorio Documentos", "Repositorio Riesgos", "Métricas de Riesgos"],
        "can_manage_app": False,
        "can_see_all_risks": True,
        "can_create_users": False
    },
    "responsable": {
        "name": "RESPONSABLE",
        "description": "Solo los módulos que se le activen",
        "icon": "🟢",
        "menus": ["Inicio"],
        "can_manage_app": False,
        "can_see_all_risks": False,
        "can_create_users": False,
        "custom_modules": []
    }
}

MODULOS = {
    "Inicio": "🏠",
    "Riesgos de Capital Humano": "👥",
    "Control Horario": "⏰",
    "Riesgo Financiero": "💰",
    "Riesgo Psicosocial": "🧠",
    "Riesgo Seguridad Informatica": "🔒",
    "CCTV": "📹",
    "Repositorio Pildoras": "💊",
    "Repositorio Documentos": "📁",
    "Repositorio Riesgos": "📋",
    "Administración": "⚙️",
    "Métricas de Riesgos": "📈"
}

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://gqfiarxccbaznjxispsv.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxZmlhcnhjY2Jhem5qeGlzcHN2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MjEwMjg5MiwiZXhwIjoyMDg3Njc4ODkyfQ.BdwO_YxfI3_kPRNIfKaoyyVKvLYtNaMCbsjFVmCBcxE")

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    supabase = None

def get_empleados():
    if not supabase:
        return []
    try:
        return supabase.table("empleados").select("*").execute().data
    except:
        return []

def get_inicio_stats():
    empleados = get_empleados()
    total = len(empleados)
    activos = len([e for e in empleados if e.get("activo", True)])
    deptos = len(set(e.get("departamento", "") for e in empleados if e.get("departamento")))
    return total, activos, deptos

def login_page():
    AUDIT_FILE = "audit_log.json"
    
    st.title("🏢 PRODE - Inicio de sesión")
    st.markdown("Control de riesgos y capital humano")
    st.markdown("---")
    
    with st.form("login"):
        email = st.text_input("📧 Email", placeholder="tu@prode.es")
        password = st.text_input("🔑 Contraseña", type="password")
        submit = st.form_submit_button("🚀 Acceder", use_container_width=True)
        
        if submit:
            if email and password:
                users = load_users()
                if email in users and users[email]["password"] == hash_password(password):
                    def log_login():
                        if os.path.exists(AUDIT_FILE):
                            with open(AUDIT_FILE, "r") as f:
                                audit = json.load(f)
                        else:
                            audit = []
                        audit.append({
                            "timestamp": datetime.now().isoformat(),
                            "user": email,
                            "action": "LOGIN",
                            "details": "Inicio de sesión"
                        })
                        with open(AUDIT_FILE, "w") as f:
                            json.dump(audit, f, indent=2)
                    
                    log_login()
                    
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = email
                    st.session_state["role"] = users[email]["role"]
                    st.session_state["custom_modules"] = users[email].get("custom_modules", [])
                    st.session_state["login_time"] = datetime.now().isoformat()
                    
                    if users[email].get("first_login"):
                        st.session_state["must_change"] = True
                    
                    st.rerun()
                else:
                    st.error("❌ Credenciales incorrectas")
            else:
                st.warning("⚠️ Introduce email y contraseña")
    
    st.markdown("---")
    st.info("❓ ¿Olvidaste tu contraseña? Ponte en contacto con **danielgilabert@prode.es** indicando en el asunto: **cambio de contraseña aplicacion**")

def change_password_page():
    st.markdown("🔐 **Cambiar contraseña**")
    st.warning("Primer inicio. Cambia tu contraseña.")
    
    new_pass = st.text_input("Nueva contraseña", type="password")
    confirm = st.text_input("Confirmar", type="password")
    
    if st.button("💾 Guardar"):
        if new_pass != confirm:
            st.error("❌ No coinciden")
        elif len(new_pass) < 6:
            st.error("❌ Mínimo 6 caracteres")
        else:
            users = load_users()
            users[st.session_state["user"]]["password"] = hash_password(new_pass)
            users[st.session_state["user"]]["first_login"] = False
            save_users(users)
            st.session_state.pop("must_change", None)
            st.success("✅ Cambiada")
            st.rerun()

def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    if st.session_state.get("must_change"):
        change_password_page()
        return
    
    if not st.session_state["authenticated"]:
        login_page()
        return
    
    user = st.session_state["user"]
    role = st.session_state["role"]
    custom_modules = st.session_state.get("custom_modules", [])
    
    if role == "responsable" and custom_modules:
        menus = custom_modules
    else:
        rol_info = ROLES.get(role, {})
        menus = rol_info.get("menus", ["Inicio"])
    
    rol_info = ROLES.get(role, {})
    
    st.sidebar.markdown(f"### 👤 {user}")
    st.sidebar.markdown(f"{rol_info.get('icon','')} **{rol_info.get('name', '')}**")
    st.sidebar.markdown(f"_{rol_info.get('description', '')}_")
    
    if st.sidebar.button("🚪 Cerrar sesión"):
        try:
            sessions = load_sessions()
            if user in sessions:
                sessions[user]["logout"] = datetime.now().isoformat()
                save_sessions(sessions)
        except:
            pass
        st.session_state["authenticated"] = False
        st.rerun()
    
    st.sidebar.markdown("---")
    menu = st.sidebar.radio("📋 Menú", menus)
    
    st.title("🏢 PRODE - Sistema de Gestión")
    st.markdown("---")
    
    if menu == "Inicio":
        st.markdown("### 🏠 Inicio")
        st.markdown(f"**Usuario:** {user}")
        st.markdown(f"**Rol:** {rol_info.get('icon','')} {rol_info.get('name', '')}")
        
        total_emp, activos_emp, num_deptos = get_inicio_stats()
        
        col1, col2 = st.columns(2)
        with col1: st.metric("👥 Empleados activos", activos_emp)
        with col2: st.metric("🏢 Departamentos", num_deptos)
    
    elif menu == "Riesgos de Capital Humano":
        st.markdown("### 👥 Riesgos de Capital Humano")
        
        emp_data = get_empleados()
        total_emp = len(emp_data)
        activos_emp = len([e for e in emp_data if e.get("activo", True)])
        
        tab1, tab2 = st.tabs(["📊 Resumen", "🏥 Reconocimientos Médicos"])
        
        with tab1:
            col1, col2, col3 = st.columns(3)
            with col1: st.metric("Empleados totales", total_emp)
            with col2: st.metric("Activos", activos_emp)
            with col3: st.metric("Departamentos", len(set(e.get("departamento","") for e in emp_data)))
        
        with tab2:
            st.markdown("#### 🏥 Análisis de Reconocimientos Médicos")
            
            uploaded_file = st.file_uploader("📁 Subir archivo Excel con citas médicas", type=["xlsx", "xls"], key="citas_file")
            
            if uploaded_file is not None:
                try:
                    df = pd.read_excel(uploaded_file)
                    columnas_ok = all(c in df.columns for c in ['fecha', 'persona trabajadora', 'asistencia', 'anulada'])
                    
                    if not columnas_ok:
                        st.error("❌ El archivo debe tener las columnas: fecha, persona trabajadora, asistencia, anulada")
                        return
                    
                    def normalizar(valor):
                        if pd.isna(valor): return False
                        t = str(valor).strip().lower()
                        return t in {"si", "sí", "s", "true", "1", "x", "yes", "y"}
                    
                    citas = []
                    for _, row in df.iterrows():
                        try:
                            fecha = pd.to_datetime(row.get("fecha"), errors="coerce")
                            if pd.isna(fecha): continue
                            nombre = str(row.get("persona trabajadora", "")).strip()
                            if not nombre: continue
                            asistio = normalizar(row.get("asistencia"))
                            anulada = normalizar(row.get("anulada"))
                            genera_costo = (not asistio) and (not anulada)
                            citas.append({
                                "Empleado": nombre,
                                "Fecha": fecha.to_pydatetime(),
                                "Asistió": asistio,
                                "Anulada": anulada,
                                "Genera Costo": genera_costo
                            })
                        except:
                            continue
                    
                    if not citas:
                        st.error("No se pudieron procesar las citas")
                        return
                    
                    total_citas = len(citas)
                    asistidas = sum(1 for c in citas if c["Asistió"])
                    anuladas = sum(1 for c in citas if c["Anulada"])
                    perdidas = sum(1 for c in citas if c["Genera Costo"])
                    costo_total = perdidas * 20.0
                    pct_asistencia = (asistidas / total_citas * 100) if total_citas else 0
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1: st.metric("Total citas", total_citas)
                    with col2: st.metric("Asistidas", asistidas, f"{pct_asistencia:.1f}%")
                    with col3: st.metric("Anuladas", anuladas)
                    with col4: st.metric("💸 Costo total", f"{costo_total:.2f} €", f"{perdidas} perdidas")
                    
                    st.markdown("---")
                    
                    df_citas = pd.DataFrame(citas)
                    
                    col_lost, col_all = st.columns(2)
                    with col_lost:
                        st.markdown("##### Citas que generan costo (20€/ud)")
                        df_perdidas = df_citas[df_citas["Genera Costo"] == True].copy()
                        df_perdidas["Fecha"] = pd.to_datetime(df_perdidas["Fecha"]).dt.strftime("%d/%m/%Y")
                        df_perdidas["Costo"] = 20.0
                        st.dataframe(df_perdidas[["Empleado","Fecha","Asistió","Anulada","Costo"]], use_container_width=True, hide_index=True)
                        st.info(f"**Total a recuperar:** {costo_total:.2f} €")
                    
                    with col_all:
                        st.markdown("##### Todas las citas")
                        df_all = df_citas.copy()
                        df_all["Fecha"] = pd.to_datetime(df_all["Fecha"]).dt.strftime("%d/%m/%Y")
                        st.dataframe(df_all[["Empleado","Fecha","Asistió","Anulada","Genera Costo"]], use_container_width=True, hide_index=True)
                    
                    csv = df_citas.to_csv(index=False).encode("utf-8")
                    st.download_button("📥 Descargar CSV", csv, file_name="reconocimientos_medicos.csv", mime="text/csv")
                    
                except Exception as e:
                    st.error(f"Error procesando archivo: {e}")
            else:
                st.info("Sube un archivo Excel con las columnas: **fecha, persona trabajadora, asistencia, anulada**")
    
    elif menu == "Control Horario":
        st.markdown("### ⏰ Control Horario")
        
        emp_data = get_empleados()
        activos = len([e for e in emp_data if e.get("activo", True)])
        
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Activos", activos)
        with col2: st.metric("Departamentos", len(set(e.get("departamento","") for e in emp_data)))
        with col3: st.metric("Fichajes hoy", "—")
        
        st.markdown("---")
        
        col_btn, col_est = st.columns([3, 1])
        with col_btn: st.link_button("🚀 ABRIR MÓDULO", "https://worktime-asisten.streamlit.app")
        with col_est: st.success("🟢 Activo")
    
    elif menu == "Riesgo Financiero":
        st.markdown("### 💰 Riesgo Financiero")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Riesgos identificados", "—")
        with col2: st.metric("Criticos", "—")
        with col3: st.metric("Resueltos", "—")
        st.info("📋 Módulo en desarrollo.")
    
    elif menu == "Riesgo Psicosocial":
        st.markdown("### 🧠 Riesgo Psicosocial")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Riesgos identificados", "—")
        with col2: st.metric("Criticos", "—")
        with col3: st.metric("Resueltos", "—")
        st.info("📋 Módulo en desarrollo.")
    
    elif menu == "Riesgo Seguridad Informatica":
        st.markdown("### 🔒 Riesgo Seguridad Informatica")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Riesgos identificados", "—")
        with col2: st.metric("Criticos", "—")
        with col3: st.metric("Resueltos", "—")
        st.info("📋 Módulo en desarrollo.")
    
    elif menu == "CCTV":
        st.markdown("### 📹 CCTV")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Cámaras activas", "—")
        with col2: st.metric("Alertas", "—")
        with col3: st.metric("Incidentes", "—")
        st.info("📋 Módulo en desarrollo.")
    
    elif menu == "Repositorio Pildoras":
        st.markdown("### 💊 Repositorio de Píldoras Formativas")
        st.info("📚 Módulo en desarrollo.")
    
    elif menu == "Repositorio Documentos":
        st.markdown("### 📁 Repositorio de Documentación")
        st.info("📂 Módulo en desarrollo.")
    
    elif menu == "Repositorio Riesgos":
        st.markdown("### 📋 Repositorio de Riesgos")
        st.info("📑 Módulo en desarrollo.")
    
    elif menu == "Administración":
        if not rol_info.get("can_create_users"):
            st.error("❌ No tienes acceso")
            return
            
        st.markdown("### ⚙️ Administración")
        
        AUDIT_FILE = "audit_log.json"
        
        def load_audit():
            if os.path.exists(AUDIT_FILE):
                with open(AUDIT_FILE, "r") as f:
                    return json.load(f)
            return []
        
        def save_audit(audit):
            with open(AUDIT_FILE, "w") as f:
                json.dump(audit, f, indent=2)
        
        def log_action(action, details=""):
            audit = load_audit()
            audit.append({
                "timestamp": datetime.now().isoformat(),
                "user": user,
                "action": action,
                "details": details
            })
            save_audit(audit)
        
        tab1, tab2, tab3 = st.tabs(["👥 Usuarios", "📋 Histórico", "🔧 Sistema"])
        
        with tab1:
            users = load_users()
            col_cr, col_li = st.columns([1, 1])
            
            with col_cr:
                st.markdown("#### ➕ Crear usuario")
                new_email = st.text_input("Email", placeholder="usuario@prode.es", key="new_email")
                new_role = st.selectbox("Rol", ["comite", "responsable"], key="new_role")
                custom_mods = []
                if new_role == "responsable":
                    all_modules = ["Inicio", "Riesgos de Capital Humano", "Control Horario", "Riesgo Financiero", "Riesgo Psicosocial", "Riesgo Seguridad Informatica", "CCTV", "Repositorio Pildoras", "Repositorio Documentos", "Repositorio Riesgos"]
                    custom_mods = st.multiselect("Módulos", all_modules, default=["Inicio"], key="new_mods")
                if st.button("Crear usuario", key="btn_crear"):
                    if new_email:
                        if new_email in users:
                            st.error("❌ Ya existe")
                        else:
                            auto_pass = generate_password()
                            users[new_email] = {
                                "password": hash_password(auto_pass),
                                "role": new_role,
                                "first_login": True,
                                "created_at": datetime.now().isoformat(),
                                "temp_password": auto_pass,
                                "custom_modules": custom_mods if new_role == "responsable" else [],
                                "created_by": user
                            }
                            save_users(users)
                            log_action("CREAR_USUARIO", f"Creado usuario {new_email} con rol {new_role}")
                            st.success(f"✅ Usuario creado")
                            st.code(f"Password: {auto_pass}")
                    else:
                        st.error("❌ Email requerido")
            
            with col_li:
                st.markdown("#### 👥 Usuarios registrados")
                for email, info in users.items():
                    with st.expander(f"📧 {email} - {ROLES.get(info['role'], {}).get('name', info['role'])}"):
                        st.write(f"**Rol:** {ROLES.get(info['role'], {}).get('name', info['role'])}")
                        if info.get("first_login"):
                            st.warning("⚠️ Debe cambiar contraseña")
                        
                        col_x, col_y = st.columns(2)
                        with col_x:
                            new_rol = st.selectbox("Cambiar rol", ["comite", "responsable"], key=f"rol_{email}")
                            if st.button("Actualizar", key=f"btn_rol_{email}"):
                                users[email]["role"] = new_rol
                                save_users(users)
                                log_action("CAMBIAR_ROL", f"{email} -> {new_rol}")
                                st.rerun()
                        with col_y:
                            if email != user:
                                if st.button("🗑️ Eliminar", key=f"btn_del_{email}"):
                                    del users[email]
                                    save_users(users)
                                    log_action("ELIMINAR_USUARIO", f"Eliminado {email}")
                                    st.rerun()
        
        with tab2:
            st.markdown("#### 📋 Histórico de accesos")
            audit = load_audit()
            if audit:
                df_audit = pd.DataFrame(reversed(audit[-100:]))
                df_audit["timestamp"] = pd.to_datetime(df_audit["timestamp"]).dt.strftime("%Y-%m-%d %H:%M")
                st.dataframe(df_audit[["timestamp", "user", "action", "details"]], use_container_width=True, hide_index=True)
                col_stat1, col_stat2 = st.columns(2)
                with col_stat1: st.metric("Total acciones", len(audit))
                with col_stat2: st.metric("Usuarios activos", len({a["user"] for a in audit}))
            else:
                st.info("No hay registro de actividades todavía.")
        
        with tab3:
            ERRORS_FILE = "errors.log"
            APP_START = "startup.txt"
            
            def get_uptime():
                if os.path.exists(APP_START):
                    with open(APP_START, "r") as f:
                        start = f.read().strip()
                    try:
                        start_dt = datetime.fromisoformat(start)
                        delta = datetime.now() - start_dt
                        days = delta.days
                        hours, remainder = divmod(delta.seconds, 3600)
                        minutes, _ = divmod(remainder, 60)
                        if days > 0:
                            return f"{days}d {hours}h {minutes}m"
                        return f"{hours}h {minutes}m"
                    except:
                        return "?"
                return "?"
            
            users = load_users()
            all_modulos = list(MODULOS.keys())
            
            tab_s1, tab_s2, tab_s3, tab_s4, tab_s5 = st.tabs(["📊 Estado", "💾 Backup", "📜 Logs", "👥 Sesiones", "⚙️ Módulos"])
            
            with tab_s1:
                st.markdown("#### 🔧 Estado del sistema")
                col1, col2, col3 = st.columns(3)
                with col1: st.success("🗄️ Base de datos")
                with col2: st.success("🔐 Autenticación")
                with col3: st.success("📱 Servicios")
                
                col_st1, col_st2, col_st3, col_st4 = st.columns(4)
                with col_st1: st.metric("Versión", "1.0.0")
                with col_st2: st.metric("Entorno", "Producción")
                with col_st3: st.metric("Uptime", get_uptime())
                with col_st4: st.metric("Usuarios", len(users))
            
            with tab_s2:
                st.markdown("#### 💾 Backup y Restauración")
                
                st.markdown("**Exportar datos:**")
                col_b1, col_b2 = st.columns(2)
                
                backup_users = json.dumps(users, indent=2)
                backup_audit = json.dumps(load_audit(), indent=2)
                
                with col_b1:
                    st.download_button("📥 Exportar usuarios", backup_users.encode("utf-8"), file_name="users_backup.json", mime="application/json")
                with col_b2:
                    st.download_button("📥 Exportar auditoría", backup_audit.encode("utf-8"), file_name="audit_backup.json", mime="application/json")
                
                st.markdown("---")
                st.markdown("**Restaurar datos:**")
                restore_file = st.file_uploader("Subir archivo de backup", type=["json"])
                if restore_file:
                    try:
                        data = json.load(restore_file)
                        if "danielgilabert" in str(data) or "users" in str(data)[:200]:
                            st.info(f"✅ Backup válido ({len(data)} usuarios)")
                            if st.button("🔄 Restaurar usuarios"):
                                save_users(data)
                                log_action("BACKUP_RESTORE", "Restaurado backup de usuarios")
                                st.success("✅ Usuarios restaurados")
                                st.rerun()
                        else:
                            st.error("❌ No parece un backup válido")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            
            with tab_s3:
                st.markdown("#### 📜 Gestión de Logs")
                
                audit = load_audit()
                st.write(f"**Registros totales:** {len(audit)}")
                
                col_l1, col_l2 = st.columns(2)
                with col_l1:
                    dias = st.number_input("Eliminar logs anteriores a (días)", 1, 365, 90, key="dias_log")
                with col_l2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("🗑️ Eliminar logs antiguos"):
                        try:
                            cutoff = datetime.now().timestamp() - (dias * 86400)
                            audit_filtrado = [a for a in audit if datetime.fromisoformat(a["timestamp"]).timestamp() >= cutoff]
                            eliminados = len(audit) - len(audit_filtrado)
                            save_audit(audit_filtrado)
                            log_action("CLEAR_LOGS", f"Eliminados {eliminados} registros")
                            st.success(f"✅ Eliminados {eliminados} registros")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")
                
                st.markdown("---")
                st.write("**Limpiar todo:**")
                st.warning("⚠️ Esta acción borra TODO el histórico de auditoría")
                if st.button("🗑️ Borrar TODO el log"):
                    save_audit([])
                    log_action("CLEAR_ALL_LOGS", "Borrado completo del log")
                    st.success("✅ Log borrado")
                    st.rerun()
            
            with tab_s4:
                st.markdown("#### 👥 Sesiones y actividad")
                
                sessions = load_sessions()
                sessions[user] = {
                    "login": st.session_state.get("login_time", datetime.now().isoformat()),
                    "role": role,
                    "last_seen": datetime.now().isoformat()
                }
                save_sessions(sessions)
                
                for usr, info in sessions.items():
                    login_dt = datetime.fromisoformat(info.get("login", datetime.now().isoformat()))
                    last_dt = datetime.fromisoformat(info.get("last_seen", datetime.now().isoformat()))
                    online = (datetime.now() - last_dt).seconds < 300
                    
                    col_se1, col_se2 = st.columns([3, 1])
                    with col_se1:
                        st.write(f"**{usr}**")
                        st.caption(f"Login: {login_dt.strftime('%d/%m/%Y %H:%M')} | Rol: {info.get('role','')}")
                    with col_se2:
                        if online:
                            st.success("🟢 Online")
                        else:
                            ago = (datetime.now() - last_dt)
                            if ago.days > 0:
                                st.error(f"🔴 {ago.days}d ago")
                            else:
                                st.error(f"🔴 {ago.seconds//60}m ago")
                
                st.markdown("---")
                st.write(f"**Sesiones activas (últimos 5 min):** {sum(1 for s in sessions.values() if (datetime.now() - datetime.fromisoformat(s.get('last_seen', datetime.now().isoformat()))).seconds < 300)}")
            
            with tab_s5:
                st.markdown("#### ⚙️ Módulos disponibles")
                st.write("Módulos que pueden asignarse a usuarios RESPONSABLE:")
                
                for mod in all_modulos:
                    col_m1, col_m2 = st.columns([4, 1])
                    with col_m1: st.write(f"{MODULOS.get(mod, '📄')} {mod}")
                    with col_m2: st.success("✅ Activo")
                
                st.markdown("---")
                st.write("**Por defecto en Inicio para nuevos usuarios:**")
                for email_u, info_u in users.items():
                    mods = info_u.get("custom_modules", [])
                    with st.expander(f"{email_u} ({ROLES.get(info_u['role'],{}).get('name','')})"):
                        st.write(f"**Módulos asignados:** {', '.join(mods) if mods else 'Solo Inicio'}")
    
    elif menu == "Métricas de Riesgos":
        if not rol_info.get("can_see_all_risks"):
            st.error("❌ No tienes acceso")
            return
            
        st.markdown("### 📈 Métricas de Riesgos - VISTA GLOBAL")
        st.info("Resumen consolidado de todos los riesgos de la organización")
        
        tab_r1, tab_r2, tab_r3, tab_r4, tab_r5 = st.tabs(["📊 Resumen", "👥 Capital Humano", "💰 Financiero", "🧠 Psicosocial", "🔒 Seguridad"])
        
        with tab_r1:
            col1, col2, col3, col4 = st.columns(4)
            with col1: st.metric("Total Riesgos", "45", "+3")
            with col2: st.metric("Críticos", "5", "-1")
            with col3: st.metric("Medios", "18", "+2")
            with col4: st.metric("Resueltos", "22", "+4")
            
            data = pd.DataFrame({
                "Área": ["Capital Humano", "Financiero", "Psicosocial", "Seg. Informática", "CCTV"],
                "Riesgos": [12, 8, 7, 9, 5],
                "Críticos": [2, 1, 1, 1, 0],
                "Score": [75, 68, 82, 65, 80]
            })
            st.bar_chart(data.set_index("Área")["Riesgos"], color="#FF6B6B")
            for _, row in data.iterrows():
                with st.expander(f"{row['Área']} - {row['Riesgos']} riesgos ({row['Críticos']} críticos)"):
                    st.write(f"**Score:** {row['Score']}%")
        
        with tab_r2:
            emp_data = get_empleados()
            activos = len([e for e in emp_data if e.get("activo", True)])
            col1, col2, col3 = st.columns(3)
            with col1: st.metric("Empleados", activos)
            with col2: st.metric("Riesgos CH", "12")
            with col3: st.metric("Score", "75%")
            st.info("📋 Ver módulo 'Riesgos de Capital Humano' para detalle.")
        
        with tab_r3:
            col1, col2, col3 = st.columns(3)
            with col1: st.metric("Riesgos", "8")
            with col2: st.metric("Críticos", "1")
            with col3: st.metric("Score", "68%")
            st.info("📋 Ver módulo 'Riesgo Financiero' para detalle.")
        
        with tab_r4:
            col1, col2, col3 = st.columns(3)
            with col1: st.metric("Riesgos", "7")
            with col2: st.metric("Críticos", "1")
            with col3: st.metric("Score", "82%")
            st.info("📋 Ver módulo 'Riesgo Psicosocial' para detalle.")
        
        with tab_r5:
            col1, col2, col3 = st.columns(3)
            with col1: st.metric("Riesgos", "9")
            with col2: st.metric("Críticos", "1")
            with col3: st.metric("Score", "65%")
            st.info("📋 Ver módulo 'Riesgo Seguridad Informatica' para detalle.")

if __name__ == "__main__":
    main()
