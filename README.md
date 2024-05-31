

# YouTube Video Downloader

Esta es una aplicación web desarrollada con Flask que permite a los usuarios descargar videos individuales o listas de reproducción de YouTube. Los videos se descargan en el servidor y luego se proporcionan para que los usuarios los descarguen en sus dispositivos locales.

## Características

- Descargar videos individuales de YouTube.
- Descargar listas de reproducción completas de YouTube.
- Los archivos se eliminan del servidor automáticamente después de ser descargados por el usuario.

## Requisitos

- Python 3.7+
- Flask
- pytube
- platformdirs

## Instalación

1. Clona este repositorio:


git clone https://github.com/Theminox/YoutubeDownloader_Flask.git

cd YoutubeDownloader_Flask


2. Crea un entorno virtual y activa:


python -m venv venv
source venv/bin/activate  # En Windows usa `venv\Scripts\activate`


3. Instala las dependencias:


pip install -r requirements.txt


## Uso

1. Ejecuta la aplicación:


python app.py


2. Abre tu navegador y ve a `http://localhost:5000`.

3. Introduce la URL del video o lista de reproducción de YouTube que deseas descargar y haz clic en "Descargar".

4. Una vez completada la descarga, serás redirigido a una página donde podrás descargar el archivo a tu dispositivo. El archivo se eliminará automáticamente del servidor después de la descarga.

## Estructura del Proyecto

```
YoutubeDownloader_Flask/
│
├── downloads/               # Directorio donde se almacenan temporalmente los videos descargados
├── templates/
│   ├── index.html           # Página principal
│   └── downloads.html       # Página de descarga
├── app.py                   # Archivo principal de la aplicación Flask
├── requirements.txt         # Lista de dependencias del proyecto
└── README.md                # Este archivo
```

## Contribuir

1. Haz un fork del proyecto.
2. Crea una rama para tu nueva característica (git checkout -b feature/nueva-caracteristica).
3. Haz commit de tus cambios (git commit -am 'Agrega nueva característica').
4. Sube tus cambios a la rama (git push origin feature/nueva-caracteristica).
5. Abre un Pull Request.

## Creado por
Este proyecto fue creado por **Minoxrex**.

Este archivo README proporciona la guía completa para los usuarios y desarrolladores,


