from platform import architecture
from sys import argv
from requests import get
import json
from dl import dlfile

try:
  snap_name = argv[1]
except:
  raise 'python3 -m snap-downloader.py [SNAPNAME] [ARCHITECTURE]'

if len(argv) < 3:
  arch = 'amd64'
else:
  arch = argv[1]

snap_api_uri = 'https://api.snapcraft.io/v2/snaps/info/' + snap_name
outfile_name = snap_name + '_' + arch + '.snap'

headers = {'Accept':'application/json', 'Snap-Device-Series':'16'}
snap_uri = get(snap_api_uri, headers=headers)
snap_obj = json.loads(snap_uri.text)
chanmap = snap_obj['channel-map']
found = 0

for idx, x in enumerate(chanmap):
   if chanmap[idx]['channel']['risk'] == 'stable':
    if str(chanmap[idx]['channel']['architecture']) == arch:
      found = 1
      dlfile((chanmap[idx]['download']['url']),'./')
snap_uri.close()
  