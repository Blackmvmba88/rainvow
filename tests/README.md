# Tests del Proyecto Rainvow

Este directorio contiene las pruebas automatizadas del proyecto.

## Estructura

```
tests/
├── __init__.py                # Inicialización del paquete de tests
├── test_spotify_live.py       # Tests para Spotify Live
└── README.md                  # Este archivo
```

## Ejecutar Tests

### Con pytest (recomendado)

```bash
# Instalar pytest
pip install pytest pytest-cov

# Ejecutar todos los tests
pytest

# Con verbosidad
pytest -v

# Con cobertura
pytest --cov=. --cov-report=html

# Test específico
pytest tests/test_spotify_live.py
```

### Manualmente

```bash
# Ejecutar archivo de test individual
python3 tests/test_spotify_live.py
```

## Escribir Nuevos Tests

### Convenciones

1. **Nombres de archivos**: `test_*.py`
2. **Nombres de funciones**: `test_*`
3. **Nombres de clases**: `Test*`
4. **Idioma**: Comentarios en español
5. **Docstrings**: Describir qué verifica el test

### Ejemplo

```python
"""Tests para el módulo de visualización."""

def test_band_amps():
    """Verifica que get_band_amps retorna array correcto."""
    import numpy as np
    from ondads import get_band_amps
    
    audio = np.random.uniform(-1, 1, size=(2205, 1))
    amps = get_band_amps(audio, 44100, 7)
    
    assert len(amps) == 7
    assert all(amp >= 0 for amp in amps)
```

## Tests Existentes

### test_spotify_live.py

Verifica funcionalidad básica de la aplicación Spotify Live:

- **test_app_imports**: Importación de módulos
- **test_token_validation**: Lógica de validación de tokens
- **test_search_params_validation**: Validación de parámetros

## Agregar Tests para Nuevos Módulos

Al agregar funcionalidad nueva:

1. Crear archivo `test_<modulo>.py`
2. Importar módulo a testear
3. Escribir tests para funciones públicas
4. Verificar casos edge
5. Documentar con docstrings

## Mocking

Para funciones que dependen de servicios externos:

```python
from unittest.mock import Mock, patch

def test_spotify_api():
    """Test con mock de Spotify API."""
    with patch('spotipy.Spotify') as mock_spotify:
        mock_spotify.return_value.search.return_value = {
            'tracks': {'items': []}
        }
        # Tu test aquí
```

## Coverage

Verificar cobertura de código:

```bash
pytest --cov=. --cov-report=html
# Abrir htmlcov/index.html en navegador
```

Meta: >80% de cobertura en código crítico.

## CI/CD

Los tests se ejecutan automáticamente en:
- Push a main/develop
- Pull Requests
- Semanalmente (lunes 9:00 UTC)

Ver: `.github/workflows/ci-cd.yml`

## Contribuir

Al enviar un PR:
- [ ] Tests existentes pasan
- [ ] Nuevos tests para funcionalidad nueva
- [ ] Coverage no disminuye significativamente
- [ ] Tests documentados con docstrings

Ver [CONTRIBUTING.md](../CONTRIBUTING.md) para más detalles.
