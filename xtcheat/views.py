import json
import random
from datetime import datetime, timedelta

import requests
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render)
from lxml import etree

import xtcheat.zhenzismsclient as smsclient

from .dailytask import send_email
from .models import Userinfo


'''
author:Lixin
date:20181212
desc:初次加载时获取cookies里的信息确认是否记住密码
input:
return:
'''
def get_info_via_cookies(request):
    context={}
    # set_signed_cookie('account',account,expires=datetime.now()+timedelta(days=3),salt='ms5cF3a2')
    if 'REMEMBER' in request.COOKIES: #记住密码
        context['account']=request.get_signed_cookie('account',salt='ms5cF3a2')
        context['password']=request.get_signed_cookie('password',salt='ms5cF3a2')
        context['remember']=request.get_signed_cookie('REMEMBER',salt='ms5cF3a2')
    return HttpResponse(json.dumps(context))


'''
author:Lixin
date:20181211
desc:注册页面方法
input:
return:
'''
def login(request):
    s = requests.session()
    url = r'http://xt.mediway.com.cn/ylxt/Loginajax.ashx?OperationType=login&mode=new'   
    if 'account' not in request.POST:
        return render(request,'xtcheat/login.html',)
    else:
        account = request.POST['account']
        password = request.POST['password']
        # groupid = request.POST['groupid']
        # body = {'j_username':'lixin0501','j_password':'844099269','hidaddress':'','isRemember':'1'}
        body = {}
        body['j_username']=account
        body['j_password']=password
        
        header = {'User-Agent':r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
                'Accept':r'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':r'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'Host': r'xt.mediway.com.cn',
                # 'Connection':'close',
                'Referer': r'http://xt.mediway.com.cn/ylxt/',}
                # 'X-Requested-With': r'XMLHttpRequest'
        context={}
        if 'groupid' not in request.POST: #第一次登陆
            body['DrpGroup']=''
            print(1)
            re = s.post(url,data=body,headers=header)
            print(2)
            remember = False
            if (re.json()['IsSuccess']==False): # 登陆失败
                error = re.json()['Msg']
                context['error']=error
            else:
                if 'error' in context:
                    context.pop('error')
                print(context)
                groupinfo = json.loads(re.json()['Msg'])
                context['groupinfo']=groupinfo
                context['account']=account
                context['password']=password
                
                if 'IsRemember' in request.POST:
                    remember = True
                context['remember']=remember
                # remember = request.POST['IsRemember']
                # print(remember)
                # print(f"{i['G_ID']}:{i['G_NAME']}")

            myresponse = render(request,'xtcheat/login.html',context)
            myresponse.set_signed_cookie('account',account,expires=datetime.now()+timedelta(days=3),salt='ms5cF3a2')
            myresponse.set_signed_cookie('password',password,expires=datetime.now()+timedelta(days=3),salt='ms5cF3a2')
            if (remember==True):
                myresponse.set_signed_cookie('REMEMBER',1,expires=datetime.now()+timedelta(days=3),salt='ms5cF3a2')
            else:
                myresponse.delete_cookie('REMEMBER')
            return myresponse
        else: #第二次登陆
            body['DrpGroup']=request.POST['groupid']
            re = s.post(url,data=body,headers=header)
            context['IsSuccess']=re.json()['IsSuccess']
            context['IsLogin']=re.json()['IsLogin']
            if (re.json()['IsLogin']==True): #登陆成功
            
                user,created = Userinfo.objects.get_or_create(account=request.get_signed_cookie('account',salt='ms5cF3a2'),password=request.get_signed_cookie('password',salt='ms5cF3a2'),groupid=request.POST['groupid'])
                # 获取个人信息
                if created:
                    url='http://xt.mediway.com.cn/ylxt/BASE/UIPersonInformationChanges.aspx'
                    rs = s.post(url,headers=header)
                    html = etree.HTML(rs.text)
                    print(html.xpath('//table[@class="form_table"]/tr[position()=2]/td[position()=1]/text()'))
                    username = html.xpath('//table[@class="form_table"]/tr[position()=2]/td[position()=1]/text()')[0]
                    phone = int(html.xpath('//input[@id="TxtPhone"]/@value')[0])
                    Mail =  html.xpath('//input[@id="Mail"]/@value')[0]
                
                    user.username = username
                    user.phone = phone
                    user.email = Mail
                    user.save() 
               
                context['user']=user
                # myresponse = render(request,'xtcheat/personinfo.html',context)
                myresponse = redirect('../person/')
                if 'IsRemember' not in request.POST:
                    myresponse.delete_cookie('REMEMBER')
                else:
                    myresponse.set_signed_cookie('REMEMBER',1,expires=datetime.now()+timedelta(days=3),salt='ms5cF3a2')           
                return myresponse
            else:
                context.clear()
                return render(request,'xtcheat/login.html',context)    


'''
author:Lixin
date:20181211
desc:个人信息展示
input:
return:
'''
def personalset(request):
    context={}
    user = get_object_or_404(Userinfo,account=request.get_signed_cookie('account',salt='ms5cF3a2'),password=request.get_signed_cookie('password',salt='ms5cF3a2'))
    context['user']=user
    return render(request,'xtcheat/personinfo.html',context)
    
    
'''
author:Lixin
date:201211
desc:修改手机页面跳转
input:
return:
'''
def update_phone(request):
    context={}
    user = get_object_or_404(Userinfo,account=request.get_signed_cookie('account',salt='ms5cF3a2'),password=request.get_signed_cookie('password',salt='ms5cF3a2'))
    context['phone']=user.phone
    return render(request,'xtcheat/updatePhone.html',context)


'''
author:Lixin
date:20181211
desc:发送手机验证码
input:
return:
'''
def send_phone_validatenum(request):
    validatenum = random.randint(1000,9999)
    phone = request.POST['phone']
    content="【打卡提醒】您的验证码为:"+str(validatenum)
    print(validatenum)
    appId = 100188
    apiUrl = r"https://sms_developer.zhenzikj.com"
    appSecret = "4eb9b575-ca25-4ccb-9bcf-5bdbf85042a5"
    client = smsclient.ZhenziSmsClient(apiUrl, appId, appSecret)
    client.send(phone,content)
    return HttpResponse(json.dumps(validatenum))


'''
author:Lixin
date:20181211
desc:保存手机号
input:
return:
'''
def save_phone(request):
    phone = request.POST['phone']
    user = get_object_or_404(Userinfo,account=request.get_signed_cookie('account',salt='ms5cF3a2'),password=request.get_signed_cookie('password',salt='ms5cF3a2'))
    user.phone = phone
    user.save()
    context = {'user':user}
    return render(request,'xtcheat/personinfo.html',context)



'''
author:Lixin
date:20181211
desc:修改邮箱界面跳转
input:
return:
'''
def update_email(request):
    context={}
    user = get_object_or_404(Userinfo,account=request.get_signed_cookie('account',salt='ms5cF3a2'),password=request.get_signed_cookie('password',salt='ms5cF3a2'))
    context['email']=user.email
    return render(request,'xtcheat/updateEmail.html',context)


'''
author:Lixin
date:20181211
desc:保存邮箱信息
input:
return:
'''
def save_email(request):
    email = request.POST['email']
    print(request.POST)
    user = get_object_or_404(Userinfo,account=request.get_signed_cookie('account',salt='ms5cF3a2'),password=request.get_signed_cookie('password',salt='ms5cF3a2'))
    user.email = email
    user.save()
    context = {'user':user}
    return render(request,'xtcheat/personinfo.html',context)


'''
author:Lixin
date:20181211
desc:发送邮箱验证码
input:
return:
'''
def send_email_validatenum(request):
    validatenum = random.randint(1000,9999)
    print(validatenum)
    email = request.POST['email']
    content = "【打卡提醒】您的验证码为:"+str(validatenum)
    send_email("smtp.qq.com",'844099269@qq.com',"xzicqvbuxlpibcjf",email,"打卡提醒",content)
    return HttpResponse(json.dumps(validatenum))


'''
author:Lixin
date:20181211
desc:改变短信提醒
input:
return:
'''
def change_phoneon(request):
    phoneon = False
    if 'phoneon' in request.POST:
        phoneon = request.POST['phoneon']
        if phoneon=='true':phoneon=True
        else:phoneon=False
    user = get_object_or_404(Userinfo,account=request.get_signed_cookie('account',salt='ms5cF3a2'),password=request.get_signed_cookie('password',salt='ms5cF3a2'))
    user.phoneon = phoneon
    user.save() 
    return HttpResponse(phoneon)


'''
author:Lixin
date:20181212
desc:改变邮箱提醒
input:
return:
'''
def change_emailon(request):
    emailon = False
    if 'emailon' in request.POST:
        emailon = request.POST['emailon']
        if emailon=='true':emailon=True
        else:emailon=False
    user = get_object_or_404(Userinfo,account=request.get_signed_cookie('account',salt='ms5cF3a2'),password=request.get_signed_cookie('password',salt='ms5cF3a2'))
    user.emailon = emailon
    user.save() 
    return HttpResponse(emailon)


'''
author:Lixin
date:20181217
desc:等待更新
input:
return:
'''
def wait(request):
    return render(request,'xtcheat/wait.html')
