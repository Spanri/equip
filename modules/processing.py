import re
from fuzzywuzzy import fuzz


def version(ser):
    """
    Processing file and return Version, WithoutVers
    """
    Name = ser['Название']
    # print(Name) 2691
    Version = []
    WithoutVers = []
    for i in range(len(Name)):
        vers = re.findall(
            r'''(ПО не классифицируется по версиям|
            ПО: не классифицируется по версиям)()''', 
            str(Name[i]))
        if not vers:
            vers = re.findall(
                r'''верси.+?(?=верси|cерийн|с функ|в составе|
                технич|идентифи|завод|зав.|партия|по заявке|
                выполняю|реализу|и медиаш|где|ПО "|ПО «|
                \)|\(|$)''', str(Name[i]))
        # print(vers)
        if not vers:
            vers = re.findall(
                r'''(программное обеспечение отсутствует|
                не классифицируется по |ПО: не классифицируется по|ПО: не классифицируется)()''', str(Name[i]))
        if not vers:
            vers = re.findall(r'''(ПО:.+$)()''', str(Name[i]))
        WithoutVers.append(str(Name[i]))
        vvv = []
        if vers:
            for key2 in vers:
                a = str(key2)
                WithoutVers[i] = WithoutVers[i].replace(a, '')
                a = re.sub(
                    r'''(версия ПО -|версия ПО:|версия ПО|версии ПО:|
                    версии ПО|версии|ПО|версия программного обеспечения|версия)''',
                    '', a)
                a = re.sub(r'(^(\s)*|(\s)*$|\)(\s)*$|;(\s)*$)', '', a, re.M)
                vvv.append(a)
        WithoutVers[i] = re.sub(r'\(ПО \)', '', WithoutVers[i])
        if not vvv == []:
            Version.append(vvv)
        else:
            Version.append(str(''))
    ser2 = {
        'Версия': Version,
        'Без лишнего': WithoutVers
    }
    ser = {**ser, **ser2}
    return ser


def smth(ser):
    """
    Processing file and return Rep
    """
    WithoutVers = ser['Без лишнего']
    Rep = []
    Aplic = []
    AllRep = []
    Partya = []
    SerNum = []
    Where = []
    AsA = []
    TecCon = []
    words = ''
    for i in range(len(WithoutVers)):
        WithoutVers[i] = re.sub(r'\(\)', '', str(WithoutVers[i]))
        WithoutVers[i] = re.sub(r'(,(\s)*$)', '', str(WithoutVers[i]))
        """
        Other thing
        """
        words = str(WithoutVers[i])
        Where0, Partya0, SerNum0, Aplic0, AsA0, TecCon0, words = other(words)
        if not Where0 == []:
            Where += Where0
        else:
            Where.append(str(''))
        if not Partya0 == []:
            Partya += Partya0
        else:
            Partya.append(str(''))
        if not SerNum0 == []:
            SerNum += SerNum0
        else:
            SerNum.append(str(''))
        if not Aplic0 == []:
            Aplic += Aplic0
        else:
            Aplic.append(str(''))
        if not AsA0 == []:
            AsA += AsA0
        else:
            AsA.append(str(''))
        if not TecCon0 == []:
            TecCon += TecCon0
        else:
            TecCon.append(str(''))
        words = re.sub(r'(\(\)|\((\s)*$)', '', str(words))
        words = words.replace(' ) ', ' ')
        """
        End of other thing
        """
        Iskl = re.findall(r'^[а-яА-Я-,\s/]+?(?=[А-Я]{3,}|:|\(|\d|[a-zA-Z]|\"|«|$)', str(words), re.M)
        if not Iskl == []:
            if len(Iskl[0]) == 1:
                Rep.append(str(''))
            else:
                Rep.append(Iskl[0])
                words = words.replace(Iskl[0], '')
        else:
            Rep.append(str(''))
        AllRep.append(words)
    WithoutVers[i] = re.sub(
        r'(\"|\s\(|\)\s|\)$|«|»|\s-|\:|\,\s$|\s$|\.$|\,$|^[:\s]*)',
        ' ', str(WithoutVers[i]), re.M)
    ser2 = {
        'Название': ser['Название'],
        'Без лишнего': AllRep,
        'Модели': Rep,
        'Версия': ser['Версия'],
        'в составе согласно Приложению': Aplic,
        'Партия': Partya,
        'Номера': SerNum,
        'Расшифровки': Where,
        'В качестве': AsA,
        'Технические условия': TecCon
    }
    return ser2


def other(words):
    Where0 = []
    Partya0 = []
    SerNum0 = []
    Aplic0 = []
    AsA0 = []
    TecCon0 = []
    # в составе согласно приложению
    hhh = re.findall(
        r'''(в составе согласно Приложению|в составе согласно приложению|
        в составе приведенном в приложении|в составе согласно Приложению|
        в составе, приведенном в приложении).+?(.|,|$)''', words)
    if not hhh == []:
        Aplic0.append(True)
        words = re.sub(
            r'''(в составе согласно Приложению|в составе согласно приложению|в составе приведенном в приложении|В СОСТАВЕ пРИЛОЖЕНИЯ|в составе, приведенном в приложении)''', '', words)
    # где...  177 857
    where = re.findall(r'где.+?(?=\)|;|$)', words)
    if not where == []:
        Where0.append(where)
        words = re.sub(r'где.+?(?=\)|;|$)', '', words)
    # партия
    partya0 = re.findall(r'партия.+?(?=с серийными|$)', words)
    par2 = re.findall(r'Партия', words)
    if not par2 == []:
        partya0 = re.findall(r'(?=в количестве).+$', words)
    if not partya0 == []:
        Partya0.append(partya0)
        words = re.sub(r'в количестве.+$', '', words)
        words = re.sub(r'партия.+?(?=с серийными|$)', '', words)
    # номера 5874 5875 7242 7243
    otherNum = re.findall(
        r'((заводские|зав.|заводской номер|идентификационн|с идентификацион).+?(?=\)|;|$))', words)
    serNum = re.findall(r'((серийны|с серийны).+?(?=\)|;|$))', words)
    if not serNum == []:
        serNum = serNum[0][0]
    repNum = []
    repNum = re.findall(r'(серий.+?серий){1}', words)
    if not repNum == []:
        serNum = re.findall(r'серийны.+?(?=\,|;|\)|$)', words)
    if not otherNum == []:
        serNum.append(otherNum[0][0])
        words = re.sub(
            r'((заводские|зав.|заводской номер|идентификационн|с идентификацион).+?(?=\)|;|$))', '', words)
    if not serNum == []:
        SerNum0.append(serNum)
        words = re.sub(r'((серийны|с серийны).+?(?=\)|;|$))', '', words)
    # в качестве
    asA = re.findall(r'в качестве.+$', words)
    if not asA == []:
        AsA0.append(asA)
        words = re.sub(r'в качестве.+$', '', words)
    # технические условия
    tecCon = re.findall(r'технические условия.+?(?=;|$)', words)
    if not tecCon == []:
        TecCon0.append(tecCon)
        words = re.sub(r'технические условия.+?(?=;|$)', '', words)
    return Where0, Partya0, SerNum0, Aplic0, AsA0, TecCon0, words


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
    return Iskl
