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

def mkdir_name():
    df = pd.read_csv('name.csv', index_col='name')
    for name in df.index:
        path = os.path.join('save_pic', name)
        if os.path.exists(path):
            print(name + ' folder exits')
        else:
            os.mkdir(path)    # 生成每个优优名字的文件夹
            print(name + ' folder generated')

def run_one():
    mkdir_name()
    df = pd.read_csv('name.csv', index_col='name')
    name = input('输入优优名字：\n')
    url = df['url'][name]
    get_page_lst(name, url)

def run_all():    # 获取文件中的通用作品url，并启动程序
    mkdir_name()
    df = pd.read_csv('name.csv', index_col='name')
    for name, url in zip(df.index, df['url']):
        print('begin ' + name)
        get_page_lst(name, url)

def get_page_lst(name, url):    # 获取每个优优的作品页列表
    page_lst = []
    num = 1
    path = os.path.join('save_pic', name)
    session = HTMLSession()
    path = os.path.join('save_pic', name)
    avatar_img(name, url, path)
    while True:
        page = url + str(num)
        r = session.get(page)
        if r.status_code == 404:    # 没有此页面
            print('parsing html...')
            get_work_urls(page_lst, name, path)
            print('Download Completed!')
            break
        else:
            page_lst.append(page)
            num += 1

def avatar_img(name, url, path):    # 保存头像，其属性和作品使用的不一样，单独获取
    homepage = url + '1'
    session = HTMLSession()
    r = session.get(homepage)
    img_ele = r.html.find('#waterfall > div:nth-child(1) > div > div.photo-frame > img', first=True)     # 获取图片元素
    img_url = img_ele.attrs['src']    # 使用attrs属性方法获取图片元素中图片的资源链接
    r_img = session.get(img_url)
    avatar_name = os.path.join(path, name) + '.jpg'
    if os.patg.exists(avatar_name):
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
                work_url = item.find('a.movie-box')[0].attrs['href']
                save_pic(work_url, name, path)
            except IndexError:
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
                   '1.选择下载\n'
                   '2.下载全部\n')
    if method == '1':
        run_one()
    elif method == '2':
        run_all()
    else:
        exit('bye!')

