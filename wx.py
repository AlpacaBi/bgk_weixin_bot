#!/usr/bin/env python3
# coding: utf-8

from wxpy import *

import requests
from json import JSONDecoder

import hashlib
import cv2
import time
import random
import os,sys
import string
import base64
import requests
import numpy as np
from urllib.parse import urlencode
import json




from aip import AipImageCensor
from aip import AipNlp
APP_ID = '11685556'
API_KEY = 'ELS0CGtNxbq15Gs0GGyP8xx8'
SECRET_KEY = 'U5U5LHnsaDcErfguBOBTlGjR107i5hku'
client = AipImageCensor(APP_ID, API_KEY, SECRET_KEY)





""" 你的 APPID AK SK """
APP_ID2 = '14895115'
API_KEY2 = 'oxGumTKpYGZfxokP7iPayTKB'
SECRET_KEY2 = 'UYlln10MWlrW3EVUH0wDYDn2TIKc9BmM'
client2 = AipNlp(APP_ID2, API_KEY2, SECRET_KEY2)





def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()








app_id = '2107740759'
app_key = 'wKHZKLMjTkxN220j'

app_id2 = '2107863903'
app_key2 = 'E9T6ifcDPqmpDvor'



app_id5 = '2107896042'
app_key5 = 'un9kJWl8yiR7TlGI'



import cv2



def get_params(img):                         #鉴权计算并返回请求参数
    #请求时间戳（秒级），用于防止请求重放（保证签名5分钟有效
    time_stamp=str(int(time.time()))
    #请求随机字符串，用于保证签名不可预测,16代表16位
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))

    params = {'app_id':app_id,                #请求包，需要根据不同的任务修改，基本相同
              'image':img,                    #文字类的任务可能是‘text’，由主函数传递进来
              'session_id':'123' ,                    #身份证件类可能是'card_type'
              'time_stamp':time_stamp,        #时间戳，都一样
              'nonce_str':nonce_str,          #随机字符串，都一样
              #'sign':''                      #签名不参与鉴权计算，只是列出来示意
             }

    sort_dict= sorted(params.items(), key=lambda item:item[0], reverse = False)  #字典排序
    sort_dict.append(('app_key',app_key))   #尾部添加appkey
    rawtext= urlencode(sort_dict).encode()  #urlencod编码
    sha = hashlib.md5()
    sha.update(rawtext)
    md5text= sha.hexdigest().upper()        #MD5加密计算
    params['sign']=md5text                  #将签名赋值到sign
    return  params                          #返回请求包



def get_params_all(img,app_id,app_key):                         #鉴权计算并返回请求参数
    #请求时间戳（秒级），用于防止请求重放（保证签名5分钟有效
    time_stamp=str(int(time.time()))
    #请求随机字符串，用于保证签名不可预测,16代表16位
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))

    params = {'app_id':app_id,                #请求包，需要根据不同的任务修改，基本相同
              'image':img,                    #文字类的任务可能是‘text’，由主函数传递进来
              'time_stamp':time_stamp,        #时间戳，都一样
              'nonce_str':nonce_str,          #随机字符串，都一样
              #'sign':''                      #签名不参与鉴权计算，只是列出来示意
             }

    sort_dict= sorted(params.items(), key=lambda item:item[0], reverse = False)  #字典排序
    sort_dict.append(('app_key',app_key))   #尾部添加appkey
    rawtext= urlencode(sort_dict).encode()  #urlencod编码
    sha = hashlib.md5()
    sha.update(rawtext)
    md5text= sha.hexdigest().upper()        #MD5加密计算
    params['sign']=md5text                  #将签名赋值到sign
    return  params                          #返回请求包

bot = Bot(cache_path=True)



tuling = Tuling(api_key='b55df5a8642c40058c9306eed9cef651')



@bot.register([Friend])
def reply_my_friend(msg):
    resm=client2.sentimentClassify(msg.text)
    ressent=resm['items'][0]['sentiment']
    respositive=resm['items'][0]['positive_prob']
    ressentt=''
    if ressent==2:
        ressentt='情感偏正向\n'
    elif ressent==1:
        ressentt='情感偏中性\n'
    else:
        ressentt='情感偏负向\n'



    respositive='情绪值：'+'{:.2f}%\n'.format(respositive*100)

    lastres=ressentt+respositive


    msg.reply(lastres)


@bot.register([Group])
def auto_reply(msg):
    if not (isinstance(msg.sender, Group) and not msg.is_at):
        tuling.do_reply(msg)




@bot.register([Friend],PICTURE)
def ai_reply(msg):

    image_name = msg.file_name

    msg.get_file('' + msg.file_name)

    f=open(image_name,'rb')

    img = base64.b64encode(f.read())   #得到API可以识别的字符串


    image = get_file_content(image_name)
    resccc=client.imageCensorUserDefined(image);


    params = get_params(img)
    url = "https://api.ai.qq.com/fcgi-bin/vision/vision_imgtotext"
    res = requests.post(url,params)
    req_con = res.content.decode('utf-8')
    req_dict = JSONDecoder().decode(req_con)




    params2 = get_params_all(img,app_id2,app_key2)
    url2 = "https://api.ai.qq.com/fcgi-bin/image/image_tag"
    res2 = requests.post(url2,params2)
    req_con2 = res2.content.decode('utf-8')
    req_dict2 = JSONDecoder().decode(req_con2)



    params5 =  get_params_all(img,app_id5,app_key5)
    url5 = "https://api.ai.qq.com/fcgi-bin/face/face_detectmultiface"
    res5 = requests.post(url5,params5)
    req_con5 = res5.content.decode('utf-8')
    req_dict5 = JSONDecoder().decode(req_con5)


    face_count=len(req_dict5['data']['face_list'])
    if face_count>0:
        img = cv2.imread(image_name)
        for face in req_dict5['data']['face_list']:
            x1=round(face['x1'])
            y1=round(face['y1'])
            x2=round(face['x2'])
            y2=round(face['y2'])
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)
        cv2.imwrite(image_name, img)     #保存已经生成好的图片


    rescul='--------------------\n审查检测:\n'
    if resccc['conclusionType']==1:
        rescul=rescul+'无黄色图片或违规图片\n'
        rescul=rescul+'--------------------\n'

    else:

        for ms in resccc['data']:
            if ms['type']==8 or ms['type']==11:
                rescul=rescul+ms['msg']+'：'+ms['stars'][0]['name']+'\n'
            else:
                rescul=rescul+ms['msg']+'({:.0f}%)\n'.format(ms['probability']*100)
        rescul=rescul+'--------------------\n'




    retu='--------------------\n总结：'+req_dict['data']['text']+'\n--------------------\n图片分析结果： \n'
    for tag in req_dict2['data']['tag_list']:
        retu=retu+(tag['tag_name']+'------'+str(tag['tag_confidence'])+'%\n')
    retu=retu+rescul

    if face_count>0:
        retu=retu+'检测到'+str(face_count)+'张人脸\n--------------------'
        msg.reply(retu)
        msg.reply_image(image_name)
    else:
        retu=retu+'没有检测到人脸\n--------------------'
        msg.reply(retu)




@bot.register([Group,Friend],RECORDING )
def auto_reply(msg):
     # 回复消息内容和类型
    return '我最讨厌别人给我发语音了，所以不支持语音功能'







embed()