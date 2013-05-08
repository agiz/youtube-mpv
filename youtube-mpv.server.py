# starts mplayer
# http://127.0.0.1:9000/p?i=youtube_url

import subprocess, urlparse
import SimpleHTTPServer, SocketServer

CACHE = '1024'
PLAYER = 'mpv'
PORT = 9000

class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        parsedParams = urlparse.urlparse(self.path)
        yt_url = parsedParams.query[2:]

        subprocess.Popen(
            [PLAYER, '-really-quiet', '-cache', CACHE, '-af', 'channels=4:4:0:2:0:0:1:3:1:1', yt_url],
            stdout=subprocess.PIPE,
        )

        self.send_response(204)

Handler = MyHandler
httpd = SocketServer.TCPServer(('', PORT), Handler)
print 'serving at port', PORT
httpd.serve_forever()
