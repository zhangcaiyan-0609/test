
# 优化excel模块：1.增加open 函数，2.利用列表推导式简化代码
import openpyxl
class Excel:
    def __init__(self,filename,sheet_name):
        self.filename = filename
        self.sheet_name = sheet_name
    def open(self):
        self.wb = openpyxl.load_workbook(self.filename)
        # 第二步：选择文件中的表单
        self.sh = self.wb[self.sheet_name]
        # 一次性读取表
    def read_data(self):
        # 第一步：将excel文件加载到一个工作簿对象中
        self.open()
        res = list(self.sh.rows)
        # 获取第一行的单元格
        '''
        title = []
        for i in res[0]:
            title.append(i.value)
        '''
        title =[i.value for i in res[0]]
        cases_data =[]
        for item in res[1:]:
            data =[c.value for c in item]
            case = dict(zip(title,data))
            cases_data.append(case)
        return cases_data

    def write_data(self, row, column, value):
        self.open()
        self.sh.cell(row=row,column=column,value=value)
        self.wb.save(self.filename)

