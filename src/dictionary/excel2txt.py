
import xlrd  # pip install xlrd==1.2.0  # getiterator() 改为 iter()
sheet='20000_words-2'
# output = '200dic.txt'
data = xlrd.open_workbook('20000_words调序整洁版.xlsx')

sheet0 = data.sheet_by_index(0)

column_dic = sheet0.col_values(1)
# print(column_dic)
output = f'{len(column_dic)}dic.txt'

with open(output, 'w') as f:
    for __val in column_dic:
        if type(__val) != str:
            continue
        # val=val.strip()
        __val = __val.strip()
        # 必须大于3个字符
        if len(__val) < 4:
            continue
        print(__val)
        f.write(__val+'\n')
        # save text