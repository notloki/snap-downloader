from sys import argv
from requests import get
import json

try:
  snap_name = argv[1]
except:
  raise 'python3 -m snap-downloader.py [SNAPNAME] [ARCHITECTURE]'

if len(argv) < 3:
  arch = 'amd64'
else:
  arch = argv[2]

def dlfile(url: str, save_path: str) -> None:
  
  dlreq = get(url, stream= True)
  local_filename = url.split('/')[-1]
  path = save_path + local_filename
  accum: int = 0
  if dlreq.status_code == 200:
    with open (path, 'wb') as f:
      for chunk in dlreq.iter_content(chunk_size=1024*1024):
        if chunk:
          accum += len(chunk)
          
          print('Downloaded: {}'.format(accum),sep='\x1b[2K\r')
          f.write(chunk)
    
    f.close()
    dlreq.close()
    
    #return dict({'bytes':accum, 'file':local_filename})    
  else:
    dlreq.close()
    #return dict({'bytes':0, 'file':'failed'})


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
  