# This script allows you to replace a given tracker on current torrents. It was made for qbittorent V4.1.9.1 on windows and will need to be adapted for another torrent client and / or operating system.
# Copyright (C) 2019  Antoine Rozec

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os
import sys

def main():
    try:
        import bencode
    except ModuleNotFoundError:
        print("The bencode.py module is needed, you can install it with this command: 'pip install bencode.py'.")
        exitProgram(1)
    if 'qbittorrent.exe' in os.popen('tasklist').detach().read().decode(encoding='cp437'):
        print('Please close qBittorrent before using this program.')
        exitProgram(1)
    print('QbTrackerUpdater - for qBittorent on windows\ntype in the tracker to be replaced, then the one to replace it with.\nRight-clic to paste in shell.\n')
    source = input('old tracker : ')
    target = input('new tracker : ')
    print('\n')
    workDir = os.environ['LOCALAPPDATA'] + '\\qBittorrent\\BT_backup'
    files = [f for f in os.listdir(workDir) if '.fastresume' in f]
    for f in files:
        path = workDir + '\\' + f
        with open(path, 'rb') as fd:
            data = bencode.decode(fd.read())
        for i, t in enumerate(data['trackers']):
            if t[0] == source:
                data['trackers'][i][0] = target
                print('tracker replaced in: %s' % f)
        with open(path, 'wb') as fd:
            fd.write(bencode.encode(data))
    print('\nDone.')
    exitProgram(0)

def exitProgram(code):
    os.system('pause')
    sys.exit(code)

if __name__ == '__main__':
	main()