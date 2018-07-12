import xlrd
import pandas as pd
import xlsxwriter

def start(fileName):
    """
    Return file with column 'Name'
    """
    file = fileName
    xl = pd.ExcelFile(file)

    df1 = xl.parse(xl.sheet_names[0])
    res = []
    for i, row in df1.iterrows():
        res.append(row.Name)
    resPd = pd.DataFrame({'Name': res})
    return resPd


def start2(fileName):
    """
    Return file
    """
    file = fileName
    xl = pd.ExcelFile(file)
    resPd = xl.parse(xl.sheet_names[0])
    return resPd


def series(resPd, ser):
    """
    Do 'pd.Series' for all element of ser 
    (add new columns to resPd)
    """
    for key, value in ser.items():
        value = pd.Series(value)
        resPd = resPd.assign(key=value.values)
        resPd = resPd.rename(columns={'key': key})
    return resPd


def end(resPd, fileName):
    """
    Save resPd to fileName
    """
    writer = pd.ExcelWriter(fileName)
    resPd.to_excel(writer, 'Лист1')
    writer.save()
