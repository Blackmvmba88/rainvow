# Guía de Colaboración del Equipo

## 🤝 Objetivo

Este documento establece las prácticas y procesos para la colaboración efectiva del equipo en el proyecto Rainvow.

## 📅 Reuniones Semanales

### Sincronización del Equipo

**Frecuencia**: Semanal  
**Duración**: 30-45 minutos  
**Día sugerido**: Lunes a las 10:00 AM

### Agenda de la Reunión

1. **Revisión de progreso (10 min)**
   - ¿Qué se completó la semana pasada?
   - Verificar checklist del CHANGELOG.md
   - Revisar PRs mergeados

2. **Bloqueos y desafíos (10 min)**
   - ¿Hay impedimentos técnicos?
   - ¿Se necesita ayuda en alguna área?
   - Discusión de issues problemáticos

3. **Planificación semanal (15 min)**
   - Priorizar issues para la semana
   - Asignar tareas
   - Establecer objetivos claros

4. **Temas técnicos (10 min)**
   - Decisiones de arquitectura
   - Actualizaciones de dependencias
   - Mejoras de rendimiento

5. **Cierre (5 min)**
   - Confirmar siguiente reunión
   - Resumen de acuerdos

### Formato de Reuniones

- **Presencial/Virtual**: Según disponibilidad del equipo
- **Herramienta recomendada**: Google Meet, Zoom, o Discord
- **Notas**: Documentar en issues de GitHub o documento compartido

## 🔄 Flujo de Trabajo

### Branching Strategy

```
main (producción)
  ├── develop (desarrollo)
  │   ├── feature/nueva-funcionalidad
  │   ├── fix/correccion-bug
  │   └── docs/actualizacion-documentacion
```

### Proceso de Contribución

1. **Crear issue** describiendo el problema o funcionalidad
2. **Crear branch** desde `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/mi-funcionalidad
   ```
3. **Desarrollar** siguiendo las guías del proyecto
4. **Commit** con mensajes claros en español:
   ```bash
   git commit -m "Agrega visualizador de frecuencias en tiempo real"
   ```
5. **Push** y crear Pull Request:
   ```bash
   git push origin feature/mi-funcionalidad
   ```
6. **Code Review** por al menos un miembro del equipo
7. **Merge** a develop después de aprobación

### Estándares de Código

- **Idioma**: Comentarios y documentación en español
- **Estilo Python**: Seguir PEP 8
- **Línea máxima**: 100 caracteres
- **Imports**: Organizados con isort
- **Formateo**: Usar black para consistencia

## 📝 Revisión de Código

### Checklist para Reviewer

- [ ] El código sigue los estándares del proyecto
- [ ] Comentarios y documentación en español
- [ ] No hay credenciales o secretos expuestos
- [ ] Manejo adecuado de errores
- [ ] Tests actualizados (si aplica)
- [ ] Documentación actualizada
- [ ] No introduce regresiones

### Checklist para Autor

Antes de solicitar review:
- [ ] Código funciona localmente
- [ ] Linting sin errores críticos
- [ ] Documentación actualizada
- [ ] CHANGELOG.md actualizado
- [ ] Commits limpios y descriptivos

## 🚨 Reportar Issues

### Template de Issue

```markdown
## Descripción
[Descripción clara del problema o funcionalidad]

## Pasos para Reproducir (si es bug)
1. ...
2. ...
3. ...

## Comportamiento Esperado
[Qué debería pasar]

## Comportamiento Actual
[Qué está pasando]

## Capturas de Pantalla
[Si aplica]

## Entorno
- OS: [e.g., macOS 13, Ubuntu 22.04]
- Python: [e.g., 3.9]
- Dependencias: [versiones relevantes]
```

## 🎯 Roles y Responsabilidades

### Mantenedores del Proyecto
- Revisar y aprobar PRs
- Gestionar releases
- Mantener roadmap actualizado
- Facilitar reuniones semanales

### Contribuidores
- Desarrollar nuevas funcionalidades
- Corregir bugs
- Mejorar documentación
- Participar en code reviews

### Todos los Miembros
- Asistir a reuniones semanales
- Comunicar bloqueos proactivamente
- Mantener issues actualizados
- Seguir estándares del proyecto

## 📊 Métricas y KPIs

### Métricas de Equipo

- **Velocity**: Issues cerrados por semana
- **Code Review Time**: Tiempo promedio de review
- **Bug Rate**: Nuevos bugs vs bugs cerrados
- **Test Coverage**: % de código cubierto por tests
- **Documentation**: % de funciones documentadas

### Revisar en Reuniones

Cada mes revisar:
- Tendencias de velocity
- Backlog health
- Deuda técnica acumulada
- Satisfacción del equipo

## 🛠️ Herramientas del Equipo

### Comunicación
- **GitHub Issues**: Tracking de tareas
- **GitHub Discussions**: Conversaciones técnicas
- **Discord/Slack**: Comunicación rápida (opcional)

### Desarrollo
- **Git**: Control de versiones
- **GitHub Actions**: CI/CD
- **pytest**: Testing (cuando aplique)

### Documentación
- **Markdown**: Documentación en repositorio
- **GitHub Wiki**: Documentación extendida (opcional)

## 📚 Recursos

### Guías del Proyecto
- [README.md](README.md) - Información general
- [ARCHITECTURE.md](ARCHITECTURE.md) - Arquitectura del sistema
- [TESTING.md](TESTING.md) - Estrategias de testing
- [CHANGELOG.md](CHANGELOG.md) - Historial de cambios

### Referencias Externas
- [PEP 8](https://pep8.org/) - Guía de estilo Python
- [Conventional Commits](https://www.conventionalcommits.org/) - Estándar de commits
- [Spotify Web API](https://developer.spotify.com/documentation/web-api/) - API Reference

## 🔄 Actualización de este Documento

Este documento debe revisarse y actualizarse:
- Cada trimestre en reunión de equipo
- Cuando cambien procesos significativos
- Cuando el equipo crezca o cambie

**Última actualización**: 2025-10-15
**Próxima revisión**: 2026-01-15

---

**Nota**: La colaboración efectiva es clave para el éxito del proyecto. Todos los miembros del equipo son responsables de mantener estos estándares y mejorar continuamente nuestros procesos.
