# ytdl server

Chrome extension and Firefox add-on that adds context menu option to play youtube videos with mpv (or other external player).

## Requirements

1. Chrome like/Firefox browser.
2. python2 or python3
3. [youtube\_dl module](http://rg3.github.io/youtube-dl)
4. [mpv](http://mpv.io) or similar

## Installation

### Server side:

#### Arch Linux

Install the AUR package, [`youtube-mpv-git`](https://aur.archlinux.org/packages/youtube-mpv-git).

#### systemd unit files

In order to install the server with systemd, you will need to copy

- `youtube-mpv.service` to `/etc/systemd/user/youtube-mpv.service`

Then you can install it with:

```
$ systemctl --user <enable|start> youtube-mpv.service
```

**Note**: these unit files assume `ytdl_server.py` is installed at
`/opt/youtube-mpv-git/ytdl_server.py`. You will need to amend the paths if you
have installed it elsewhere.

#### Ubuntu

```
./install-ubuntu.sh
```

make sure you don't run this script as root (without sudo)


**Note: ** for playlist support add <code>ytdl-raw-options=yes-playlist=</code>
to your <code>mpv.conf</code> file.


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

### Receive native notifications on errors

Modify `ytdl_config.py` to set the `NOTIFY_COMMAND` to a command, such as
`notify-send` on Linux to provide native notifications when a video cannot be
found.

## How does it work

Whenever 'Play with mpv' is selected in browser,
url `http://127.0.0.1:9000/p?i=<youtube_url>` is
sent to listening server. Server checks if url is
supported, extracts video url and starts player.

## Credits

[agiz](https://github.com/agiz), [dcrystalj](https://github.com/dcrystalj), [ihavenoface](https://github.com/ihavenoface), [jamietanna](https://github.com/jamietanna)

## License

[GPLv2](https://github.com/agiz/youtube-mpv/blob/master/LICENSE)
