from flask import Flask, request, render_template, redirect, url_for, flash
import os
from pytube import Playlist, YouTube
import platformdirs

app = Flask(__name__)
app.secret_key = '2133223142556753412'  # Necesario para usar flash messages

def get_download_path():
    return platformdirs.user_downloads_dir()

def download_youtube_video(video_url, download_path):
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    try:
        print(f'Descargando video: {video_url}')
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=download_path)
        print(f'Descargado: {yt.title}')
        return f'Descargado: {yt.title}'
    except Exception as e:
        print(f'Error al descargar {video_url}: {e}')
        return f'Error al descargar {video_url}: {e}'

def download_youtube_playlist(playlist_url, download_path):
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    playlist = Playlist(playlist_url)

    print(f'Descargando la lista de reproducción: {playlist.title}')
    print(f'Número de videos en la lista: {len(playlist.video_urls)}')

    results = []
    for url in playlist.video_urls:
        result = download_youtube_video(url, download_path)
        results.append(result)
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    download_path = get_download_path()

    if "playlist" in url.lower():
        results = download_youtube_playlist(url, download_path)
    else:
        result = download_youtube_video(url, download_path)
        results = [result]

    flash('\n'.join(results))
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
