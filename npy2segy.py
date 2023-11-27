import numpy as np
from pathlib import Path
import sys
import segyio
import time

def npy2segy(npyfile:str, headersfile:str, output:str):
    
    print('Reading txt file...')
    with open(Path(headersfile), 'r') as f:
        txt = f.readlines()

    shape = (int(txt[1]) ,int(txt[0]))
    print('Reading npy...')
    cube = np.memmap(Path(npyfile), dtype='float32', mode='r', shape=shape)
    N = int(txt[0])
    print('Creating SEGY...')
    il = np.fromstring(txt[2], dtype=int, sep=' ')
    xl = np.fromstring(txt[3], dtype=int, sep=' ')
    t = np.fromstring(txt[4], dtype=float, sep=' ')
    
    #spec = segyio.spec()
    #spec.ilines = il
    #spec.xlines = xl
    #spec.samples = t
    #spec.format = 5
    #spec.sorting = 2
    #spec.tracecount = N
    #ils, xls = np.meshgrid(il, xl)
    #ils = ils.flatten('F')
    #xls = xls.flatten('F')
    #with segyio.create(Path(output), spec) as s:
    with segyio.open(Path(output), mode='r+') as s:
         #s.text[:] = txt[5:]
         print('Copying traces...') 
         #for i in range(N):
         for i,h in enumerate(s.header[:]):
             #h.update({segyio.TraceField.INLINE_3D: ils[i], segyio.TraceField.CROSSLINE_3D: xls[i]}) 
             s.trace[i] = cube[:, i] 
    return None


if __name__ == "__main__":
     t1 = time.time()
     print('Start')
     npy2segy(npyfile = str(sys.argv[1]), headersfile = str(sys.argv[2]), output = str(sys.argv[3]))
     print(f'Completed...{time.time()-t1} sec pased')

