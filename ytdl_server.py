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
else:
    from http.server import HTTPServer
    from http.server import SimpleHTTPRequestHandler as RequestHandler
    import socketserver as SocketServer
    from urllib import parse

import youtube_dl
"""Check https://github.com/rg3/youtube-dl/"""

import ytdl_config
"""PORT, HOST, PLAYER and OPTS variables."""

FNULL = open(os.devnull, 'w')
"""/dev/null"""

y = youtube_dl.YoutubeDL({
  'quiet': True,
  'nocheckcertificate': True,
  'logger': None,
  'age_limit': None,
  'forcejson': True
})
"""youtube_dl handle"""

class MyHandler(RequestHandler):

  def match_id(self, url):
    data = False
    try:
      data = y.extract_info(url, download=False)
    except youtube_dl.DownloadError:
      return False
    return data

  def do_GET(self):
    parsedParams = parse.urlparse(self.path)
    parsed_query = urlparse.parse_qs(parsedParams.query)
    yt_url = parsed_query['i'][0]

    data = self.match_id(yt_url)
    if data == False:
      return self.send_response(204)

    video_url = ''
    if 'url' in data:
      """Non-youtube video?"""
      video_url = data['url']
    else:
      """youtube video"""
      video_url_lo = ''
      video_url_hi = ''
      for format_id in data['formats']:
        if 'format_id' in format_id and format_id['format_id'] == '22':
          video_url_hi = format_id['url']
        elif 'format_id' in format_id and format_id['format_id'] == '18':
          video_url_lo = format_id['url']
      if video_url_hi == '':
        if video_url_lo == '':
          print('Unknown format. Cannot play video from:', yt_url)
          return self.send_response(204)
        video_url = video_url_lo
      else:
        video_url = video_url_hi

    command = map(str, ytdl_config.OPTS.split(' '))
    """Get additional options."""

    command.insert(0, ytdl_config.PLAYER)
    """Prepend default player."""

    command.append(video_url)
    """Append video url."""

    subprocess.Popen(
      command,
      stdout=FNULL,
      stderr=FNULL
    )

    self.send_response(204)

  def log_message(self, format, *args):
    """Disable debug output."""
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
  """This class allows to handle requests in separated threads.
    No further content needed, don't touch this."""

if __name__ == "__main__":
  serve(ytdl_config.HOST, ytdl_config.PORT)
