import xlrd
import pandas as pd
import xlsxwriter


def start(file_name):
    """
    Return file with column 'Name'
    """
    file = file_name
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


def start2(file_name):
    """
    Return file
    """
    file = file_name
    xl = pd.ExcelFile(file)
    res_pd = xl.parse(xl.sheet_names[0])
    # print(resPd.Name)
    ser = {
        'Название': res_pd.Name,
    }
    return ser


def end(ser, file_name):
    """
    Save resPd to fileName
    """
    res_pd = pd.DataFrame(ser)
    writer = pd.ExcelWriter(file_name)
    res_pd.to_excel(writer, 'Лист1')
    writer.save()
