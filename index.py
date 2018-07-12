import sys
import os
sys.path.append(os.path.join(sys.path[0], 'modules'))

import connect
import other
import processing

# resPd = connect.start(pd, './excel/certificates.xlsx')
resPd = connect.start2('./excel/output3.xlsx')

ser = processing.version(resPd)
ser = processing.smth(resPd, ser)

resPd = connect.series(resPd, ser)

connect.end(resPd, './excel/output4.xlsx')

print('Normas')
