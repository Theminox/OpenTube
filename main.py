from flask import Flask, request, render_template, redirect, url_for, flash, send_file, after_this_request
import os
from pytube import Playlist, YouTube
import platformdirs

app = Flask(__name__)
app.secret_key = '2133223142556753412'  

DOWNLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def get_download_path():
    return DOWNLOAD_FOLDER

def download_youtube_video(video_url, download_path):
    try:
        app.logger.info(f'Descargando video: {video_url}')
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()
        file_path = stream.download(output_path=download_path)
        app.logger.info(f'Descargado: {yt.title}')
        return file_path
    except Exception as e:
        app.logger.error(f'Error al descargar {video_url}: {e}')
        return None

def download_youtube_playlist(playlist_url, download_path):
    playlist = Playlist(playlist_url)
    app.logger.info(f'Descargando la lista de reproducción: {playlist.title}')
    app.logger.info(f'Número de videos en la lista: {len(playlist.video_urls)}')

    file_paths = []
    for url in playlist.video_urls:
        file_path = download_youtube_video(url, download_path)
        if file_path:
            file_paths.append(file_path)
    return file_paths

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    download_path = get_download_path()
    
    if "playlist" in url.lower():
        file_paths = download_youtube_playlist(url, download_path)
    else:
        file_path = download_youtube_video(url, download_path)
        file_paths = [file_path] if file_path else []

    if file_paths:
        flash('Descarga completada. Los archivos se descargarán automáticamente.')
        
        return redirect(url_for('download_file', filename=os.path.basename(file_paths[0])))
    else:
        flash('Error al descargar los videos.')
        return redirect(url_for('index'))

@app.route('/downloads/<filename>')
def download_file(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        flash('El archivo no se encuentra en el servidor.')
        return redirect(url_for('index'))

    @after_this_request
    def remove_file(response):
        try:
            os.remove(file_path)
            app.logger.info(f'Archivo {filename} eliminado.')
        except Exception as error:
            app.logger.error(f'Error al eliminar el archivo {filename}: {error}')
        return response

    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
