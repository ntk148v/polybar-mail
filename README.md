# Polybar Mail

 A [Polybar](https://github.com/jaagr/polybar) module to show unread messages from mail inspired by [polybar-gmail](https://github.com/crabvk/polybar-gmail).

## Dependencies

 - **Font Awesome** - default email icon.
- **canberra-gtk-play** - new email sound notification (optional).

## Installation

- Get polybarmail

```bash
git clone http://github.com/ntk148v/polybar-mail.git
cp polybarmail.py ~/.config/polybar/polybarmail.py
cp mail.ini ~/.config/polybar/mail.ini
# Modify mail.ini with your mail configuration
```

- Scripts arguments

```bash
usage: polybarmail.py [-h] [--config CONFIG] [-p PREFIX] [-c COLOR] [-ns]

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG
  -p PREFIX, --prefix PREFIX
  -c COLOR, --color COLOR
  -ns, --nosound
```

- Update polybar config

```ini
[module/mail]
type = custom/script
exec = ~/.config/polybar/polybarmail.py
tail = true
click-left = xdg-open https://<your-mail-website>
```
