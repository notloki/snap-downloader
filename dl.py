from requests import get


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


