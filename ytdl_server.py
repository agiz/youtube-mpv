#!/usr/bin/env python
from __future__ import print_function

import json
import os
import subprocess
import sys

# http://stackoverflow.com/a/1660073/2257038
if sys.version_info.major == 2:
    from BaseHTTPServer import HTTPServer as HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler as RequestHandler
    import SocketServer
    import urlparse as parse
else:
    from http.server import HTTPServer
    from http.server import SimpleHTTPRequestHandler as RequestHandler
    import socketserver as SocketServer
    from urllib import parse

# Check https://github.com/rg3/youtube-dl/
import youtube_dl

# PORT, HOST, PLAYER and OPTS variables
import ytdl_config

from ytdl_db import VideoDB

# used for redirecting stdout, stderr
FNULL = open(os.devnull, 'w')

y = youtube_dl.YoutubeDL({
    'quiet': True,
    'nocheckcertificate': True,
    'logger': None,
    'age_limit': None,
    'forcejson': True
    })


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

        if 'g' in parsed_query:
            return self.wfile.write(
                'var video_arr = ' + json.dumps(vdb.get_videos()) + ';' +
                'var format_arr = ' + json.dumps(vdb.get_formats()) + ';' +
                'var video_format_arr = ' + json.dumps(vdb.get_videos_formats()) + ';'
                )
        elif 'i' in parsed_query:
            yt_url = parsed_query['i'][0]
        else:
            return self.send_response(204)

        data = self.match_id(yt_url)
        if not data:
            return self.send_response(204)

        format = ''
        video_url = ''
        if 'url' in data:
            # Non-youtube video?
            video_url = data['url']
            if 'format' in data:
                format = data['format']
        elif 'formats' in data:
            # youtube video
            video_url_lo = ''
            video_url_hi = ''
            for format_id in data['formats']:
                if 'format_id' in format_id and format_id['format_id'] == '22':
                    video_url_hi = format_id['url']
                    format = format_id['format']
                    break
                elif 'format_id' in format_id and format_id['format_id'] == '18':
                    video_url_lo = format_id['url']
                    format = format_id['format']
            if video_url_hi == '':
                if video_url_lo == '':
                    print('Unknown format. Cannot play video from:', yt_url)
                    return self.send_response(204)
                video_url = video_url_lo
            else:
                video_url = video_url_hi
        else:
            return self.send_response(204)

        # Get additional options
        command = list(map(str, ytdl_config.OPTS.split(' ')))

        # Prepend default player
        command.insert(0, ytdl_config.PLAYER)

        # Append video url
        command.append(video_url)

        subprocess.Popen(
                command,
                stdout=FNULL,
                stderr=FNULL
                )

        duration = -1
        title = ''
        description = ''
        thumbnail = ''
        extractor = ''
        video_id = ''
        webpage_url = ''

        if 'duration' in data:
          duration = data['duration']
        if 'title' in data:
          title = data['title']
        if 'description' in data:
          description = data['description']
        if 'thumbnail' in data:
          thumbnail = data['thumbnail']
        if 'extractor' in data:
          extractor = data['extractor']
          extractor = extractor.lower()
        if 'id' in data:
          video_id = data['id']
        if 'webpage_url' in data:
          webpage_url = data['webpage_url']

        vdb.insert(extractor, video_id, webpage_url, title, description,
                   thumbnail, duration, format)

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
    vdb = VideoDB()
    vdb.init_database()
    serve(ytdl_config.HOST, ytdl_config.PORT)
