
import xlrd
sheet='20000_words-2'
output = '200dic.txt'
data = xlrd.open_workbook('20000_words调序整洁版.xlsx')

sheet0 = data.sheet_by_index(0)

column_dic = sheet0.col_values(1)
# print(column_dic)

with open(output,'w') as f:
    for val in column_dic:
        if type(val) != str:
            continue
        # val=val.strip()
        val= val.strip()
        print(val)
        f.write(val+'\n')
        # save text