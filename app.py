from flask import Flask, request, jsonify
import os
import youtube_dl

app = Flask(__name__)

def download_video(url, format='mp4'):
    ydl_opts = {
        'format': 'bestvideo+bestaudio' if format == 'mp4' else 'bestaudio',
        'outtmpl': f'/tmp/{url.split("=")[-1]}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if format == 'mp3' else []
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        return f'{url.split("=")[-1]}.{format}'

@app.route('/convert', methods=['POST'])
def convert_video():
    try:
        data = request.get_json()
        url = data['url']
        format = data['format']
        
        file_name = download_video(url, format)
        return jsonify({'success': True, 'file': file_name})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
