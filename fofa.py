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
        self.result = []

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
            result_ip_domain = re.findall(r'class="hsxa-jump-a">(.*?)</a>', response.text)
            temp_list = []
            i = 0
            while result_urls:
                # 从list1中取出一个元素
                item_from_list1 = result_urls.pop(0)
                # 从list2中取出五个元素
                items_from_list2 = result_ip_domain[i:i + 5]
                # 合并成一个新的列表
                merged_item = [item_from_list1] + items_from_list2
                # 添加到合并后的列表
                temp_list.append(merged_item)
                i += 5
        except:
            print("未获取到数据，请检查网络情况")
            exit()
        return temp_list

    # 保存函数，将结果保存在result.csv文件中
    def save(self, list):
        # csv文件的表头
        header = ["漏洞域名", "IP地址", "国家", "ASN", "组织", "主域"]
        with open('result.csv', 'w', encoding='GBK', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(list)
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
