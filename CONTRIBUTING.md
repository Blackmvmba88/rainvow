# Guía de Contribución

¡Gracias por tu interés en contribuir a Rainvow! Esta guía te ayudará a empezar.

## 🚀 Cómo Contribuir

### 1. Fork y Clonar

```bash
# Fork el repositorio en GitHub
# Luego clona tu fork
git clone https://github.com/TU_USUARIO/rainvow.git
cd rainvow
```

### 2. Configurar Entorno

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Instalar herramientas de desarrollo
pip install black isort flake8 pytest
```

### 3. Crear Branch

```bash
git checkout -b feature/mi-funcionalidad
```

Usa prefijos descriptivos:
- `feature/` - Nueva funcionalidad
- `fix/` - Corrección de bugs
- `docs/` - Cambios en documentación
- `refactor/` - Refactorización de código
- `test/` - Añadir o mejorar tests

### 4. Hacer Cambios

Sigue estos estándares:

#### Código Python
- **Idioma**: Comentarios y documentación en español
- **Estilo**: PEP 8, máximo 100 caracteres por línea
- **Formateo**: Usa `black` y `isort`

```bash
# Formatear código
black .
isort .

# Verificar linting
flake8 .
```

#### Commits
Mensajes claros y descriptivos en español:

```bash
git commit -m "Agrega visualizador de espectro de frecuencias"
git commit -m "Corrige error en renovación de tokens de Spotify"
git commit -m "Actualiza documentación de instalación"
```

### 5. Testing

Antes de enviar tu PR:

```bash
# Verificar sintaxis
python -m py_compile tu_archivo.py

# Ejecutar tests (si existen)
pytest

# Verificar que tu código funciona
python tu_archivo.py
```

### 6. Documentar

Actualiza la documentación relevante:
- README.md si cambia funcionalidad principal
- CHANGELOG.md con tus cambios
- Docstrings en funciones nuevas
- Comentarios en código complejo

### 7. Push y Pull Request

```bash
git push origin feature/mi-funcionalidad
```

Luego crea un Pull Request en GitHub con:
- **Título descriptivo** en español
- **Descripción clara** de los cambios
- **Referencias** a issues relacionados
- **Screenshots** si hay cambios visuales

## 📋 Checklist de PR

Antes de enviar tu PR, verifica:

- [ ] Código sigue estándares del proyecto (PEP 8)
- [ ] Código formateado con black e isort
- [ ] Sin errores de flake8 (críticos)
- [ ] Comentarios y documentación en español
- [ ] CHANGELOG.md actualizado
- [ ] Código funciona localmente
- [ ] No hay credenciales o secretos expuestos
- [ ] Tests actualizados (si aplica)

## 🐛 Reportar Bugs

Usa el template de issues de GitHub. Incluye:
- Descripción clara del problema
- Pasos para reproducir
- Comportamiento esperado vs actual
- Información del entorno (OS, Python version)
- Screenshots si aplica

## 💡 Sugerir Funcionalidades

Abre un issue describiendo:
- ¿Qué problema resuelve?
- ¿Cómo funcionaría?
- ¿Hay alternativas?
- Beneficios para el proyecto

## 📚 Áreas de Contribución

### Alta Prioridad
- Pruebas automatizadas (pytest)
- Mejoras de rendimiento
- Documentación de APIs
- Ejemplos de uso

### Siempre Bienvenidos
- Corrección de bugs
- Mejoras de documentación
- Optimización de código
- Nuevas funcionalidades

### Requieren Discusión
- Cambios de arquitectura
- Nuevas dependencias
- Breaking changes
- Cambios de API

## 🔍 Code Review

Tu PR será revisado por mantenedores. Esperamos:
- Respuestas a comentarios en 48 horas
- Apertura a feedback constructivo
- Disposición para iterar en el código

## 🎯 Estándares de Calidad

### Código
- Funciones < 50 líneas (preferible)
- Complejidad ciclomática < 10
- Nombres descriptivos de variables
- Sin código muerto o comentado

### Documentación
- Docstrings en funciones públicas
- Comentarios para lógica compleja
- README actualizado si necesario
- Ejemplos de uso claros

### Testing
- Código testeable (funciones puras cuando sea posible)
- Tests para nuevas funcionalidades (deseable)
- No romper tests existentes

## ❓ Preguntas

Si tienes dudas:
1. Revisa la documentación existente
2. Busca en issues cerrados
3. Abre un issue con tu pregunta
4. Contacta a los mantenedores

## 📜 Código de Conducta

- Sé respetuoso y constructivo
- Acepta feedback con mente abierta
- Enfócate en el código, no en la persona
- Ayuda a otros contribuidores
- Mantén un ambiente positivo

## 🙏 Agradecimientos

Toda contribución es valiosa, desde corregir un typo hasta implementar funcionalidades complejas. ¡Gracias por ayudar a mejorar Rainvow!

---

**Recursos Útiles**:
- [TEAM.md](TEAM.md) - Guía de colaboración del equipo
- [ARCHITECTURE.md](ARCHITECTURE.md) - Arquitectura del proyecto
- [TESTING.md](TESTING.md) - Estrategias de testing
