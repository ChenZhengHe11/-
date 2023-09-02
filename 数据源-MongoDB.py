import time
import requests
import json
import csv
import os
import pymongo


class Control_line:
    def __init__(self):

        self.client = pymongo.MongoClient()
        self.collection = self.client['计算机网络-课设']['省控线-2023年']

        # with open('有效网址.csv', 'a', encoding='utf-8', newline='')as csvfile:
        #     self.fieldnames = ['网址']
        #     self.write = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
        #     self.write.writeheader()

        self.province_ids = {"11": '北京', '12': '天津', '13': '河北', '14': '山西', '15': '内蒙古', '21': '辽宁', '22': '吉林',
                        '23': '黑龙江', '31': '上海', '32': '江苏', '33': '浙江', '34': '安徽', '35': '福建', '36': '江西', '37': '山东',
                        '41': '河南', '42': '湖北', '43': '湖南', '44': '广东', '45': '广西', '46': '海南', '50': '重庆', '51': '四川',
                        '52': '贵州', '53': '云南', '54':'西藏', '61': '陕西', '62': '甘肃', '63': '青海', '64': '宁夏', '65':'新疆'}

        self.url = 'https://static-data.gaokao.cn/www/2.0/proprovince/{}/pro.json'

        self.headers = {
            "Accept": "",
            "application/json,": "text/plain, */*",
            "Accept-Encoding": "",
            "gzip,": "deflate, br",
            "Accept-Language": "",
            "zh-CN,zh;q=0.9,en;q=0.8": "",
            "Cache-Control": "",
            "no-cache": "&",
            "Origin": "",
            "https": "//www.gaokao.cn&//www.gaokao.cn/",
            "Pragma": "",
            "Referer": "",
            "Sec-Ch-Ua": "",
            "\"Not.A/Brand\";v=\"8\",": "\"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
            "Sec-Ch-Ua-Mobile": "",
            "?0": "",
            "Sec-Ch-Ua-Platform": "",
            "\"Windows\"": "",
            "Sec-Fetch-Dest": "",
            "empty": "",
            "Sec-Fetch-Mode": "",
            "cors": "",
            "Sec-Fetch-Site": "",
            "same-site": "",
            "User-Agent": "",
            "Mozilla/5.0": "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

    def get_data(self, id):
        response = requests.get(url=self.url.format(id), headers=self.headers)
        res_json = response.json()
        self.parse_data(res_json)

    def parse_data(self, res_json):
        specialplan_list = res_json['data']['2023']
        list_s = list(specialplan_list.keys())
        for node in list_s:
            datas = specialplan_list[f'{node}']
            for i in range(0, len(datas)):
                item = {}
                item['地区'] = datas[i]['province']
                item['年份'] = datas[i]['year']
                item['考生类别'] = datas[i]['type_name']
                item['批次'] = datas[i]['name']
                item['分数线'] = datas[i]['score']
                item['位次'] = datas[i]['score_section']
                if datas[i]['major_score'] != '0.00':
                    item['专业分'] = datas[i]['major_score']
                else:
                    item['专业分'] = '-'

                # 使用省份名称作为集合名称，插入数据到对应集合中
                province = datas[i]['province']
                collection = self.collection[f"{province}"]
                collection.insert_one(item)

    def get_province_by_id(self, province_id):
        province = None
        for pid, p in self.province_ids.items():
            # print(p)
            if pid == province_id:
                province = p
                break
        return province

    def run(self):
        # self.get_data()
        keys = list(self.province_ids.keys())  # 转换为列表
        for key in keys:
            # print(key)
            self.get_data(key)


if __name__ == '__main__':
    t_start = time.time()
    print(t_start)
    r = Control_line()
    r.run()
    t_end = time.time()
    print(f'程序运行总时间：{t_end-t_start}')