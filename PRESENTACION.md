# 🎓 Guía de Presentación - Primer Día de Clase

## 📋 Checklist Pre-Clase

### Antes del Martes

- [ ] Tener PostgreSQL instalado y corriendo
- [ ] Clonar/descargar el proyecto
- [ ] Ejecutar `./setup.sh` o seguir pasos manuales
- [ ] Verificar que el servidor local funcione
- [ ] Hacer deploy en Railway/Render (opcional pero recomendado)
- [ ] Preparar cuentas de demo

### Materiales para Mostrar

- [ ] Laptop con proyecto corriendo
- [ ] Proyector/pantalla para mostrar el código
- [ ] URL del proyecto deployado (si aplica)
- [ ] Programa del seminario impreso

## 🎯 Estructura de la Presentación (30-45 minutos)

### 1. Introducción (5 min)

**Mensaje clave:** "En este seminario van a construir aplicaciones completas como esta"

**Puntos a cubrir:**
- Presentación del equipo docente
- Objetivos del seminario
- Proyecto final: MVP presentado ante panel de profesionales

**Demo rápida:**
- Abrir el dashboard deployado
- Mostrar que los datos son reales del BCRA
- "Esto lo van a poder hacer ustedes en 13 semanas"

### 2. Demostración del Stack Completo (20 min)

#### A. Frontend - Lo que ve el usuario (5 min)

**Mostrar:**
1. Dashboard con cards de indicadores
2. Gráficos interactivos (hover sobre Chart.js)
3. Tabla de datos
4. Responsive design (achicar ventana del navegador)

**Explicar:**
- HTML estructura el contenido
- CSS (Bootstrap) lo hace ver bien
- JavaScript lo hace interactivo

**Código a mostrar:**
```html
<!-- Mostrar una card simple en index.html -->
<div class="card indicator-card">
    <div class="card-body text-center">
        <div class="indicator-value">$1,234.56</div>
        <div class="indicator-label">Tipo de Cambio</div>
    </div>
</div>
```

#### B. Backend - La API (8 min)

**Mostrar:**
1. Ir a `/docs` - Swagger UI automático
2. Expandir endpoint `/api/dashboard`
3. Hacer "Try it out" → Execute
4. Mostrar el JSON de respuesta

**Explicar:**
- FastAPI genera esta documentación automáticamente
- Cada endpoint es una "ventanilla" que entrega datos
- El frontend consume estos endpoints

**Código a mostrar:**
```python
# Mostrar endpoint simple en app/main.py
@app.get("/api/datos/ultimos-valores")
def obtener_ultimos_valores(db: Session = Depends(get_db)):
    """
    Obtener el último valor disponible de cada variable
    """
    variables = db.query(Variable).all()
    # ... resto del código
    return ultimos_valores
```

#### C. Base de Datos (4 min)

**Mostrar:**
- Abrir DBeaver/pgAdmin
- Mostrar tablas: `variables`, `datos_bcra`, `usuarios`
- Hacer un SELECT simple: `SELECT * FROM variables;`
- Mostrar relación: `datos_bcra` tiene `variable_id` que apunta a `variables`

**Explicar:**
- Los datos persisten aquí
- SQLAlchemy (ORM) traduce Python a SQL
- Diseño normalizado: cada dato una sola vez

#### D. Consumo de API Externa (3 min)

**Mostrar:**
```python
# En bcra_client.py
def get_tipo_cambio(self, desde=None, hasta=None):
    """Obtiene datos del Tipo de Cambio USD"""
    return self.get_datos_variable(
        self.VARIABLES['tipo_cambio_oficial'], 
        desde, 
        hasta
    )
```

**Ejecutar en terminal:**
```bash
python app/bcra_client.py
```

**Explicar:**
- Consumimos la API oficial del BCRA
- Guardamos los datos en nuestra BD
- Exponemos los datos en nuestra propia API

### 3. El Flujo Completo de Datos (8 min)

**Dibujar en pizarra:**

```
API BCRA → Cliente Python → PostgreSQL → FastAPI → Frontend (Browser)
           (requests)      (SQLAlchemy)  (endpoints) (fetch + Chart.js)
```

**Contar la historia:**

1. **"Cada día, nuestro script se despierta..."**
   - Ejecuta `python -m app.populate_db`
   - Llama a la API del BCRA
   - Guarda datos frescos en PostgreSQL

2. **"Un usuario abre el dashboard..."**
   - Browser carga `index.html`
   - JavaScript hace `fetch('/api/dashboard')`
   - FastAPI consulta PostgreSQL con SQLAlchemy
   - Devuelve JSON
   - JavaScript renderiza con Chart.js

3. **"El usuario se loguea..."**
   - Ingresa email/password
   - FastAPI verifica en BD
   - Genera JWT token
   - Frontend guarda token
   - Futuras requests incluyen token

**Demo en vivo:**
1. Abrir DevTools (F12)
2. Ir a Network tab
3. Refrescar página
4. Mostrar request a `/api/dashboard`
5. Mostrar el JSON que llega
6. "Este JSON se transforma en los gráficos que ven"

### 4. Patrones de Diseño Aplicados (5 min)

**Explicar brevemente (serán clases completas más adelante):**

**Repository Pattern:**
```python
# En lugar de SQL directo por todos lados...
# Tenemos un único lugar que sabe cómo obtener datos

class VariableRepository:
    def obtener_todas(self):
        return self.session.query(Variable).all()
    
    def obtener_por_nombre(self, nombre):
        return self.session.query(Variable).filter(
            Variable.nombre == nombre
        ).first()
```

**DTO Pattern (Pydantic):**
```python
# Los datos viajan en "contenedores" validados
class UsuarioCreate(BaseModel):
    email: EmailStr
    nombre: str
    password: str = Field(..., min_length=6)

# FastAPI valida automáticamente
```

### 5. Tecnologías que van a Aprender (3 min)

**Mostrar el `requirements.txt` y explicar:**

- `fastapi` - Framework web moderno y rápido
- `sqlalchemy` - ORM para bases de datos
- `pydantic` - Validación de datos
- `python-jose` - Autenticación JWT
- `requests` - Consumo de APIs
- `uvicorn` - Servidor ASGI

**En el frontend:**
- HTML5 semántico
- Bootstrap 5 - componentes listos
- Chart.js - gráficos interactivos
- Vanilla JavaScript (luego frameworks)

### 6. Deployment (2 min)

**Si está deployado, mostrar:**
- URL pública funcionando
- "Esto está en un servidor real, accesible desde cualquier lugar"
- Mencionar Railway/Render como opciones gratuitas

**Explicar proceso:**
1. Push código a GitHub
2. Conectar Railway/Render
3. Configurar variables de entorno
4. Deploy automático
5. "En producción en minutos"

### 7. Roadmap del Curso (2 min)

**Mostrar programa y conectar con el MVP:**

- **Semanas 1-2:** Python + Patrones → "Ya vieron cómo los usamos aquí"
- **Semanas 3-4:** BD + APIs → "Este dashboard no existiría sin esto"
- **Semanas 5-6:** FastAPI → "El corazón del backend"
- **Semanas 7-9:** Frontend → "Lo que hace que se vea así"
- **Semanas 10-11:** Deploy + Scraping → "Publicar y obtener más datos"
- **Semana 12-13:** MVP propio + Panel profesional

### 8. Cierre y Motivación (2 min)

**Mensaje final:**

"Este proyecto integra TODO lo que van a aprender:
- ✅ Patrones de diseño profesionales
- ✅ Base de datos relacional
- ✅ API REST completa
- ✅ Autenticación segura
- ✅ Frontend moderno
- ✅ Deploy en producción
- ✅ Consumo de datos reales

Al final del seminario, van a presentar su propio MVP ante un panel de:
- Project Managers
- Especialistas de LinkedIn
- Profesionales de la industria

No solo van a aprender a programar.
Van a aprender a construir productos completos.
Van a tener un proyecto real en su portfolio.
Van a poder mostrarlo en entrevistas laborales.

**¿Preguntas?**"

## 🎤 Tips de Presentación

### Antes de empezar:
1. Tener 2 pestañas abiertas:
   - Dashboard funcionando
   - `/docs` de la API
2. Tener VS Code abierto con el proyecto
3. Tener DBeaver/pgAdmin con BD abierta
4. Terminal lista con entorno virtual activado

### Durante la presentación:
- **Ir despacio en el código** - muchos nunca programaron
- **Usar analogías** - "La API es como un mozo que toma tu pedido"
- **Mostrar, no solo decir** - código en vivo, no slides
- **Interactuar** - hacer preguntas, pedir predicciones
- **Celebrar complejidad** - "Esto es avanzado, pero lo van a dominar"

### Frases útiles:
- "Esto puede parecer complejo ahora, pero en la semana X van a..."
- "¿Alguien puede adivinar qué hace esta línea?"
- "Miren qué elegante es esta solución..."
- "Esto lo van a usar en cada proyecto que hagan"

## 📝 Recursos para Compartir

**Al final de la clase, compartir:**

1. Link al repositorio GitHub
2. URL del dashboard deployado
3. Credenciales de demo:
   - Email: admin@bcra-dashboard.com
   - Password: admin123

4. Documentación recomendada:
   - FastAPI: https://fastapi.tiangolo.com/
   - Bootstrap: https://getbootstrap.com/
   - Chart.js: https://www.chartjs.org/

## ⚡ Plan B - Si algo falla

### Si no funciona el internet:
- Tener screenshots del dashboard
- Mostrar código offline
- Explicar la arquitectura en pizarra

### Si PostgreSQL tiene problemas:
- Cambiar temporalmente a SQLite en `.env`:
  ```
  DATABASE_URL=sqlite:///./bcra_dashboard.db
  ```

### Si el deploy no está listo:
- Correr localmente
- "El deploy lo haremos juntos en clase X"

## 🎯 Objetivos Logrados al Final de la Presentación

Los estudiantes deben:
- [ ] Entender el flujo completo de datos
- [ ] Ver que el stack es integrado, no piezas sueltas
- [ ] Sentirse motivados (no abrumados)
- [ ] Tener claro que al final harán algo similar
- [ ] Conocer las herramientas principales del curso

---

**¡Éxito en la presentación! 🚀**
