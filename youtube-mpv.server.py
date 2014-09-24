# starts mplayer
# http://127.0.0.1:9000/p?i=youtube_url

import subprocess, urlparse
import SimpleHTTPServer, SocketServer

CACHE = '1024'
PLAYER = 'mpv'
PORT = 9000

#youtube-dl -o - https://www.youtube.com/watch\?v\=u_VnHAy1Vdc | mpv - -cache 8192 -cache-min 30

class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        parsedParams = urlparse.urlparse(self.path)
        parsed_query = urlparse.parse_qs(parsedParams.query)
        #print parsed_query
        yt_url = parsed_query['i'][0]
        #yt_url = parsedParams.query[2:]
        #print yt_url

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
            ['youtube-dl', '-g', yt_url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        ).communicate()
        """Returns video location url."""

        video_url = stdout.strip()

        subprocess.Popen(
            ['mpv', '--vo=opengl-hq', '--no-border', video_url],
            stdout=subprocess.PIPE
        )

        self.send_response(204)

Handler = MyHandler
httpd = SocketServer.TCPServer(('', PORT), Handler)
print 'serving at port', PORT
httpd.serve_forever()
