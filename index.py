#%% Main

# подключение модулей
import sys
import os
sys.path.append(os.path.join(sys.path[0], 'modules'))
import connect
import processing

#%% Parse

ser = {}

# первая строка - для работы с изначальным файлом (который вы нам дали)
# вторая строка - для работы с файлом, в который вынесены названия оборудования
# ser = connect.start('./excel/certificates.xlsx')
ser = connect.start2('./excel/output.xlsx')

print('Файл открылся')

# сначала отбираем версию, а потом всё остальное
ser = processing.version(ser)
print('Версия убралась')
ser = processing.smth(ser)
print('Всё остальное обработалось')

#%% End
# превращаем объект ser в excel файл под названием output4
# (можно как угодно назвать)
connect.end(ser, './excel/output4.xlsx')

print('Закончилось')
