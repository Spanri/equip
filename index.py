#%% Main

import sys
import os
sys.path.append(os.path.join(sys.path[0], 'modules'))

import connect
import other
import processing

#%% Parse

# example of ser
# {
#   'Название': Column_Name_of_file,
#   'Другое наименование': Column_AAA_of_file
# }
ser = {}

# ser = connect.start(pd, './excel/certificates.xlsx')
ser = connect.start2('./excel/output3.xlsx')
# print(ser)

ser = processing.version(ser)
ser = processing.smth(ser)

#%% End
connect.end(ser, './excel/output4.xlsx')

print('Normas')
