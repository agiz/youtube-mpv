#!/usr/bin/env python
from __future__ import print_function

import json
import os
import signal
import subprocess
import sys
import threading

# http://stackoverflow.com/a/1660073/2257038
if sys.version_info.major == 2:
  from BaseHTTPServer import HTTPServer as HTTPServer
  from SimpleHTTPServer import SimpleHTTPRequestHandler as RequestHandler
  # from BaseHTTPServer import BaseHTTPRequestHandler as RequestHandler
  import SocketServer
  import urlparse as parse
  from distutils.spawn import find_executable as which
else:
  from http.server import HTTPServer
  from http.server import SimpleHTTPRequestHandler as RequestHandler
  # from http.server import BaseHTTPRequestHandler as RequestHandler
  import socketserver as SocketServer
  from urllib import parse
  from shutil import which

# Check https://github.com/rg3/youtube-dl/
# import youtube_dl

# PORT, HOST, PLAYER and OPTS variables
import ytdl_config

from ytdl_db import VideoDB

# used for redirecting stdout, stderr
FNULL = open(os.devnull, 'w')

# y = youtube_dl.YoutubeDL({
#   'quiet': True,
#   'nocheckcertificate': True,
#   'logger': None,
#   'age_limit': None,
#   'forcejson': True
# })

def report_error(summary, message=""):
  print(summary + ': ' + message)
  # http://stackoverflow.com/a/12611523/2257038
  if not ytdl_config.NOTIFY_COMMAND == '' and which(ytdl_config.NOTIFY_COMMAND):
    subprocess.Popen([
      ytdl_config.NOTIFY_COMMAND,
      "YoutubeDL mpv: " + summary,
      message,
    ])
  else:
    print("Error: NOTIFY_COMMAND is unset, or does not exist")

class MyHandler(RequestHandler):
  """
  Perform video lookup using youtube-dl
  """

  def match_id(self, url):
    data = False
    # try:
    #   data = y.extract_info(url, download=False)
    # except youtube_dl.DownloadError:
    #   return False
    return data

  def do_GET(self):
    """
    Given a request, grab the URI for the video, and then play it through
    the user's specified PLAYER
    """
    parsedParams = parse.urlparse(self.path)
    parsed_query = parse.parse_qs(parsedParams.query)

    if 'g' in parsed_query:
      # msg = b'var video_arr = ' + json.dumps(vdb.get_videos(0, 100)).encode() + b';' + b'var format_arr = ' + json.dumps(vdb.get_formats()).encode() + b';' + b'var video_format_arr = ' + json.dumps(vdb.get_videos_formats()).encode() + b';'
      msg = json.dumps({
        'videos': vdb.get_videos(0, 100),
        'formats': vdb.get_formats(),
        'videoFormats': vdb.get_videos_formats(),
      }).encode()
      self.send_response(200)
      self.send_header('Content-type', 'application/json; charset=utf-8')
      self.send_header('Content-Length', len(msg))
      self.end_headers()

      return self.wfile.write(msg)
    elif 'i' in parsed_query:
      yt_url = parsed_query['i'][0]
    #
    # here comes delete videos logic...
    #
    else:
      return self.send_response(204)

    data = self.match_id(yt_url)
    if not data:
      report_error("No file found", "No file found for " + yt_url)
      return self.send_response(400)

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
          report_error('Unknown format', 'Cannot play video from' + yt_url)
          return self.send_response(400)
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

    vdb.insert(extractor, video_id, webpage_url,
               title, description, thumbnail, duration, format)

    self.send_response(204)

  def log_message(self, format, *args):
    """
    Disable debug output.
    """
    return


class SimpleHTTPServer():
  def __init__(self, ip, port):
    self.server = ThreadedHTTPServer((ip, port), MyHandler)

  def start(self):
    try:
      self.server_thread = threading.Thread(target=self.server.serve_forever)
      # self.server_thread.daemon = True
      self.server_thread.start()
      signal.pause() # not supported on windows; use: while True: time.sleep(100)
      # or: while thread.isAlive(): thread.join(1)  # not sure if there is an appreciable cost to this.
    except (KeyboardInterrupt, SystemExit):
      self.stop()

  def waitForThread(self):
    self.server_thread.join()

  def addRecord(self, recordID, jsonEncodedRecord):
    LocalData.records[recordID] = jsonEncodedRecord

  def stop(self):
    print('stopping...')
    self.server.shutdown()
    self.waitForThread()

class ThreadedHTTPServer(SocketServer.ThreadingMixIn, HTTPServer):
  """
  This class allows to handle requests in separated threads. No further
  content needed, don't touch this.
  """
  allow_reuse_address = True

  def shutdown(self):
    print('shutting down...')
    self.socket.close()
    HTTPServer.shutdown(self)

if __name__ == "__main__":
  vdb = VideoDB()
  vdb.init_database()
  server = SimpleHTTPServer(ytdl_config.HOST, 9001)
  print('Server is running...')
  server.start()
  server.waitForThread()
