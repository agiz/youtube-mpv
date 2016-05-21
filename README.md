# ytdl server

Chrome extension and Firefox add-on that adds context menu option to play youtube videos with mpv (or other external player).

## Requirements

1. Chrome like/Firefox browser.
2. python2 or python3
3. [youtube\_dl module](http://rg3.github.io/youtube-dl)
4. [mpv](http://mpv.io) or similar

## Installation

### Server side:
#### Ubuntu

```
./install-ubuntu.sh
```

make sure you don't run this script as root (without sudo)


### Client side (browser):

1. chrome://extensions/
2. tick Developer mode
3. Load unpacked extension...
4. Choose chrome directory of this project.

## Usage

1. Navigate to script's directory.
2. Run `python ytdl_server.py`.

## Configuration

### Change port, host or player, player options

Modify `ytdl_config.py` file.

General (mpv) player options should be set (usually) in
`~/.config/mpv/config`. Specific options like provided
`--no-terminal` should be put in `OPTS` variable and
separated with space ie: `--no-terminal --screen 1`.

## How does it work

Whenever 'Play with mpv' is selected in browser,
url `http://127.0.0.1:9000/p?i=<youtube_url>` is
sent to listening server. Server checks if url is
supported, extracts video url and starts player.

## Credits

[agiz](https://github.com/agiz), [dcrystalj](https://github.com/dcrystalj), [ihavenoface](https://github.com/ihavenoface)

## License

[GPLv2](https://github.com/agiz/youtube-mpv/blob/master/LICENSE)
