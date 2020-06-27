import os
import datetime
import shutil
import xlwt
import xlrd
from xlutils.copy import copy


def get_file_name():
    last = len(files) - 1  # 最新的工单
    file = files[last]
    month = int(file[0:2])  # 工单月份
    day = int(file[2:4])  # 工单日

    if len(files) == 0 or day < int(dl[2]) or month < int(dl[1]):  # 当前路径为空目录时或者新的一天的第一张工单
        file = str(dl[1]) + str(dl[2]) + '01'  # 新工单的文件名为当前日期+“01”

    else:  # 上面的条件不满足说明当前日期和工单上的日期一样，则需要递增工单序号

        file_index = file[4:6]  # 获得工单序号(最后两位)
        index = int(file_index)
        ds = None
        if index + 1 < 10:  # 递增+1后的工单序号如果小于10要在前面加0
            ds = '0' + str(index + 1)
        else:
            ds = str(index + 1)

        file = file[0:4] + ds + '.doc'  # 新单号用处理后的取代旧的最后两位

    return file


def create():
    last = len(files) - 1
    des = get_file_name()
    source = files[last]
    shutil.copyfile(source, des)
    odd = odd_prefix + dl[0] + dl[1] + des[0:6]
    print('成功创建工单文件:%s, 工单号:%s' % (des, odd))
    print('工单文件内容需要手动更改')
    save_odd(odd)


def save_odd(odd):  # 保存工单号到excel文件
    excel_file = 'odd.xls'
    if os.path.exists(excel_file):  # 如果存在工单excel文件直接追加内容
        r_excel = xlrd.open_workbook(excel_file)
        rows = r_excel.sheets()[0].nrows
        excel = copy(r_excel)
        table = excel.get_sheet(0)
        next_row = rows
        table.write(next_row, 0, odd)
        excel.save(excel_file)
    else:  # 不存在，新创建工单excel文件
        book = xlwt.Workbook()
        table = book.add_sheet('Over', cell_overwrite_ok=True)
        sheet = book.add_sheet('Sheet1')  # 添加工作页
        table.write(0, 0, odd)
        book.save(filename_or_stream=excel_file)

    print('工单号已保存')


dl = []
files = []

today = datetime.date.today()  # 当前日期
dl = str(today).split('-')
default_path = os.getcwd()
test_path = r'D:\运维\2020年3月'
odd_prefix = 'YWGD'  # 单号前缀,可根据实际修改

for f in os.listdir(default_path):  # 获得当前路径所有工单文件名
    file_suffix = os.path.splitext(f)[1]
    if file_suffix == '.doc' or file_suffix == '.docx':
        files.append(f)

create()
