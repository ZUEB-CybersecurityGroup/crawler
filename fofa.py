import csv
import re

import requests
import yaml


class Fofa():
    def __init__(self):
        # self.url = ''
        self.headers = {
            "Cookie": self.getcookie(),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76"
        }
        self.result=[]

    def get_url(self):
        response = requests.get(url=input("请输入详情页："), headers=self.headers)
        return response

    # 解析函数，利用正则表达式提取出想要的信息
    def parse(self):
        response = self.get_url()
        temp_list = []
        # 提取链接
        try:
            result_urls = re.findall(r'<a href="(.*?)" target="_blank">', response.text)
            temp_list = list(zip(result_urls,))

        except:
            print("未获取到数据，请检查网络情况")
            exit()
        return temp_list

    # 保存函数，将结果保存在result.csv文件中
    def save(self,list):
        # csv文件的表头
        header = ["漏洞域名"]
        with open('result.csv', 'w', encoding='utf8',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for i in list:
                writer.writerow([i])
        print("内容保存在result.csv中")

    def getcookie(self):
        with open('fofa_cookie.yml', 'r') as file:
            config = yaml.safe_load(file)
            if config.get('Cookie') == '':
                print('请先配置Cookie')
            else:
                return config.get('Cookie')

    def mian(self):
        self.save(self.parse())

if __name__ == '__main__':
    fofa = Fofa()
    fofa.mian()