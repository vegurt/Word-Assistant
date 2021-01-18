from sys import argv
from tkinter import *

import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml import etree


def translate(words):
    """函数说明：
    因为采用 get 方式 url 中要过滤掉 / 换成全角。否则引起url的解析错误。
    response.text 是 bytes 数据类型
    """
    URL = "http://dict.youdao.com/w/eng/{}/#keyfrom=dict2.index"
    #headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/70.0.3538.67 Chrome/70.0.3538.67 Safari/537.36'}
    words = words.replace("/", "／")
    url = URL.format(words)

    response = requests.get(url, headers=headers)
    selector = etree.HTML(response.text)     # 生成 selector  对象, 利用 xpath 获得内容
    content = selector.xpath("//div[@id='results-contents']")[0]
    content = etree.tostring(content, encoding='utf-8', method='html')

    result = content.decode('utf-8')
    # url 方式要过滤掉 / 换成全角
    # result = result.replace(
    #    "<img src", "<img style='float:right;width:30vw' src")
    result = BeautifulSoup(result, features='lxml').get_text()
    result = result.split('\n')
    res = result
    for i in res:
        if i == '':
            result.remove('')
    res = []
    for i in result:
        res.append(i.strip())

    result = '\n'.join(res)+'\n'
    return result


def word_match(your_word, correct_word):
    for i in your_word:
        if i not in correct_word:
            return False
    return True


class application(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        self.pack()

        self.trans = ['英>汉', '汉>英']

        self.svar = StringVar()
        self.ivar1 = IntVar()
        self.ivar2 = IntVar()

        try:
            self.dd_all = pd.read_excel(
                'trans_data.xlsx', index_col=0, sheet_name=None)
            self.units = list(self.dd_all.keys())
            self.dd_all['全部单词'] = pd.concat([self.dd_all[i] for i in self.units if not i.startswith(
                '-') and i.endswith('-w')]).reset_index(drop=True).dropna(how='all').dropna(how='all', axis=1)
            self.dd_all['真·全部单词'] = pd.concat(
                [self.dd_all[i] for i in self.units if i.endswith('-w')]).reset_index(drop=True).dropna(how='all').dropna(how='all', axis=1)
            self.dd_all['全部句子'] = pd.concat([self.dd_all[i] for i in self.units if not i.startswith(
                '-') and i.endswith('-s')]).reset_index(drop=True).dropna(how='all').dropna(how='all', axis=1)
            self.dd_all['真·全部句子'] = pd.concat(
                [self.dd_all[i] for i in self.units if i.endswith('-s')]).reset_index(drop=True).dropna(how='all').dropna(how='all', axis=1)
            self.units_all = list(self.dd_all.keys())
            for i in self.units:
                self.dd_all[i] = self.dd_all[i].dropna(
                    how='all').dropna(how='all', axis=1)
            self.create_widgets()
        except Exception:
            self.master.destroy()
            tl = Tk()
            tl.title('ERROR')
            Message(tl, text='Excel File "trans_data.xlsx" Not Found',
                    width=800).pack()

    def create_widgets(self):
        self.fr1 = Frame()
        self.fr1.pack(side='top', fill='x')
        self.fr2 = Frame()
        self.fr2.pack(side='top', fill='both')
        self.fr11 = Frame(self.fr1)
        self.fr11.pack(side='left', fill='y')
        self.fr12 = Frame(self.fr1)
        self.fr12.pack(side='right', fill='both')
        self.fr122 = Frame(self.fr12)
        self.fr122.pack(side='bottom', fill='x')
        self.fr121 = Frame(self.fr12)
        self.fr121.pack(side = 'bottom', fill='both')

        self.orig_text = Label(self.fr121, text='Your Word Assistant', font=(
            'Times New Roman', 16, 'italic'), anchor='center', justify='left', wraplength=550, width = 550, height = 10, relief = 'ridge')
        self.orig_text.pack(side='bottom', fill='x')

        self.unit_op = Listbox(self.fr11, height=10)
        for i in self.units_all:
            self.unit_op.insert(END, i)
        self.unit_op.pack(side='left')

        self.unit_scr = Scrollbar(self.fr11)
        self.unit_scr.pack(side='left', fill='y')

        self.unit_op.config(yscrollcommand=self.unit_scr.set)
        self.unit_scr.config(command=self.unit_op.yview)

        self.trans_op = Listbox(self.fr11, height=2)
        for i in self.trans:
            self.trans_op.insert(END, i)
        self.trans_op.pack(side='left')

        self.btns = Button(self.fr11, text='start', command=self.start_call)
        self.btns.pack(side='left')

        self.btnn = Button(self.fr122, text='next', command=self.next_call)
        self.btnn.pack(side='right')

        self.btnl = Button(self.fr122, text='last', command=self.last_call)
        self.btnl.pack(side='right')
        
        self.btnc = Button(self.fr122, text='check', command=self.check_call)
        self.btnc.pack(side='right')

        self.btnr = Checkbutton(self.fr122, text='记忆模式', variable=self.ivar2)
        self.btnr.pack(side='left')
        
        self.btny = Checkbutton(
            self.fr122, text='有道词典（需联网）', variable=self.ivar1)
        self.btny.pack(side='left')        
        
        self.answer = Entry(self.fr122, textvariable=self.svar, width = 100)
        self.answer.pack(side='right', fill='x')        

        self.scr = Scrollbar(self.fr2)
        self.scr.pack(side='right', fill='y')

        self.t = Text(self.fr2, font=('微软雅黑', 12), width=800, height=1000)
        self.t.pack(side='right', fill='both')

        self.t.config(yscrollcommand=self.scr.set)
        self.scr.config(command=self.t.yview)

        self.answer.bind('<Up>', self.last_call)
        self.answer.bind('<Down>', self.next_call)
        self.answer.bind('<Return>', self.check_call)

    def next_call(self, event=None):
        try:
            if self.num < self.letter_info[0] - 1:
                self.num += 1
            else:
                self.num = 0

            self.svar.set('')
            self.letter_ori = self.ds[self.trans_from][self.num]
            self.orig_text.config(text=self.letter_ori)

            self.check_call(flag=0)
        except Exception:
            self.t.insert(END, '请点击“Start”按钮以开始\n\n')

    def last_call(self, event=None):
        try:
            if self.num > 0:
                self.num -= 1
            else:
                self.num = self.letter_info[0] - 1

            self.svar.set('')
            self.letter_ori = self.ds[self.trans_from][self.num]
            self.orig_text.config(text=self.letter_ori)

            self.check_call(flag=0)
        except Exception:
            self.t.insert(END, '请点击“Start”按钮以开始\n\n')

    def check_call(self, event=None, flag=1):
        try:
            self.corr_answer = self.ds[self.trans_to][self.num]
            self.t.delete(1.0, END)
            self.t.insert(END, '\n'.join(
                [self.uni_status, self.tra_status])+'\n\n\n')
            if flag == 1 or self.ivar2.get():
                self.t.insert(END, '\n'.join(
                    [self.ds['eng'][self.num], self.ds['detail'][self.num]])+'\n')
                self.MyAnswer = self.svar.get()
                if not self.ivar2.get():
                    if self.MyAnswer:
                        if (self.tra_status == '英>汉' and word_match(self.MyAnswer, self.corr_answer)) or (self.tra_status == '汉>英' and self.MyAnswer == self.corr_answer):
                            self.t.insert(END, '\n\nYour answer is RIGHT:  %s' %
                                          self.corr_answer)

                        else:
                            self.t.insert(END, '\n\nYour answer(%s) is WRONG\nThe correct answer is:\n\n%s' % (
                                self.MyAnswer, self.corr_answer))

                            ans_transed = self.find_word(
                                self.tra_status, self.MyAnswer)
                            if ans_transed:
                                self.t.insert(END, '\n\n查询结果：\n')
                                for i, j in ans_transed:
                                    self.t.insert(END, '\n'+'\n'.join(
                                        ['%s No.%d' % (i, j), self.dd_all[i]['eng'][j], self.dd_all[i]['detail'][j]])+'\n')

                            else:
                                self.t.insert(END, '\n\n未在数据库中查询到结果')

                            if self.ivar1.get():
                                try:
                                    yd_trans = translate(self.MyAnswer)
                                    self.t.insert(
                                        END, '\n\n\n您的答案在有道词典的解释：\n%s' % yd_trans)
                                except requests.exceptions.ConnectionError:
                                    self.t.insert(
                                        END, '\n\n\n您的答案在有道词典的解释：\n\n<!网络未连接，请检查您的网络连接>\n')

                    else:
                        self.t.insert(END, '\n\nThe correct answer is:\n\n%s' %
                                      self.corr_answer)
                        if self.ivar1.get():
                            try:
                                self.t.insert(END, '\n\n\n在有道词典的解释：\n%s' %
                                              translate(self.letter_ori))
                            except requests.exceptions.ConnectionError:
                                self.t.insert(END, '\n\n<!网络未连接，请检查您的网络连接>\n')

                else:
                    if self.ivar1.get():
                        try:
                            self.t.insert(END, '\n\n\n在有道词典的解释：\n%s' %
                                          translate(self.letter_ori))
                        except requests.exceptions.ConnectionError:
                            self.t.insert(END, '\n\n<!网络未连接，请检查您的网络连接>\n')
        except Exception:
            self.t.insert(END, '请点击“Start”按钮以开始\n\n')

    def start_call(self, event=None):
        self.num = 0
        self.svar.set('')

        self.uni_status = self.unit_op.get(ACTIVE)
        self.tra_status = self.trans_op.get(ACTIVE)

        if self.tra_status == '英>汉':
            self.orig_text.config(font=('Times New Roman', 18, 'italic'))
            self.trans_from = 'eng'
            self.trans_to = 'ch'
        elif self.tra_status == '汉>英':
            self.orig_text.config(font=('幼圆', 18))
            self.trans_from = 'ch'
            self.trans_to = 'eng'

        self.sht = self.uni_status
        self.dd = self.dd_all[self.sht]

        self.ds = self.dd.sample(frac=1).reset_index(drop=True)
        self.letter_info = self.ds.shape

        self.letter_ori = self.ds[self.trans_from][self.num]

        self.orig_text.config(text=self.letter_ori)
        self.t.delete(1.0, END)
        self.t.insert(END, self.uni_status+'\n'+self.tra_status+'\n')
        #self.t.insert(END, '\n'+str(self.ds))

        if self.ivar2.get():
            self.check_call()
            if self.ivar1.get():
                try:
                    self.t.insert(END, '\n\n\n在有道词典的解释：\n%s' %
                                  translate(self.letter_ori))
                except requests.exceptions.ConnectionError:
                    self.t.insert(END, '\n\n<!网络未连接，请检查您的网络连接>\n')

    def find_word(self, method, word):
        res = []
        for i in self.units:
            if i.endswith('-w'):
                for j in range(1, self.dd_all[i].shape[0]+1):
                    if word_match(word, self.dd_all[i]['ch'][j]) or word_match(word, self.dd_all[i]['eng'][j]):
                        res.append((i, j))

        return res

    def keytest(self, event=None):
        self.t.delete(1.0, END)
        self.t.insert(1.0, event)


root = Tk()
root.title('背单词')
#root.iconphoto(True, PhotoImage(file = 'English.png'))
root.geometry('1080x720')
app = application(master=root)
root.mainloop()
