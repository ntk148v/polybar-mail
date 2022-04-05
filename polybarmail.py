import argparse
import configparser
import imaplib
from pathlib import Path
import subprocess
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument(
    '--config', default=f'{Path.home()}/.config/polybar/mail.ini')
parser.add_argument('-p', '--prefix', default='\uf0e0')
parser.add_argument('-c', '--color', default='#e06c75')
parser.add_argument('-ns', '--nosound', action='store_true')
args = parser.parse_args()

unread_prefix = '%{F' + args.color + '}' + args.prefix + ' %{F-}'
error_prefix = '%{F' + args.color + '}\uf06a %{F-}'
count_was = 0

print(args.config)

# Parse config file
if not Path(args.config).is_file():
    print(error_prefix + f'config file {args.config} not found', flush=True)
    sys.exit(1)
config = configparser.ConfigParser()
config.read(args.config)

try:
    mail_protocol = config['default']['mail_protocol']
    mail_server = config['default']['mail_server']
    mail_port = config['default']['mail_port']
    mail_username = config['default']['mail_username']
    mail_password = config['default']['mail_password']
    mail_box = config['default']['mail_box']
except KeyError as e:
    print(error_prefix + f'wrong config: {str(e)}', flush=True)
    sys.exit(1)


def print_count(count, is_odd=False):
    tilde = '~' if is_odd else ''
    output = ''
    if count > 0:
        output = unread_prefix + tilde + str(count)
    else:
        output = (args.prefix + ' ' + tilde).strip()
    print(output, flush=True)


def update_count(count_was):
    # Connect to mail server
    typ = data = None
    if mail_protocol.upper() == 'IMAP':
        imap = imaplib.IMAP4_SSL(mail_server, mail_port)
        imap.login(mail_username, mail_password)
        imap.select(mailbox=mail_box)
        typ, data = imap.search(None, '(Unseen)')
    else:
        raise Exception(f'Unsupported mail protocol: {mail_protocol}')
    if typ != 'OK':
        raise Exception(f'Search command return {typ}')
    count = len(data[0].split())
    print_count(count)
    if not args.nosound and count_was < count and count > 0:
        subprocess.run(['canberra-gtk-play', '-i', 'message'])
    return count


print_count(0, True)

while True:
    try:
        count_was = update_count(count_was)
        time.sleep(30)
    except Exception as e:
        print(error_prefix + f'something went wrong: {str(e)}', flush=True)
        sys.exit(1)
