import subprocess

def Sound(data):
    if data == 'up':
        subprocess.call(['notify-send', 'Hello'])
        print('upp')
    if data == 'down':
        subprocess.call(['pactl', 'set-sink-volume', '0', '-15%'])
    if data == 'set':
        subprocess.call(['pactl', 'set-sink-volume', '0', '+15%'])