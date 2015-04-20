# starts mplayer
# http://127.0.0.1:9000/p?i=youtube_url
from urllib.parse import urlparse, parse_qs
import subprocess, socketserver
import http.server

CACHE = '1024'
PLAYER = 'mpv'
PORT = 9000

class MyHandler(http.server.SimpleHTTPRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        parsedParams = urlparse(self.data)
        parsed_query = parse_qs(parsedParams.query, encoding='utf-8', errors='replace')

        # print(parsed_query[b'i'])
        yt_url = str(parsed_query[b'i'][0])[2:-1]
        print(yt_url)

        #subprocess.Popen(
        #    #[PLAYER, '-really-quiet', '--vo=opengl-hq', '--no-border', yt_url],
        #    ['youtube-dl -o -', yt_url, '| mpv - -cache 1024 0cache-min 30'],
        #    stdout=subprocess.PIPE,
        #)
        #subprocess.check_output("youtube-dl -o - " + yt_url + " | mpv - -cache 8192 --vo=opengl-hq --no-border", shell=True)
        #subprocess.check_output("youtube-dl -o - " + yt_url + " | mpv - -cache 1024 --vo=opengl-hq --no-border", shell=True)
        #subprocess.check_output("youtube-dl -o - " + yt_url + " | /usr/local/Cellar/mpv/0.3.11/bin/mpv - -cache 1024 -cache-min 30 --vo=opengl-hq --no-border", shell=True)

        #subprocess.check_output("youtube-dl -o - " + yt_url + " | mpv - --cache=2048 --cache-initial=512 --vo=opengl-hq --no-border", shell=True)
        """Use this is ffmpeg is compiled without openssl."""

        stdout, stderr = subprocess.Popen(
            ['./youtube-dl', '-g', yt_url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        ).communicate()

        """Returns video location url."""

        video_url = stdout.strip()
        mpv = ['mpv', '--vo=opengl-hq', '--no-border', video_url.decode('utf-8')]

        with subprocess.Popen(mpv) as proc:
            log.write(proc.stdout.read())

        self.send_response(204)

Handler = MyHandler
httpd = socketserver.TCPServer(('', PORT), Handler)
print('serving at port', PORT)
httpd.serve_forever()
