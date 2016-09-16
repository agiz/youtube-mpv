#!/usr/bin/env python
from __future__ import print_function

import os
import subprocess
import sys

# http://stackoverflow.com/a/1660073/2257038
if sys.version_info.major == 2:
    from BaseHTTPServer import HTTPServer as HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler as RequestHandler
    import SocketServer
    import urlparse as parse
    from distutils.spawn import find_executable as which
else:
    from http.server import HTTPServer
    from http.server import SimpleHTTPRequestHandler as RequestHandler
    import socketserver as SocketServer
    from urllib import parse
    from shutil import which

# Check https://github.com/rg3/youtube-dl/
import youtube_dl

# PORT, HOST, PLAYER and OPTS variables
import ytdl_config

# used for redirecting stdout, stderr
FNULL = open(os.devnull, 'w')

y = youtube_dl.YoutubeDL({
    'quiet': True,
    'nocheckcertificate': True,
    'logger': None,
    'age_limit': None,
    'forcejson': True
    })

def report_error(summary, message=""):
    print(summary + ': ' + message)
    # http://stackoverflow.com/a/12611523/2257038
    if not ytdl_config.NOTIFY_COMMAND == '' and which(ytdl_config.NOTIFY_COMMAND):
        subprocess.Popen([ytdl_config.NOTIFY_COMMAND, "YoutubeDL mpv: " + summary, message])
    else:
        print("Error: NOTIFY_COMMAND is unset, or does not exist")

class MyHandler(RequestHandler):
    """
    Perform video lookup using youtube-dl
    """

    def match_id(self, url):
        data = False
        try:
            data = y.extract_info(url, download=False)
        except youtube_dl.DownloadError:
            return False
        return data

    def do_GET(self):
        """
        Given a request, grab the URI for the video, and then play it through
        the user's specified PLAYER
        """
        parsedParams = parse.urlparse(self.path)
        parsed_query = parse.parse_qs(parsedParams.query)
        yt_url = parsed_query['i'][0]

        data = self.match_id(yt_url)
        if not data:
            report_error("No file found", "No file found for " + yt_url)
            return self.send_response(400)

        video_url = ''
        if 'url' in data:
            # Non-youtube video?
            video_url = data['url']
        else:
            # youtube video
            video_url_lo = ''
            video_url_hi = ''
            start_time = 0
            for format_id in data['formats']:
                if 'format_id' in format_id and format_id['format_id'] == '22':
                    video_url_hi = format_id['url']
                elif 'format_id' in format_id and format_id['format_id'] == '18':
                    video_url_lo = format_id['url']

            if video_url_hi == '':
                if video_url_lo == '':
                    report_error('Unknown format', 'Cannot play video from' + yt_url)
                    return self.send_response(400)
                video_url = video_url_lo
            else:
                video_url = video_url_hi
            if 'start_time' in data and data['start_time'] is not None:
                start_time = int(float(data['start_time']))

        # Get additional options
        command = list(map(str, ytdl_config.OPTS.split(' ')))

        # Prepend default player
        command.insert(0, ytdl_config.PLAYER)
        
        # Append start time option
        if start_time and start_time != 0:
            command.append('--start=+' + str(start_time))

        # Append video url
        command.append(video_url)

        subprocess.Popen(
                command,
                stdout=FNULL,
                stderr=FNULL
                )

        self.send_response(204)

    def log_message(self, format, *args):
        """
        Disable debug output.
        """
        return


def serve(host, port, HandlerClass=MyHandler,
          ServerClass=HTTPServer):
    protocol = 'HTTP/1.0'
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if ':' in arg:
            host, port = arg.split(':')
            port = int(port)
        else:
            try:
                port = int(sys.argv[1])
            except:
                host = sys.argv[1]

    server_address = (host, port)

    HandlerClass.protocol_version = protocol
    httpd = ThreadedHTTPServer(server_address, HandlerClass)

    sa = httpd.socket.getsockname()
    print('Serving HTTP on', sa[0], 'port', sa[1], '...')
    httpd.serve_forever()


class ThreadedHTTPServer(SocketServer.ThreadingMixIn,
                         HTTPServer):
    """
    This class allows to handle requests in separated threads. No further
    content needed, don't touch this.
    """

if __name__ == "__main__":
    serve(ytdl_config.HOST, ytdl_config.PORT)
