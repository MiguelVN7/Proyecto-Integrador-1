# Sigere – Sistema de Gestión de Reservas Deportivas

## Contexto del proyecto
Sigere es una aplicación web desarrollada como proyecto académico para la asignatura **Proyecto Integrador 1 (2025-1)**. Permite a estudiantes y personal universitario reservar espacios deportivos, gestionar horarios y consultar información relevante sobre los escenarios disponibles. El proyecto utiliza **Django 5**, **SQLite** como base de datos local y un front-end basado en **HTML/CSS** con archivos estáticos propios. Además, integra servicios de **OpenAI** para generar descripciones e imágenes de los espacios deportivos.

Los usuarios principales son:

- Estudiantes de la universidad que desean reservar espacios deportivos.
- Personal administrativo encargado de supervisar las reservas y mantener la información actualizada.

El equipo de desarrollo está conformado por **Diego Mesa, Andrés Alarcón y Miguel Villegas**.

## Evaluación autocrítica de calidad
La revisión se centra en cuatro parámetros clave: **Usabilidad**, **Compatibilidad**, **Rendimiento** y **Seguridad**. Para cada uno se describen los puntos positivos actuales, las áreas que requieren mejora y oportunidades de inversión futuras.

### Usabilidad
 **Cumple**
- Flujo de navegación sencillo con vistas separadas para inicio, registro, reservas, perfil y consultas de espacios.
- Formularios con validaciones básicas y mensajes de retroalimentación utilizando el sistema de mensajes de Django.
- Diseño responsive básico mediante estilos personalizados y componentes ligeros, lo que facilita el acceso desde dispositivos móviles.

 **A mejorar**
- El diseño visual puede modernizarse (colores, tipografía, microinteracciones) para mejorar la experiencia del usuario.
- Faltan ayudas contextuales y tutoriales breves que guíen al usuario en su primera reserva.
- Accesibilidad limitada: no se han revisado contrastes, etiquetas ARIA ni soporte completo para teclado.

 **Oportunidades de inversión**
- Destinar tiempo a pruebas de usabilidad con estudiantes para identificar cuellos de botella específicos.
- Invertir en una librería de componentes UI moderna (p. ej., Tailwind, Bootstrap o un sistema de diseño interno) y en un diseñador UX que unifique la experiencia.
- Incorporar métricas de experiencia (encuestas in-app, heatmaps) para medir satisfacción en un contexto académico con recursos limitados.

### Compatibilidad
 **Cumple**
- Arquitectura basada en Django permite ejecución tanto en entornos locales como en plataformas PaaS (ej. Render) con configuración mínima.
- Uso de SQLite en desarrollo simplifica la instalación y evita dependencias externas complejas.
- Los recursos estáticos se sirven con WhiteNoise, facilitando despliegues en diversos servidores.

 **A mejorar**
- No se ha verificado compatibilidad con múltiples navegadores (solo pruebas en Chrome/Edge).
- Dependencia de servicios externos como OpenAI sin mecanismos de fallback cuando la API no está disponible.
- Falta automatización para configurar variables de entorno críticas (OPENAI_API_KEY, DEBUG, etc.).

 **Oportunidades de inversión**
- Configurar entornos de pruebas cross-browser (BrowserStack, Sauce Labs) para detectar inconsistencias tempranas.
- Implementar un sistema de configuración más robusto (por ejemplo, `django-environ`) y documentación clara para despliegues.
- Evaluar la migración a una base de datos relacional en la nube (PostgreSQL) con scripts de infraestructura como código para escenarios empresariales.

### Rendimiento
 **Cumple**
- El uso de Django y plantillas server-side reduce la carga en el cliente y mantiene tiempos de respuesta bajos para el volumen actual.
- Consultas principales están filtradas por usuario, lo que evita transferencias innecesarias de datos.
- Archivos estáticos precompilados y servidos localmente, minimizando la latencia en el contexto académico.

 **A mejorar**
- No existen pruebas de carga o métricas de rendimiento registradas; el comportamiento bajo alta concurrencia es desconocido.
- La generación de contenido con OpenAI puede introducir latencias significativas y no se ejecuta de forma asíncrona.
- Falta caching de consultas frecuentes (espacios deportivos, reservas activas) y compresión adicional para assets pesados.

 **Oportunidades de inversión**
- Configurar monitoreo de rendimiento (Django Debug Toolbar en desarrollo, herramientas APM en producción) para identificar cuellos de botella.
- Explorar la ejecución asíncrona o en segundo plano (Celery, RQ) para llamadas a APIs externas.
- Optimizar imágenes y habilitar caching en CDN o en el propio WhiteNoise para reducir el tiempo de carga percibido.

### Seguridad
 **Cumple**
- Autenticación integrada con el modelo personalizado de usuario y vistas protegidas mediante `login_required`.
- Uso de Hashing de contraseñas y validadores por defecto de Django.
- Protección CSRF y middleware de seguridad habilitados por defecto en Django.

 **A mejorar**
- Variables sensibles (SECRET_KEY, credenciales API) están hardcodeadas o dependen del entorno local sin controles adicionales.
- No se han implementado políticas de contraseñas avanzadas ni verificación en dos pasos.
- Ausencia de pruebas de seguridad o auditorías básicas (scanners de vulnerabilidades, revisión de dependencias).

 **Oportunidades de inversión**
- Migrar los secretos a un gestor seguro (Render Secrets, AWS Secrets Manager) y rotarlos periódicamente.
- Implementar autenticación multifactor y políticas de contraseña acordes a estándares universitarios.
- Integrar análisis de dependencias (Dependabot, GitHub Advanced Security) y pruebas de penetración ligeras para prevenir vulnerabilidades.

---
Esta autoevaluación ofrece una hoja de ruta práctica para priorizar mejoras de calidad en un proyecto académico con aspiraciones de escalabilidad futura. Las recomendaciones permiten escalar gradualmente hacia un estándar empresarial si se dispone de recursos adicionales.

## Principio de Inversión de Dependencias aplicado

Para reducir el acoplamiento con la API de OpenAI y facilitar pruebas, se aplicó el principio **Dependency Inversion Principle (DIP)** en el módulo responsable de generar descripciones e imágenes:

1. **Diagnóstico**: Las vistas `descripcion_espacio_deportivo`, `generar_imagen_espacio` y `descripcion_e_imagen_view` dependían directamente de la clase `OpenAI`, lo que dificultaba cambiar de proveedor o realizar pruebas unitarias.
2. **Abstracción**: Se creó la interfaz `AIContentProvider` (en `Sigere/Apps/LandingPage/services/ai_provider.py`) que expone los métodos `generate_description` y `generate_image_url`.
3. **Implementación concreta**: Se implementó `OpenAIContentProvider`, responsable de interactuar con la librería oficial de OpenAI y encapsular errores específicos.
4. **Inyección de dependencias**: El archivo `Sigere/settings.py` define `AI_CONTENT_PROVIDER`, permitiendo seleccionar la clase concreta y sus parámetros mediante configuración. Las vistas consumen la abstracción usando `get_ai_provider()` (caché simple) y capturan `AIProviderError`.
5. **Beneficios**: Ahora es posible reemplazar la implementación por un mock en pruebas, utilizar un proveedor alterno o incluso desactivar la integración sin modificar las vistas.

Para instanciar manualmente el proveedor actual:

```python
from Sigere.Apps.LandingPage.services import get_ai_provider

provider = get_ai_provider()
descripcion = provider.generate_description("Coliseo EAFIT", palabras=120)
imagen_url = provider.generate_image_url("Coliseo EAFIT")
```

Puedes registrar otra implementación creando una clase que herede de `AIContentProvider` y actualizando `AI_CONTENT_PROVIDER['CLASS']` en `settings.py`.

## Patrones de diseño de Django aplicados

### Patrón 1 – Manager/QuerySet personalizados (Capa: Modelos)
- **Decisión**: Centralizar la lógica de filtrado de reservas en `Sigere/Apps/LandingPage/managers.py` para cumplir con el enfoque *Fat Models / Skinny Views*.
- **Implementación**: Se creó `ReservaQuerySet` con métodos reutilizables (`for_user`, `active`, `past`, `cancelled`, `ordered_recent_first`) y se asoció a `Reserva` mediante `Reserva.objects = ReservaQuerySet.as_manager()`.
- **Beneficios**: Las vistas y métodos de `Usuario` ahora invocan `reserva_set.active()` y similares, reduciendo duplicación y mejorando la testabilidad de las consultas.

### Patrón 2 – Class-Based Views con Mixins (Capa: Vistas)
- **Decisión**: Migrar `misReservas` y `perfil` a vistas basadas en clases para reutilizar comportamientos comunes y facilitar la extensión.
- **Implementación**: Se añadieron `MisReservasView (LoginRequiredMixin, ListView)` y `PerfilView (LoginRequiredMixin, TemplateView)` en `views.py`, aprovechando el manager personalizado para obtener los datos.
- **Beneficios**: Menos código repetido, separación clara entre obtención de datos y renderizado, y soporte nativo para pruebas y extensiones futuras (paginación, filtros, etc.).

### Patrón 3 – Normalización (Capa: Modelos)
- **Decisión**: Separar los campos académicos del modelo `Usuario` en una entidad específica siguiendo el principio de normalización.
- **Implementación**: Se creó `PerfilUniversitario` (OneToOne con `Usuario`) en `models.py`, se añadieron formularios dedicados (`DatosUniversitariosForm`) y un `post_save` signal que garantiza su existencia. Las vistas actualizan este perfil mediante formularios independientes.
- **Beneficios**: Datos personales y académicos quedan desacoplados, facilitando futuras extensiones (perfiles múltiples, auditorías), reduce la presencia de campos opcionales en el usuario base y permite reusar el perfil en otros contextos.

### Ejemplo de uso rápido

```python
from Sigere.Apps.LandingPage.models import Reserva

# Obtener reservas activas ordenadas para un usuario dado
reservas = (Reserva.objects
			.for_user(usuario_actual)
			.active()
			.ordered_recent_first())

# Registrar la URL de mis reservas (vista basada en clase)
from django.urls import path
from Sigere.Apps.LandingPage.views import MisReservasView

urlpatterns = [
	path('misReservas/', MisReservasView.as_view(), name='misReservas'),
]

# Perfil universitario normalizado asociado al usuario
from Sigere.Apps.LandingPage.models import PerfilUniversitario

perfil = PerfilUniversitario.objects.get(usuario=usuario_actual)
perfil.carrera = "Ingeniería"
perfil.save()

# Recordar generar la migración correspondiente:
# python manage.py makemigrations LandingPage
# python manage.py migrate
```


## Nueva funcionalidad: Sistema de reseñas y calificaciones

### Descripción general
Se implementó desde cero un **sistema de reseñas** para que cada usuario pueda calificar los espacios deportivos una vez finaliza su reserva. La información agregada (promedios y número de reseñas) se expone en la ficha del espacio y en un panel dedicado. Esta funcionalidad fortalece la toma de decisiones de los estudiantes y agrega un componente social al producto.

### Patrones de diseño aplicados

| Capa | Patrón | Justificación | Alternativa descartada | Beneficios | Trade-offs |
|------|--------|---------------|------------------------|------------|-----------|
| Modelos | Normalización + señal `post_save` (`PerfilUniversitario`, `Resena`) | Separar datos académicos y reseñas en tablas dedicadas garantiza integridad y crea los perfiles automáticamente. | Mantener campos denormalizados en `Usuario`/`Reserva`. | Datos coherentes, extensibilidad futura. | Más migraciones y tablas a mantener. |
| Servicios | Service Layer (`services/reviews.py`) | Encapsula la lógica de negocio (validaciones, estadísticas) fuera de vistas y modelos. | Métodos ad-hoc en vistas. | Código reutilizable y testeable. | Archivo adicional que el equipo debe ubicar. |
| Vistas | Class-Based Views con mixins (`ReviewCreateView`, `ReviewDashboard`) | Gestionan formularios y permisos con menos boilerplate y hooks claros. | Funciones basadas en vistas. | Reutilización y orden. | Curva de aprendizaje para entender el flujo CBV. |
| Formularios | `ModelForm` + validación personalizada | Garantiza que sólo usuarios con reservas emitidas califiquen. | Formularios manuales. | Menos código y validación centralizada. | Dependencia fuerte del modelo. |
| Templates | Template tags (`rating_tags.py`) | Renderiza estrellas y promedios de forma consistente. | Lógica en los templates. | Reutilización limpia. | Deben cargarse explícitamente en cada template. |
| Persistencia | Manager/QuerySet (`ReviewQuerySet`) | Expone filtros como `for_space` o `published` usados en vistas y servicios. | Filtrado in situ en cada consulta. | API expresiva y DRY. | Necesita mantenimiento coordinado. |

### Especificaciones funcionales

**Requisitos clave**

- Permitir reseñas únicamente para reservas efectivamente realizadas por el usuario.
- Calcular métricas agregadas por espacio (promedio y total de reseñas).
- Evitar duplicados mediante `UniqueConstraint` por usuario/espacio/reserva.
- Mostrar reseñas personales y ranking global de espacios.

**Casos de uso**

1. Deportista califica un espacio desde su historial de reservas.
2. Otro estudiante consulta calificaciones antes de reservar.
3. Administrador modera reseñas desde el panel de Django.

**User stories representativas**

- “Como deportista, quiero dejar mi reseña tras usar el espacio para ayudar a otros compañeros.”
- “Como estudiante, deseo conocer la reputación de un espacio antes de reservarlo.”
- “Como administrador, necesito revisar reseñas para detectar problemas recurrentes.”

### Implementación destacada

- `Resena` añade `UniqueConstraint` y relaciona usuario, reserva y espacio.
- Campos `calificacion_promedio` y `total_resenas` en `EspacioDeportivo` se actualizan vía señales `post_save/post_delete`.
- `ReviewService` centraliza validaciones, registro y generación de métricas.
- Vistas basadas en clases (`resenas_dashboard`, `resena_crear`, `resena_eliminar`) usan mixins de autenticación y mensajes.
- Template tag `star_range` pinta estrellas reutilizables en los listados.

### Cómo probar rápidamente

```python
from Sigere.Apps.LandingPage.models import Reserva
from Sigere.Apps.LandingPage.services.reviews import ReviewService

reserva = Reserva.objects.active().first()
ReviewService.register_review(
	reserva=reserva,
	usuario=reserva.usuario,
	calificacion=4,
	comentario="Iluminación excelente"
)
```

Las migraciones en `LandingPage/0006_*.py` crean las tablas necesarias y migran datos académicos existentes a `PerfilUniversitario` para evitar errores al cargar el perfil.