#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Name:         old_driver_spider
Copyright:    snow
Version:      1.0
Email:        snowi@protonmail.com
'''

import os
import pandas as pd
from requests_html import HTMLSession

def mkdir_name(file_name):
    df = pd.read_csv(file_name, index_col='name')
    for name in df.index:
        path = os.path.join('save_pic', name)
        if os.path.exists(path):
            print(name + ' folder exits')
        else:
            os.mkdir(path)    # 生成每个名字的文件夹
            print(name + ' folder generated')

def run(file_name, method):
    df = pd.read_csv(file_name, index_col='name')
    mkdir_name(file_name)
    select = input('输入序号：\n'
                   '1.选择名称下载\n'
                   '2.下载全部(不推荐)\n')
    if select == '1':
        name = input('输入名字：')
        path = os.path.join('save_pic', name)
        url = df['url'][name]
        if method == '1':
            avatar_img(name, url, path)
        else:
            pass
        get_page_lst(name, url, path)
    elif select == '2':
        for name, url in zip(df.index, df['url']):
            print('begin ' + name)
            path = os.path.join('save_pic', name)
            if method == '1':
                avatar_img(name, url, path)
            else:
                pass
            get_page_lst(name, url, path)
    else:
        exit('wrong selection')

def run_search(name, url, path):
    if os.path.exists(path):
        print(name + ' folder exits')
    else:
        os.mkdir(path)
        print(name + ' folder generated')
    get_page_lst(name, url, path)   # 搜索的结果超出页数不是返回404，而是页面显示搜索没有结果

def get_page_lst(name, url, path):    # 获取每个优优的作品页列表
    page_lst = []
    num = 1
    session = HTMLSession()
    while True:
        page = url + str(num)
        r = session.get(page)
        if (r.status_code == 404) or r.html.find('div.alert.alert-danger'):    # 没有此页面
            print('parsing html...')
            get_work_urls(page_lst, name, path)
            print('Download Completed!')
            break
        else:
            page_lst.append(page)
            #print(page_lst)
            num += 1

def avatar_img(name, url, path):    # 保存头像，其属性和作品使用的不一样，单独获取
    homepage = url + '1'
    session = HTMLSession()
    r = session.get(homepage)
    img_ele = r.html.find('#waterfall > div:nth-child(1) > div > div.photo-frame > img', first=True)     # 获取图片元素
    img_url = img_ele.attrs['src']    # 使用attrs属性方法获取图片元素中图片的资源链接
    r_img = session.get(img_url)
    avatar_name = os.path.join(path, name) + '.jpg'    # 如果不使用os.chdir，则需要在创建文件时使用完整相对路径
    if os.path.exists(avatar_name):
        print(avatar_name + 'exists')
    else:
        with open(avatar_name, 'wb') as f:
            f.write(r_img.content)
            print('avatar saved')

def get_work_urls(page_lst, name, path):    # 获取每一页的所有作品对应网页
    session = HTMLSession()
    for page in page_lst:
        r = session.get(page)
        work_list = r.html.find('div.item')
        for item in work_list:
            try:
                work_url = item.find('a.movie-box')[0].attrs['href']  # 在find生成的列表中取出ele元素，再找出作品页面链接，及元素的'href'属性值
                save_pic(work_url, name, path)
            except IndexError:  # 演员页面的第一个元素是头像，没有a.movie-box属性，生成的空列表
                print('pass avatar image')

def save_pic(work_url, name, path):    # 解析作品页面
    session = HTMLSession()
    r = session.get(work_url)
    img_ele = r.html.find('body > div.container > div.row.movie > div.col-md-9.screencap > a', first=True)
    img_url = img_ele.attrs['href']
    img_title = img_ele.attrs['title']
    r_img = session.get(img_url)
    img_name = img_title.replace('*','').replace('?','').replace(':','')    # 文件名不能有*等特殊符号，使用链式替换
    file_name = os.path.join(path, img_name) + '.jpg'
    if os.path.exists(file_name):
        print(img_name + '  exists')
    else:
        with open(file_name, 'wb') as f:
            f.write(r_img.content)
            print(img_name + '.jpg')

if __name__ == '__main__':
    method = input('输入序号：\n'
                   '1.根据演员下载\n'
                   '2.根据类别下载\n'
                   '3.根据系列下载\n'
                   '4.根据制作商下载\n'
                   '5.根据发行商下载\n'
                   '6.根据搜索下载\n')
    file_name = 'name_actress.csv' if method == '1' else 'name_genre.csv' if method == '2'\
                else 'name_series.csv' if method == '3' else 'name_studio.csv' if method == '4'\
                else 'name_label.csv' if method == '5' else None
    if method in ['1', '2', '3', '4', '5']:
        run(file_name, method)
    elif method == '6':
        name = input('输入搜索内容：')
        url = 'https://javlog.com/cn/search/' + name + '/page/'
        path = os.path.join('save_pic', name)
        run_search(name, url, path)
    else:
        exit('bye!')

