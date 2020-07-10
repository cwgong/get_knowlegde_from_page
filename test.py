# import io
import json
# with io.open('./json_data_/1205702212.json','r',encoding='utf-8') as f:
#     # p = f.readline()
#     t = json.load(f)
#     print(t)

import os

# allFileNum = 0
#
#
# def printPath(level, path):
#     global allFileNum
#     '''''
#     打印一个目录下的所有文件夹和文件
#     '''
#     # 所有文件夹，第一个字段是次目录的级别
#     dirList = []
#     # 所有文件
#     fileList = []
#     # 返回一个列表，其中包含在目录条目的名称
#     files = os.listdir(path)
#     # 先添加目录级别
#     dirList.append(str(level))
#     for f in files:
#         if (os.path.isdir(path + '/' + f)):
#             # 排除隐藏文件夹。因为隐藏文件夹过多
#             if (f[0] == '.'):
#                 pass
#             else:
#                 # 添加非隐藏文件夹
#                 dirList.append(f)
#         if (os.path.isfile(path + '/' + f)):
#             # 添加文件
#             fileList.append(f)
#     # 当一个标志使用，文件夹列表第一个级别不打印
#     i_dl = 0
#     for dl in dirList:
#         if (i_dl == 0):
#             i_dl = i_dl + 1
#         else:
#             # 打印至控制台，不是第一个的目录
#             print('-' * (int(dirList[0])), dl)
#             # 打印目录下的所有文件夹和文件，目录级别+1
#             printPath((int(dirList[0]) + 1), path + '/' + dl)
#     for fl in fileList:
#         # 打印文件
#         print(fl)
#         f = open('C:/Users/DELL/Desktop/userid3/' + fl)  # 读取完txt再读txt里面的类容
#         # print(f.read())
#         # 'a'表示附加模式，用写入模式‘w'要小心，如果指定文件已经存在，python将再返回文件对象前清空该文件
#         f2 = open("20170610uid.txt", 'a')
#         f2.write(f.read())
#         # 以下三行是逐行读取，跟f2.write(f.read())效果一样
#         # alllines = f.readlines()
#         # for eachLine in alllines:
#         #   f2.write(eachLine)
#         f2.close()
#         # 随便计算一下有多少个文件
#         allFileNum = allFileNum + 1
#         print(allFileNum)
#
#
# if __name__ == '__main__':
#     printPath(1, 'C:/Users/DELL/Desktop/userid3/')

# path = './pdf_data'
# def get_file(path):  # 获取文件路径
#     file_list = []
#     for root, dirs, files in os.walk(path):
#
#         for file in files:
#             print(file)     #文件名
#             # print(os.path.join(root, file))
#             file_list.append(os.path.join(root, file))
#     return file_list
#
#
# result = get_file(path)
# print(result)
# print(type(result))

with open('./a.json','r',encoding='utf-8') as f:
    t = json.load(f)
    print(t)
    print(type(t))
