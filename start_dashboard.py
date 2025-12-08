#!/usr/bin/env python3
"""
Script de inicio rápido para el Dashboard de Rainvow.

Este script verifica las dependencias, informa al usuario sobre
componentes disponibles, y lanza el dashboard con configuración básica.
"""

import sys
import subprocess


def check_dependency(module_name, package_name=None):
    """Verifica si un módulo está instalado."""
    if package_name is None:
        package_name = module_name

    try:
        __import__(module_name)
        return True
    except ImportError:
        return False


def main():  # noqa: C901
    """Función principal que verifica dependencias e inicia el dashboard."""
    print("=" * 60)
    print("🌈 Inicio Rápido del Dashboard de Rainvow")
    print("=" * 60)
    print()

    # Verificar dependencias principales
    dependencies = {
        'flask': 'Flask',
        'flask_socketio': 'Flask-SocketIO',
        'psutil': 'psutil',
        'numpy': 'NumPy',
    }

    missing = []
    for module, name in dependencies.items():
        if check_dependency(module):
            print(f"✓ {name} instalado")
        else:
            print(f"✗ {name} NO instalado")
            missing.append(module)

    print()

    # Verificar dependencias opcionales
    print("Dependencias opcionales:")
    optional_deps = {
        'sounddevice': ('Audio en tiempo real', 'sounddevice'),
        'spotipy': ('Integración con Spotify', 'spotipy'),
        'openrgb': ('Control RGB Keyboard', 'openrgb-python'),
        'pygetwindow': ('Seguimiento de ventanas', 'pygetwindow'),
    }

    for module, (desc, package) in optional_deps.items():
        if check_dependency(module):
            print(f"  ✓ {desc}")
        else:
            print(f"  ○ {desc} (pip install {package})")

    print()

    if missing:
        print("⚠️  Faltan dependencias principales:")
        for dep in missing:
            print(f"   pip install {dep}")
        print()
        response = input("¿Deseas instalarlas ahora? (s/n): ")
        if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
            print("\nInstalando dependencias...")
            # Validar contra lista conocida de dependencias
            valid_deps = {'flask', 'flask_socketio', 'psutil', 'numpy'}
            safe_deps = [dep for dep in missing if dep in valid_deps]
            if not safe_deps:
                print("❌ Error: Dependencias no válidas")
                return 1
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-q"
            ] + safe_deps)
            print("✓ Dependencias instaladas\n")
        else:
            print("\nPor favor instala las dependencias manualmente:")
            print("  pip install -r requirements.txt\n")
            return 1

    print("🚀 Iniciando dashboard...")
    print("   URL: http://localhost:5000")
    print("   Presiona Ctrl+C para detener")
    print()

    # Importar y ejecutar dashboard
    try:
        import dashboard
        dashboard.start_background_threads()
        port = 5000
        dashboard.socketio.run(
            dashboard.app,
            host='0.0.0.0',
            port=port,
            debug=False,
            allow_unsafe_werkzeug=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard detenido")
        return 0
    except Exception as e:
        print(f"\n❌ Error al iniciar dashboard: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
