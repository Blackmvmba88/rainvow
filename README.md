# Rainvow AR Demo

Este proyecto incluye una sencilla demostración de realidad aumentada con [A-Frame](https://aframe.io/) y [AR.js](https://ar-js-org.github.io/AR.js/). El archivo `ar.html` despliega un cubo 3D animado cuando la cámara detecta el marcador *hiro*.
Para hacerlo más visual, se integra [Hydra-synth](https://github.com/ojack/hydra) como capa de efectos sobre la escena.

## Cómo ejecutar

1. Inicia un servidor local en la raíz del proyecto. Por ejemplo:
   
   ```bash
   # Con Python
   python3 -m http.server
   
   # o con Node
   npx http-server
   ```
2. Abre `http://localhost:8000/ar.html` en un navegador moderno (Chrome, Firefox, Safari).
3. Concede permisos de cámara cuando lo solicite el navegador.
4. Apunta la cámara a un marcador *hiro*. Puedes imprimir uno desde [este enlace](https://raw.githubusercontent.com/AR-js-org/AR.js/master/data/images/HIRO.jpg).

Para que la cámara funcione, la página debe servirse mediante `https` o desde `localhost`.

## Requisitos

- Navegador con soporte WebGL y permisos de cámara.
- Conexión segura (HTTPS o entorno local) para acceder a la cámara.

Esta demo es autónoma y no necesita dependencias adicionales.

### Efecto Hydra

Al abrir `ar.html`, notarás una capa de patrones generativos. Estos efectos se generan con Hydra-synth y se mezclan sobre la imagen de la cámara para dar un aspecto más dinámico. Puedes modificar el código de Hydra en el archivo para experimentar con otros visuales.

### Lectura de PDFs con Hydra

También puedes abrir `pdf_overlay.html` para cargar un archivo PDF desde tu equipo. La página renderiza la primera página del documento y superpone una capa de efectos con Hydra-synth, ideal para resaltar pasos importantes o experimentar con anotaciones visuales.

1. Inicia el servidor como en el paso anterior.
2. Abre `http://localhost:8000/pdf_overlay.html`.
3. Selecciona un PDF local desde el control "Cargar PDF".

El efecto Hydra se puede modificar editando el código de la página para ajustar colores y animaciones.

### Capturas de pantalla

Si deseas guardar una imagen de tu escritorio para documentar tus experimentos, utiliza el script `screenshot.py`:

```bash
pip install pyautogui colorama
python3 screenshot.py --tag prueba
```

Las capturas se guardarán en la carpeta `screenshots` y el mensaje aparecerá resaltado en azul para mayor claridad.
