import re


def version(resPd):
    """
    Processing file and return Version, WithoutVers
    """
    Version = []
    WithoutVers = []
    for i, key in resPd.iterrows():
        vers = re.findall(
            r'(?=(верси.+?)(верси|cерийн|с функ|в составе|техническ|идентифи|завод|зав.|партия|по заявке|выполняю|реализу|и медиаш|$|\)|\())', str(key.Name))
        if(not vers):
            vers = re.findall(
                r'(программное обеспечение отсутствует)()', str(key.Name))
        Version.append(str(''))
        WithoutVers.append(str(key.Name))
        if vers:
            for key2 in vers:
                # Заносим очередную версию в Version
                Version[i] += str(key2[0]) + ' || '
                # Удаляем версию
                WithoutVers[i] = re.sub(
                    str(key2[0]), '', WithoutVers[i])
            # Удаляем всякие штуки
            WithoutVers[i] = re.sub(
                r'(\(\)|\s$|\,\s$|\.$)', '', WithoutVers[i])
            Version[i] = re.sub(
                r'(версия\sПО\s-|версия\sПО:|версия\sПО|версии\sПО:|версии\sПО|версии|версия\sпрограммного\sобеспечения|версия)', '', Version[i])
    ser = {
        'Версия': Version,
        'Без версии': WithoutVers
    }
    return ser


def smth(resPd, ser):
    """
    Processing file and return Rep
    """
    Version = ser['Версия']
    WithoutVers = ser['Без версии']
    Rep = []
    AAA = []
    words = ''
    for i, key in resPd.iterrows():
        Table = []
        Iskl = []
        if Version[i]:
            words = re.sub(r'(\"|\(|\)|\,|«|»|;|\s-\s|:)',
                           '', str(WithoutVers))
            aaa = re.findall(r'\s([A-Za-z\d\-/]+)', str(words))
            if aaa:
                AAA.append(aaa[0])
            else:
                AAA.append(str(''))
            words = words.split(' ')
            for word in words:
                if word not in Table:
                    Table.append(word)
                else:
                    if word not in Iskl:
                        Iskl.append(word)
        if Iskl:
            Rep.append(Iskl)
        else:
            Rep.append(str(''))
    ser2 = {
        'Чето': Rep
    }
    ser = {**ser, **ser2}
    return ser
