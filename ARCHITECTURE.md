# Arquitectura de Sigere

## Visión general
- **Framework**: Django 5 (patrón MTV clásico).
- **Módulo principal**: `Sigere/Apps/LandingPage` concentra modelos, vistas, formularios y templates.
- **Base de datos**: SQLite en desarrollo, con capacidad de cambiar a PostgreSQL mediante configuración (`dj-database-url`).
- **Estática**: Servida con WhiteNoise y recursos ubicados en `static/`.
- **Integraciones**: OpenAI para generación de descripciones e imágenes.

## Capas y responsabilidades
| Capa | Componentes | Responsabilidades clave |
|------|-------------|-------------------------|
| Modelos | `models.py`, `managers.py` | Definición de entidades (Usuario, PerfilUniversitario, EspacioDeportivo, Reserva) y lógica de consulta especializada mediante `ReservaQuerySet`. |
| Vistas | `views.py` | Controladores de flujo: CBV para reservas y perfil, FVs para autenticación y servicios IA. |
| Formularios | `forms.py` | Validación de datos de usuario (`DatosPersonalesForm`, `DatosUniversitariosForm`) y reservas (`ReservaForm`). |
| Templates | `templates/LandingPage` | Presentación basada en Bootstrap + estilos personalizados. |
| Servicios | `services/` | Integración desacoplada con OpenAI (`AIContentProvider`, `OpenAIContentProvider`). |

## Patrones de diseño aplicados
### 1. Manager/QuerySet personalizados (Modelos)
- `Sigere/Apps/LandingPage/managers.py` define `ReservaQuerySet` con métodos reutilizables (`for_user`, `active`, `past`, `cancelled`, `ordered_recent_first`).
- `Reserva` usa `ReservaQuerySet.as_manager()` para que tanto `Reserva.objects` como `usuario.reserva_set` expongan estas operaciones.
- Resultado: lógica de filtrado coherente, vistas más ligeras y posibilidad de encadenar consultas legibles.

### 2. Class-Based Views + Mixins (Vistas)
- `MisReservasView (LoginRequiredMixin, ListView)` encapsula la lista de reservas del usuario utilizando el manager personalizado.
- `PerfilView (LoginRequiredMixin, TemplateView)` centraliza la carga/actualización de formularios y estadísticos del usuario.
- Resultado: reutilización de comportamientos, menor duplicación, fácil extensión (paginación, permisos, etc.).

### 3. Normalización de modelos (Modelos)
- Se introdujo `PerfilUniversitario` (relación OneToOne con `Usuario`) para aislar la información académica.
- Formularios (`DatosUniversitariosForm`) y vistas se actualizan para operar sobre esta entidad; un signal `post_save` garantiza que cada usuario disponga de un perfil asociado.
- Resultado: datos personales y académicos desacoplados, reducción de campos opcionales en `Usuario` y estructura apta para auditorías o futuras extensiones.

## Flujo principal
1. **Autenticación**: Vistas `login_view` y `signup_view` gestionan el acceso de usuarios.
2. **Reserva de espacios**: `reservar_deportivos` utiliza formularios y modelos para persistir reservas.
3. **Visualización de reservas**: `MisReservasView` muestra reservas ordenadas; las estadísticas se consumen en `PerfilView`.
4. **IA asistida**: `descripcion_espacio_deportivo`, `generar_imagen_espacio` y `descripcion_e_imagen_view` consultan al proveedor definido en `settings.AI_CONTENT_PROVIDER`.

## Instrucciones de extensión
- **Nuevo proveedor IA**: implemente una clase que herede de `AIContentProvider` y actualice `AI_CONTENT_PROVIDER['CLASS']` en `settings.py`.
- **Nuevos perfiles académicos**: extienda `PerfilUniversitario` con datos adicionales y expóngalos mediante formularios dedicados.
- **Nuevas métricas de reservas**: agregue métodos a `ReservaQuerySet` y consúmalos desde vistas o templates.
- **Nuevas vistas protegidas**: derive de `LoginRequiredMixin` + CBV adecuados (`ListView`, `DetailView`, etc.) para mantener coherencia.

## Diagramas (alto nivel)
```
Usuarios ─▶ Vistas (CBV/FV) ─▶ Formularios ─▶ Modelos/Managers ─▶ Base de datos
                     │
                     └────▶ Servicios (AIContentProvider) ─▶ OpenAI
```

Este documento resume la arquitectura tras la aplicación de los patrones solicitados y sirve como guía para futuras contribuciones.
