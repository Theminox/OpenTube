from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory
import os
from pytube import Playlist, YouTube
import platformdirs

app = Flask(__name__)
app.secret_key = '2133223142556753412'  # Necesario para usar flash messages

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
        stream.download(output_path=download_path)
        app.logger.info(f'Descargado: {yt.title}')
        return yt.title
    except Exception as e:
        app.logger.error(f'Error al descargar {video_url}: {e}')
        return None


def download_youtube_playlist(playlist_url, download_path):
    playlist = Playlist(playlist_url)
    app.logger.info(f'Descargando la lista de reproducción: {playlist.title}')
    app.logger.info(f'Número de videos en la lista: {len(playlist.video_urls)}')

    titles = []
    for url in playlist.video_urls:
        title = download_youtube_video(url, download_path)
        if title:
            titles.append(title)
    return titles


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    download_path = get_download_path()

    if "playlist" in url.lower():
        titles = download_youtube_playlist(url, download_path)
    else:
        title = download_youtube_video(url, download_path)
        titles = [title] if title else []

    if titles:
        flash(f'Descargado: {", ".join(titles)}')
        # Redirige a la ruta para descargar los archivos
        return redirect(url_for('list_downloads'))
    else:
        flash('Error al descargar los videos.')
        return redirect(url_for('index'))


@app.route('/downloads')
def list_downloads():
    files = os.listdir(DOWNLOAD_FOLDER)
    return render_template('downloads.html', files=files)


@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=True)
