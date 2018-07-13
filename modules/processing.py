import re
from fuzzywuzzy import fuzz


def version(ser):
    """
    Processing file and return Version, WithoutVers
    """
    Name = ser['Название']
    # print(Name)
    Version = []
    WithoutVers = []
    for i in range(len(Name)):
        vers = re.findall(
            r'(?=(верси.+?)(верси|cерийн|с функ|в составе|техническ|идентифи|завод|зав.|партия|по заявке|выполняю|реализу|и медиаш|где|$|\)|\())', str(Name[i]))
        # print(vers)
        if(not vers):
            vers = re.findall(
                r'(программное обеспечение отсутствует)()', str(Name[i]))
        Version.append(str(''))
        WithoutVers.append(str(Name[i]))
        if vers:
            for key2 in vers:
                # Заносим очередную версию в Version
                Version[i] += str(key2[0]) + ' || '
                # Удаляем версию
                WithoutVers[i] = re.sub(
                    str(key2[0]), '', WithoutVers[i])
            # Удаляем всякие штуки
            # print(WithoutVers[i])
            Version[i] = re.sub(
                r'(версия\sПО\s-|версия\sПО:|версия\sПО|версии\sПО:|версии\sПО|версии|версия\sпрограммного\sобеспечения|версия)', '', Version[i])
        # print(WithoutVers[i])
            
    ser2 = {
        'Версия': Version,
        'Без версии': WithoutVers
    }
    ser = {**ser, **ser2}
    return ser

# ; это разные оборудования
# разделить по ;
# и для каждого элемента пропустить этот цикл
# НОООО иногда бывает, что это модели разные,
# значит попробовать после этого еще сравнить по ;


def smth(ser):
    """
    Processing file and return Rep
    """
    WithoutVers = ser['Без версии']
    Rep = []
    Aplic = []
    AllRep = []
    WithoutRep = []
    Partya = []
    SerNum = []
    Where = []
    words = ''
    for i in range(len(WithoutVers)):
        """
        Other thing
        """
        words = str(WithoutVers[i])
        hhh = re.findall(r'(в составе согласно Приложению|в составе согласно приложению|в составе, приведенном в приложении).+$', words)
        partya0 = re.findall(r'партия.+$', words)
        serNum = re.findall(r'серийные номера.+$', words)  
        otherNum = re.findall(r'((заводские номера|зав.|заводской номер|идентификационные номера).+[;$)])', words)
        par2 = re.findall(r'Партия', words)
        where = re.findall(r'где.+[)$]', words)
        if not where == []:
            Where.append(where)
        else:
            Where.append(str(''))
        if not par2 == []:
            partya0 = re.findall(r'в количестве.+$', words)     
        words = re.sub(
            r'(в составе согласно Приложению|в составе согласно приложению|в составе, приведенном в приложении|серийные номера|партия).+$',
            '', str(WithoutVers[i]))
        if not partya0 == []:
            Partya.append(partya0)
            words = re.sub(r'в количестве.+$', '', words)
        else:
            Partya.append(str(''))
        if not otherNum == []:
            serNum.append(otherNum[0][0])
        if not serNum == []:
            # print(serNum)
            SerNum.append(serNum)
        else:
            SerNum.append(str(''))
        if not hhh == []:
            Aplic.append(True)
        else:
            Aplic.append(str(''))
        """
        End of other thing (Yes, i cannot put it in func)
        """
        Iskl, AllR = comma(words)
        AllRep.append(AllR)
        if Iskl:
            Rep.append(Iskl)
        else:
            Rep.append(str(''))
        WithoutRep.append(str(WithoutVers[i]))
        for rep in Rep[i]:
            p = re.compile(r'(^\s|\s$)', re.M)
            rep = re.sub(p, '', str(rep))
            rep = re.sub(r'(\)\)$)', ')', str(rep))
        # for key in Rep[i]:
        #     print(str(key) + ' ' + str(WithoutRep[i]))
        #     WithoutRep[i] = re.sub(
        #         str(key) + ',' 
        #         or str(key) + r'$' 
        #         or str(key) + '"'
        #         or str(key) + r'\s$', 
        #         '', str(WithoutRep[i]))
    WithoutVers[i] = re.sub(r'(\"|\s\(|\)\s|\)$|«|»|\s-|\:|\,\s$|\s$|\.$|\,$)',
                    ' ', str(WithoutVers[i]))
    WithoutVers[i] = re.sub(r'(\)\,)', ',', str(WithoutVers[i]))
    ser2 = {
        'Без версии': WithoutVers,
        'Все повторения': AllRep,
        'Модели': Rep,
        # 'Без моделей': WithoutRep
        'в составе согласно Приложению': Aplic,
        'Партия': Partya,
        'Номера': SerNum,
        'где...': Where
    }
    ser = {**ser, **ser2}
    return ser


def comma(words0):
    Iskl = []
    words = words0.replace(';', ',').split(', ')
    for i, word in enumerate(words):
        if(not i == len(words)-1):
            if(abs(len(words[i]) - len(words[i+1])) > 5):
                lenn = min(len(words[i]), len(words[i+1]))
                words[i] = words[i][slice(-lenn-1, len(words[i]))]
                words[i+1] = words[i+1][slice(-lenn-1, len(words[i+1]))]
        for word2 in words:
            fuz = fuzz.token_sort_ratio(word, word2)
            if fuz > 70 and fuz < 100:
                Iskl.append(word)
                Iskl.append(word2)
        Iskl = list(set(Iskl))
    AllRep = words.copy()
    return Iskl, AllRep