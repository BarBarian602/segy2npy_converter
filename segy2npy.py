import numpy as np
from pathlib import Path
import sys
import segyio
import time

def create_path_npy(segyfile:str):
    if segyfile.find('.sgy')>0:
        return (segyfile.lower().replace('.sgy', '.npy'))
    if segyfile.find('.segy')>0:
        return (segyfile.lower().replace('.segy', '.npy'))

def create_optimize_npy(npyfile:str):
        return (npyfile.lower().replace('.npy', '_opt.npy'))

def create_txt_headers(path:str):
     return path.lower().replace('.npy', '_headers.txt')

def segy2npy(segypath: str, byteIl: int, byteXL: int, byteX: int, byteY: int, second_file:str):
    print('Opening SEGY...')
    with segyio.open(Path(segypath), mode='r', iline=byteIl, xline=byteXL, ignore_geometry=True) as f:
        shape = (len(f.samples), f.tracecount)
        pOut = create_path_npy(segypath)
        pTxt = create_txt_headers(pOut)
        cube = np.memmap(Path(pOut), dtype='float32', mode='w+', shape=shape)
        #il = f.ilines
        #xl = f.xlines
        time = f.samples
        print('Copying traces...')
        x = []
        y = []
        ils = []
        xls = []
        for i in range(f.tracecount):
            cube[:, i] = f.trace[i]
            x.append(f.header[i].get(byteX))
            y.append(f.header[i].get(byteY))
            ils.append(f.header[i].get(byteIl))
            xls.append(f.header[i].get(byteXL))


        print('Writing headers...')
        with open (Path(pTxt), 'w+') as t:
            t.write(str(f.tracecount)+'\n') #0
            t.write(str(len(f.samples))+'\n') #1
            #t.write(''.join(map(lambda i: str(i) +' ', il))+'\n') #2
            #t.write(''.join(map(lambda i: str(i) +' ', xl))+'\n') #3
            #t.write(''.join(map(lambda i: str(i) +' ', x))+'\n') #4
            #t.write(''.join(map(lambda i: str(i) +' ', y))+'\n') #5
            #t.write(''.join(map(lambda i: str(i) +' ', t))+'\n') #6
            #t.write(segyio.tools.wrap(f.text[0]) + '\n') #5
        print(second_file)
        print(second_file == 'True' )
        if second_file == 'True':
            print('Creating second file...')
            pOut2 = create_optimize_npy(pOut)
            pOutSeg2 = pOut2.replace('.npy', '.sgy')
            np.memmap(Path(pOut2), dtype='float32', mode='w+', shape=shape)
            il = np.unique(ils)
            xl = np.unique(xls)
            spec = segyio.spec()
            spec.ilines = il
            spec.xlines = xl
            spec.samples = time
            spec.format = 5
            spec.sorting = 2
            spec.tracecount = f.tracecount
            with segyio.create(Path(pOutSeg2), spec) as s:
                 s.text[0] = f.text[0]
                 for j, h in enumerate(s.header[:]):
                      h.update({segyio.TraceField.CDP_X: x[j], segyio.TraceField.CDP_X: x[j], segyio.TraceField.CDP_Y: y[j], segyio.TraceField.INLINE_3D: ils[j], segyio.TraceField.CROSSLINE_3D: xls[j]})
                      s.trace[i] = np.ones(time.size)
                      
    return None


if __name__ == "__main__":
     """ 
     Call function in terminal and write: 
     1) SEGY filename: str,
     2) byte of Inline header: int,
     3) byte of Xline header: int,
     4) byte of CDP_X header: int,
     5 byte of CDP_Y header: int,
     6) True / False if you need to create second output file: bool
     """
     t1 = time.time()
     print('Start')
     segy2npy(segypath=str(sys.argv[1]), byteIl=int(sys.argv[2]), byteXL=int(sys.argv[3]), byteX=int(sys.argv[4]), byteY=int(sys.argv[5]), second_file=(sys.argv[6]))
     print(f'Completed...{time.time()-t1} sec pased')


