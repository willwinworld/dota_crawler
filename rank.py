# -*- coding: utf-8 -*-
import requests
from pyquery import PyQuery as pq

  # 最终结果字典，先为了获取各个玩家的排名，姓名，战队名，天梯分数，这个跟之前的dota有点不太一样


def get_all_player(url):
    r = requests.get(url)  #获取链接，赋给了r这个变量，r就是一个对象,人类就是一个类,具体的人就是对象
    d = pq(r.text)      #pq是一个函数，d是变量也是函数
    #ladder_url_list = []    #所有天梯玩家子链接URL的列表容器
    final_list = []
    player_nodes = d('.container.xuning-box .table.table-list.table-text tr')    #所以才可以往d里面传参数
    for node in player_nodes:
        dollar = pq(node)
        name = dollar('td:eq(3) span:eq(0)').text() #获得玩家名字，这个有点拿不准，重点检查！
        rank = dollar('td:eq(0)').text() #获取玩家现在排名，不是最高排名
        group = dollar('td:eq(4)').text() #获取玩家战队
        max_score = dollar('td:eq(6)').text() #获取玩家最高积分 
        url_str = dollar.attr('onclick')
        if url_str: # 第42位玩家ana没有资料，要剔除，或者直接在选择器里剔除因为它的tr里没有onclick属性，直接tr[onclick]
            url = 'http://www.dotamax.com/player/detail/' + url_str.split('/')[-2]
            #ladder_url_list.append(url)
            final_list.append({'name':name, 'rank':rank, 'group':group,'max_score':max_score, 'url':url})
        else:
            final_list.append({'name':name, 'rank':rank, 'group':group,'max_score':max_score, 'url':''})
    return final_list

def get_player_detail(url):  #第二个函数目的主要是读每个玩家的常用英雄的具体信息
    r = requests.get(url)
    d = pq(r.text)
    regular_heroes_list = []
    player_info_nodes = d('.flat-grey-box:eq(0) .table.table-list.table-thead-left .table-player-detail tr')
    for hero_node in player_info_nodes:
        dollar = pq(hero_node)
        hero_name = dollar('td:eq(0) a').text()
        hero_counts = dollar('td:eq(1) div:eq(0)').text()
        winning_rate = dollar('td:eq(2) div:eq(0)').text()
        average_kda = dollar('td:eq(4) div:eq(0)').text()
        regular_heroes_list.append({'common_hero':hero_name, 'hero_counts':hero_counts, 'winning_rate':winning_rate,'average_kda':average_kda})       
    return regular_heroes_list

def run():
    all_player = get_all_player('http://www.dotamax.com/ladder/') #两个参数去接收ladder_result_list和result_list,返回的是列表
    final_result = []
    for player_info in all_player[:4]: #singal_player_info是一个个字典
        print player_info['url']
        name = player_info['name']
        rank = player_info['rank']
        group = player_info['group']
        max_score = player_info['max_score']
        if player_info['url']:
            detail_info = get_player_detail(player_info['url'])
        else:
            detail_info = []
        final_result.append({'rank':rank, 'name':name, 'group':group, 'max_score':max_score, 'normal_heroes':detail_info})
    return final_result    


sss = run()
print sss


        
   
  
        
        
        
                
       
