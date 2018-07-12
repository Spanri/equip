#%% Test11
"""
This will be another comment line 
for the testing of the different sections
"""
from notebook.auth import passwd
passwd('nysha2161')

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
print(resPd)

connect.end(resPd, './excel/output4.xlsx')
#%% Test12
print('Normas')
