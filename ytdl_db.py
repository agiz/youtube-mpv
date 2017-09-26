import os
import sqlite3
import time

class VideoDB(object):

  def init_database(self):
    print('Initializing database ...')

    self.con = sqlite3.connect(
      os.path.join(os.path.dirname(os.path.realpath(__file__)), 'history.db'),
      detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES,
      check_same_thread=False
    )
    self.c = self.con.cursor()

    self.c.execute(
      'PRAGMA foreign_keys = ON'
    )

    self.c.execute(
      '''
      CREATE TABLE IF NOT EXISTS format(
        id INTEGER PRIMARY KEY,
        format_name TEXT NOT NULL UNIQUE ON CONFLICT IGNORE
      )
      '''
    )

    self.c.execute(
      '''
      CREATE TABLE IF NOT EXISTS video(
        id INTEGER PRIMARY KEY,
        download_date REAL,
        extractor TEXT,
        video_id TEXT,
        webpage_url TEXT,
        title TEXT,
        description TEXT,
        thumbnail TEXT,
        duration INTEGER
      )
      '''
    )

    self.c.execute(
      '''
      CREATE TABLE IF NOT EXISTS video_format(
        id INTEGER PRIMARY KEY,
        video_id INTEGER,
        format_id INTEGER,
        FOREIGN KEY (video_id) REFERENCES video(id),
        FOREIGN KEY (format_id) REFERENCES format(id)
      )
      '''
    )


    self.c.execute(
      '''
      CREATE UNIQUE INDEX IF NOT EXISTS extractor_id_index ON video (
        extractor,
        video_id
      )
      '''
    )
    self.con.commit()

  def insert(self, extractor, video_id, webpage_url,
             title, description, thumbnail, duration, format):

    download_date = time.time() * 1000

    try:
      self.c.execute(
        '''
        INSERT INTO video(
          download_date,
          extractor,
          video_id,
          webpage_url,
          title,
          description,
          thumbnail,
          duration
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (download_date, extractor, video_id, webpage_url,
         title, description, thumbnail, duration,)
      )
    except sqlite3.IntegrityError:
      self.c.execute(
        'UPDATE video SET download_date=? WHERE extractor=? AND video_id=?',
        (download_date, extractor, video_id,)
      )
      return

    lastrow = self.c.lastrowid

    self.c.execute(
      '''
      INSERT INTO format(format_name)
      SELECT ? WHERE NOT EXISTS(SELECT id FROM format WHERE format_name=?)
      ''',
      (format, format,)
    )

    self.c.execute(
      'SELECT id FROM format WHERE format_name=?', (format,)
    )
    format_id = self.c.fetchone()
    format_id = format_id[0]

    self.c.execute(
      'INSERT INTO video_format(video_id, format_id) VALUES (?, ?)',
      (lastrow, format_id,)
    )

    self.con.commit()

    return lastrow

  def get_videos(self, offset, count):
    print 'get_videos'
    self.c.execute(
      '''
      SELECT
        id,
        download_date,
        extractor,
        video_id,
        webpage_url,
        title,
        description,
        thumbnail,
        duration
      FROM video
      ORDER BY download_date DESC
      LIMIT (%s), (%s)
      ''' %
      (offset, count)
    )
    return self.c.fetchall()

  def get_formats(self):
    self.c.execute(
      'SELECT id, format_name FROM format ORDER BY id ASC'
    )
    return self.c.fetchall()

  def get_videos_formats(self):
    self.c.execute(
      '''
      SELECT
        video_id,
        format_id
      FROM video_format
      ORDER BY video_id, format_id ASC
      '''
    )
    return self.c.fetchall()

  def delete_video(self, ids):
    self.c.execute(
      'DELETE FROM video_format WHERE video_id IN (%s)' %
      (','.join(ids))
    )

    self.c.execute(
      'DELETE FROM video WHERE id IN (%s)' %
      (','.join(ids))
    )
    self.con.commit()

  def delete_all(self, ids):
    self.c.execute(
      'DELETE * FROM video_format'
    )

    self.c.execute(
      'DELETE * FROM video'
    )
    self.con.commit()
