# -*- coding: utf-8 -*-

# 最终目标：[{'斯拉达':{'攻击类型'：近战，'定位':[核心 - 耐久 - 控制 - 先手],'阵营':夜魇,'其它简称'：大鱼人}}]
# 需要两个列表，两个字典
#先把属性加到属性字典中（至于定位的列表可以最后加入），再把属性字典加到英雄字典中，最后把英雄字典加到结果列表中

import requests
from pyquery import PyQuery as pq
import time #反爬虫的方法

def open(url): 
    r = requests.get(url) #想象一个黑盒子，输入的是URL（获取的是URL）
    d = pq(r.text) #获得是当前页面的HTML，即当前页面的内容
    heros_url_list = []
    heros_node = d('.bg .r_bar_bg .hero_list .heroPickerIconLink') #扫描（获取）所有英雄的URL
    for hero_node in heros_node:
        heros_url_list.append(pq(hero_node).attr('href')) #<a id="link_earthshaker" class="heroPickerIconLink" target="_blank" href="http://db.dota2.com.cn/hero/earthshaker/">    
    return heros_url_list                                 #这是撼地者的URL，要获取的是href里的URL，在a标签里面，所以可以attr获取，只要在a标签里，其他属性id,class,target,href都可以用attr去获得

def read_heros_nature(url):
    r = requests.get(url)
    print url #方便调试
    time.sleep(0.5） #以0.5的间隔去打印去打印
    d = pq(r.text)
    position_list = [] #定位列表
    hero_dict = {} #每个英雄的字典
    nature_dict = {} #每个英雄属性的字典
    heros_node = d('.hero_info')
    for node in heros_node:
        dollar = pq(node)
        name = dollar('.hero_name').text() #英雄名
        attack_type = dollar('.info_p:eq(0)').text() #攻击类型
        position = dollar('.info_p:eq(1)').text() #定位列表最后加入
        side = dollar('.info_p:eq(2)').text()  #阵营
        other_names = dollar('.info_p:eq(3)').text() #其它简称
        position_list.append(position) #将定位内容加入定位列表中
        nature_dict.update({'attack_type':attack_type, 'position':position, 'side':side, 'other_names':other_names})#将英雄属性字典加到英雄字典中
        x = nature_dict
        hero_dict = {name:x} #字典的key是独一无二的，key不一定非要是字符串
    return hero_dict

#定义慢函数，将上面两个函数结合起来，思路是调用第一个函数，得到所有子链接，遍历所有子链接，调用第二个函数得到结果  
#a = open('http://www.dota2.com.cn/heroes/') #a是所有英雄子页面的URL链接列表
#def run():
    #for i in a:
       #result = read_heros_nature(i)
    #return result


#sss = read_heros_nature('http://db.dota2.com.cn/hero/shadow_fiend/')
#print sss

def run():
    hero_urls = open('http://www.dota2.com.cn/heroes/')
    final_result = []
    for url in hero_urls: #a是所有英雄子页面的URL链接列表，那么遍历的i就是各个英雄URL的字符串
       nature = read_heros_nature(url)
       final_result.append(nature)
    return final_result


if __name__ == "__main__":  #调试的一种方法 #关键要搞清楚字典取keys时返回的是列表
    res = run() #a是一个列表啊
    for i in res:  #遍历所有英雄最终结果的列表，i是单个英雄的字典
       hero_name = i.keys()[0] #获得单个英雄的名字
       print hero_name.encode('gbk', 'ignore')
       hero_nature_list = i.values() #获得单个英雄名字所对应的values，返回的是一个列表
       hero_nature_list22 = hero_nature_list[0].values()
       for i in hero_nature_list22:
           print i.encode('gbk', 'ignore')
       print
