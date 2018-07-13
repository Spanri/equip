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
    ser = {
        'Название': resPd.Name,
    }
    return ser


def start2(fileName):
    """
    Return file
    """
    file = fileName
    xl = pd.ExcelFile(file)
    resPd = xl.parse(xl.sheet_names[0])
    # print(resPd.Name)
    ser = {
        'Название': resPd.Name,
    }
    return ser


def end(ser, fileName):
    """
    Save resPd to fileName
    """
    resPd = pd.DataFrame(ser)
    writer = pd.ExcelWriter(fileName)
    resPd.to_excel(writer, 'Лист1')
    writer.save()
