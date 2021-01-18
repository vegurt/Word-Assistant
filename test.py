import pandas as pd

dd = pd.read_excel(
    'trans_data.xlsx', index_col=0, sheet_name=None)
dd_concatted = pd.concat([dd[i] for i in list(dd.keys()) if not i.startswith('-')]).reset_index(drop=True).dropna(how = 'all').dropna(how = 'all', axis = 1)
shape = dd_concatted.shape

#dd['全部'] = dd_concatted
l = list(dd.keys())

def find_word(method, word):
    global shape, dd_concatted
    if method == '英>汉':
        for i in range(shape[0]):
            if word in dd_concatted['ch'][i]:
                return i
    elif method == '汉>英':
        for i in range(shape[0]):
            if word in dd_concatted['eng'][i]:
                return i
    #else:
    #    return -1

for i in l:
    dd[i] = dd[i].dropna(how = 'all').dropna(how = 'all', axis = 1)

i = 'Unit 1'
j = 26
print(dd[i]['ch'][j])
'''
for i in list(dd.keys()):
    #print(dd[i]['ch'])
    for j in range(1, dd[i].shape[0]+1):
        print(dd[i]['ch'][j])
        '''