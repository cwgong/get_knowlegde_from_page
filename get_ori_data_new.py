# -*- coding: utf-8 -*-

import pymysql
import json
import time
import io
import requests
import datetime
'''
获取原始数据，其中包含公司信息、 pdf url链接信息等
'''

# 把datetime类型转为时间戳形式(毫秒)
def datetime_toTimestamp(dt):
    return int(time.mktime(dt.timetuple())*1000)

# 把时间戳转为固定字符串格式
def timestamp_to_date(timestamp):
    timeArray = time.localtime(timestamp/1000)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

# 获取 A股董事会决议相关数据
def get_board_meeting(start, end):
    
    host = '10.0.0.95'
    port = 3306
    db='datacenter_pub'
    user='product'
    password='easy2get'
    
    connection = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset='utf8')
    cursor = connection.cursor()

    sql = "SELECT t.text_id, t.sec_code, t.mar_type, t.sec_name, t.pub_date, t.ann_title, t.info_type, t.ann_url FROM ann_info_tab_news t WHERE t.ann_title LIKE '%决议%' AND t.ann_title LIKE '%董事会%' AND t.update_at>='{}' AND t.update_at<'{}'".format(start, end)
    
    cursor.execute(sql)
    result = cursor.fetchall()
    
    y = []
    for data in result:
        pub_date = data[4] # type = datetime
        timestamp = datetime_toTimestamp(pub_date)
        # print(timestamp_to_date(timestamp)) # 已验证
        temp_dic = {'text_id': data[0],
                    'sec_code': data[1],
                    'mar_type': data[2],
                    'sec_name': data[3],
                    'pub_date': timestamp,
                    'ann_title': data[5],
                    'info_type': data[6],
                    'ann_url': data[7]}
        y.append(temp_dic)

    # 关闭数据连接
    connection.close()
    return y

# 获取 A股股东大会决议相关数据
def get_shareholders_meeting(start, end):
    
    host = '10.0.0.95'
    port = 3306
    db='datacenter_pub'
    user='product'
    password='easy2get'
    
    connection = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset='utf8')
    cursor = connection.cursor()

    sql = "SELECT t.text_id, t.sec_code, t.mar_type, t.sec_name, t.pub_date, t.ann_title, t.info_type, t.ann_url FROM ann_info_tab_news t WHERE t.ann_title LIKE '%决议%' AND t.ann_title LIKE '%股东大会%' AND t.update_at>='{}' AND t.update_at<'{}'".format(start, end)
    
    cursor.execute(sql)
    result = cursor.fetchall()
    
    y = []
    for data in result:
        pub_date = data[4] # type = datetime
        timestamp = datetime_toTimestamp(pub_date)
        # print(timestamp_to_date(timestamp)) # 已验证
        temp_dic = {'text_id': data[0],
                    'sec_code': data[1],
                    'mar_type': data[2],
                    'sec_name': data[3],
                    'pub_date': timestamp,
                    'ann_title': data[5],
                    'info_type': data[6],
                    'ann_url': data[7]}
        y.append(temp_dic)
    # 关闭数据连接
    connection.close()
    return y


def get_bond_prospectus(start, end):
    host = '10.0.0.95'
    port = 3306
    db = 'datacenter_pub'
    user = 'product'    #这是本地连接的，从生产连需要其他账号密码
    password = 'easy2get'

    connection = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset='utf8')
    cursor = connection.cursor()

    # sql = "SELECT t.text_id, t.sec_code, t.mar_type, t.sec_name, t.pub_date, t.ann_title, t.info_type, t.ann_url FROM ann_info_tab_news t WHERE t.ann_title LIKE '%说明书%' AND t.ann_title LIKE '%债券募集%' AND t.update_at>='{}' AND t.update_at<'{}'".format(
    #     start, end)
    sql = " SELECT t.textid, t.sec_code, t.mar_type, t.sec_name, t.pub_date, t.ann_title, t.info_type, t.ann_url FROM dw.stk_ann_classify_info t WHERE t.ann_group = '发行情况报告书' AND t.mod_time >= '{}' and t.mod_time <= '{}' ".format(start, end)
    sql = " SELECT t.textid, t.sec_code, t.mar_type, t.sec_name, t.pub_date, t.ann_title, t.info_type, t.ann_url, t.uniqueid FROM dw.stk_ann_classify_info t WHERE t.ann_group = '合作设立产业并购基金公告' AND t.mod_time >= '{}' and t.mod_time <= '{}' ".format(
        start, end)
    cursor.execute(sql)
    result = cursor.fetchall()

    y = []
    for data in result:
        pub_date = data[4]  # type = datetime
        # print(pub_date)

        ss = str(pub_date)
        yy = ss[0] + ss[1] + ss[2] + ss[3]
        m = ss[4] + ss[5]
        d = ss[6] + ss[7]
        dd = yy + '-' + m + '-' + d
        # print(dd)
        # print(type(dd))
        pub_date = datetime.date(*map(int, dd.split('-')))

        timestamp = datetime_toTimestamp(pub_date)
        # print(timestamp_to_date(timestamp)) # 已验证
        temp_dic = {'text_id': data[0],
                    'sec_code': data[1],
                    'mar_type': data[2],
                    'sec_name': data[3],
                    'pub_date': timestamp,
                    'ann_title': data[5],
                    'info_type': data[6],
                    'ann_url': data[7],
                    'uniqueid':data[8]}
        y.append(temp_dic)
    # 关闭数据连接
    connection.close()
    return y
    
    
def pdf_to_json(ann_url):
    url = 'http://10.0.0.86:10002/analysis'
    params = {'pdf_url': ann_url}
    try:
        response = requests.get(url, params = params)
        response = response.json()
        return response
    except:
        print("Find A Error!")
        print(ann_url)
        return {}

def get_pdf(pdf_url, file_path, c=1):

    try:
        r = requests.get(pdf_url)
        f = io.open(file_path, "wb")
        f.write(r.content)
        f.close()
    except:
        if c < 6:
            c += 1
            print("get_pdf() again!")
            get_pdf(pdf_url, file_path, c)
        print("get_pdf() error!")


def mk_name(url):
    commas = ['.',':','/','?','=','&']
    for comma in commas:
        url = url.replace(comma,'')
    name = url
    return name

def upload_file_1(url,text_id):
    name_pdf = './pdf_data_new_2/' + str(text_id).replace('.','') + '.pdf'
    get_pdf(url, name_pdf)

def upload_file_2(url,text_id):
    name_pdf = './pdf_data_new_3/' + str(text_id).replace('.','') + '.pdf'
    get_pdf(url, name_pdf)

def upload_file(url,text_id):
    name_pdf = './pdf_data_new_1/' + str(text_id).replace('.','') + '.pdf'
    get_pdf(url, name_pdf)

def upload_file_3(url,text_id):
    name_pdf = './pdf_data_new_4/' + str(text_id).replace('.','') + '.pdf'
    get_pdf(url, name_pdf)

if __name__ == "__main__":
    
    # start = '1569859200000' #
    # start = '1546272000000'
    start = 20190101
    start_1 = 20190502
    start_2 = 20190902
    # start = 20170101
    # end = '1574784000000'
    # end = '1577808000000'
    end = 20190501
    end_1 = 20190901
    end_2 = 20200101
    # end  =20200101
    # data = get_board_meeting(start, end)
    # print(len(data))
    # data = get_shareholders_meeting(start, end)
    #     # print(len(data))


    data = get_bond_prospectus(start, end)
    print(len(data))
    text_list = []
    for p in data:
        # print(p)
        # print('----------------------------')
        if p['sec_name'] != '':
            # name_pdf = str(p['text_id']) + '.pdf'
            # text_list.append(name_pdf)
            p['uniqueid'] = p['uniqueid'].replace('.','')
            text_list.append(p)
    print(len(text_list))
    # for x in text_list[0:10]:
    #     print(x)
    # print(text_list[0])
    with open('./long_1.json','w',encoding='utf-8') as f:
        json.dump(text_list,f,ensure_ascii=False)

    # for text in text_list:
    #     upload_file(text['ann_url'],text['uniqueid'])
    #     print(text)
    #     # print(text)
    # print("Upload Finish!")

    data_1 = get_bond_prospectus(start_1, end_1)
    print(len(data_1))
    text_list_1 = []
    for p in data_1:
        # print(p)
        # print('----------------------------')
        if p['sec_name'] != '':
            # name_pdf = str(p['text_id']) + '.pdf'
            # text_list.append(name_pdf)
            p['uniqueid'] = p['uniqueid'].replace('.', '')
            text_list_1.append(p)

    with open('./long_2.json','w',encoding='utf-8') as f:
        json.dump(text_list_1,f,ensure_ascii=False)

    # for text in text_list_1:
    #     upload_file_1(text['ann_url'],text['uniqueid'])
    # print("Upload Finish!")
    #
    data_2 = get_bond_prospectus(start_2, end_2)
    print(len(data_2))
    text_list_2 = []
    for p in data_2:
        # print(p)
        # print('----------------------------')
        if p['sec_name'] != '':
            # name_pdf = str(p['text_id']) + '.pdf'
            # text_list.append(name_pdf)
            p['uniqueid'] = p['uniqueid'].replace('.', '')
            text_list_2.append(p)
    #
    with open('./long_3.json','w',encoding='utf-8') as f:
        json.dump(text_list_2,f,ensure_ascii=False)
    #
    # for text in text_list_2:
    #     upload_file_2(text['ann_url'], text['uniqueid'])
    # print("Upload Finish!")

    # with open('./prospectus_info.json','w',encoding='utf-8') as f:
    #     json.dump(text_list,f,ensure_ascii=False)
        # f.write(p)
        # url = p['ann_url']
        # id = p['text_id']
        # text_dic = {'url':url,'text_id':id}
        # text_list.append(text_dic)

    # c = 0
    # for x in text_list:
    #     url = x['url']
    #     c += 1
    #     if url == 'http://static.cninfo.com.cn/finalpage/2019-10-17/1206990607.PDF':
    #         print(c)
    #         break
    #     else:
    #         continue


    # for item in text_list[0:299]:
    #     url = item['url']
    #     text_id = item['text_id']
    #     print(url)
    #     print('--------------------------')
    #     name_pdf = './pdf_data/' + str(text_id) + '.pdf'
    #     name_json = './json_data/' + str(text_id) + '.json'
    #     # print(name_pdf)
    #     # print(name_json)
    #     get_pdf(url,name_pdf)
    #     con = pdf_to_json(url)
    #     con_json = json.dumps(con, ensure_ascii=False)
    #     with open(name_json, 'w',encoding='utf-8') as f:  # 设置文件对象
    #         f.write(con_json)


    # url = 'http://static.cninfo.com.cn/finalpage/2019-11-26/1207115168.PDF'
    # text_id = 1111
    # print(url)
    # print('--------------------------')
    # name_pdf = './pdf_data_/' + str(text_id) + '.pdf'
    # name_json = './json_data_/' + str(text_id) + '.json'
    # print(name_pdf)
    # print(name_json)
    # get_file(url, name_pdf)
    #     # print(name_pdf)
    #     # con = pdf_to_json(url)
    #     # print(con)
    # con_json = json.dumps(con, ensure_ascii=False)
    # print(con_json)
    # with open(name_json, 'w', encoding='utf-8') as f:  # 设置文件对象
    #     f.write(con_json)
    # for p in data:
    #     url = p['ann_url']
    #     print(url)
    #     print('-----------------------')
    #     name_pdf = './pdf_data/' + mk_name(url) + '.pdf'
    #     name_json = './json_data/' + mk_name(url) + '.json'
    #     get_file(url, name_pdf)
    #     con = pdf_to_json(url)
    #     con_json = json.dumps(con, ensure_ascii=False)
    #     with open(name_json, 'w',encoding='utf-8') as f:  # 设置文件对象
    #         f.write(con_json)


    # print(data)1546272000  1577808000
    # for p in data:
    #     print(pdf_to_json(p['ann_url']))
    #     print('-----------------------------------------------')

    # "1202994608.pdf","1202994608.pdf","1202994608.pdf","1202994608.pdf","1202994608.pdf","1202994608.pdf","1202994608.pdf","1202994608.pdf"
    
    