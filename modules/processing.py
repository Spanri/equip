import re
from fuzzywuzzy import fuzz


def version(ser):
    """
    Processing file and return Version, WithoutVers
    """
    Name = ser['Название']
    # print(Name) 2691
    Version = []
    Without_vers = []
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
        Without_vers.append(str(Name[i]))
        vvv = []
        if vers:
            for key2 in vers:
                a = str(key2)
                Without_vers[i] = Without_vers[i].replace(a, '')
                a = re.sub(
                    r'''(версия ПО -|версия ПО:|версия ПО|версии ПО:|
                    версии ПО|версии|ПО|версия программного обеспечения|версия)''',
                    '', a)
                a = re.sub(r'(^(\s)*|(\s)*$|\)(\s)*$|;(\s)*$)', '', a, re.M)
                vvv.append(a)
        Without_vers[i] = re.sub(r'\(ПО \)', '', Without_vers[i])
        if not vvv == []:
            Version.append(vvv)
        else:
            Version.append(str(''))
    ser2 = {
        'Версия': Version,
        'Без лишнего': Without_vers
    }
    ser = {**ser, **ser2}
    return ser


def smth(ser):
    """
    Processing file and return Rep
    """
    Without_vers = ser['Без лишнего']
    Rep = []
    Aplic = []
    All_rep = []
    Partya = []
    Ser_num = []
    Where = []
    As_a = []
    Tec_con = []
    words = ''
    for i in range(len(Without_vers)):
        Without_vers[i] = re.sub(r'\(\)', '', str(Without_vers[i]))
        Without_vers[i] = re.sub(r'(,(\s)*$)', '', str(Without_vers[i]))
        """
        Other thing
        """
        words = str(Without_vers[i])
        Where0, Partya0, Ser_num0, Aplic0, As_a0, Tec_con0, words = other(words)
        if not Where0 == []:
            Where += Where0
        else:
            Where.append(str(''))
        if not Partya0 == []:
            Partya += Partya0
        else:
            Partya.append(str(''))
        if not Ser_num0 == []:
            Ser_num += Ser_num0
        else:
            Ser_num.append(str(''))
        if not Aplic0 == []:
            Aplic += Aplic0
        else:
            Aplic.append(str(''))
        if not As_a0 == []:
            As_a += As_a0
        else:
            As_a.append(str(''))
        if not Tec_con0 == []:
            Tec_con += Tec_con0
        else:
            Tec_con.append(str(''))
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
        All_rep.append(words)
        Without_vers[i] = re.sub(
            r'(\"|\s\(|\)\s|\)$|«|»|\s-|\:|\,\s$|\s$|\.$|\,$|^[:\s]*)',
            ' ', str(Without_vers[i]), re.M)
    ser2 = {
        'Название': ser['Название'],
        'Без лишнего': All_rep,
        'Модели': Rep,
        'Версия': ser['Версия'],
        'в составе согласно Приложению': Aplic,
        'Партия': Partya,
        'Номера': Ser_num,
        'Расшифровки': Where,
        'В качестве': As_a,
        'Технические условия': Tec_con
    }
    return ser2


def other(words):
    Where0 = []
    Partya0 = []
    Ser_num0 = []
    Aplic0 = []
    As_a0 = []
    Tec_con0 = []
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
    other_num = re.findall(
        r'((заводские|зав.|заводской номер|идентификационн|с идентификацион).+?(?=\)|;|$))', words)
    ser_num = re.findall(r'((серийны|с серийны).+?(?=\)|;|$))', words)
    if not ser_num == []:
        ser_num = ser_num[0][0]
    rep_num = []
    rep_num = re.findall(r'(серий.+?серий){1}', words)
    if not rep_num == []:
        ser_num = re.findall(r'серийны.+?(?=\,|;|\)|$)', words)
    if not other_num == []:
        ser_num.append(other_num[0][0])
        words = re.sub(
            r'((заводские|зав.|заводской номер|идентификационн|с идентификацион).+?(?=\)|;|$))', '', words)
    if not ser_num == []:
        Ser_num0.append(ser_num)
        words = re.sub(r'((серийны|с серийны).+?(?=\)|;|$))', '', words)
    # в качестве
    asA = re.findall(r'в качестве.+$', words)
    if not asA == []:
        As_a0.append(asA)
        words = re.sub(r'в качестве.+$', '', words)
    # технические условия
    tec_con = re.findall(r'технические условия.+?(?=;|$)', words)
    if not tec_con == []:
        Tec_con0.append(tec_con)
        words = re.sub(r'технические условия.+?(?=;|$)', '', words)
    return Where0, Partya0, Ser_num0, Aplic0, As_a0, Tec_con0, words


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
