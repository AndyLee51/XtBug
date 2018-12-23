import requests,json
from datetime import datetime,timedelta
import smtplib
from email.header import Header
from email.mime.text import MIMEText
import xtcheat.zhenzismsclient as smsclient
from lxml import etree
from .models import Userinfo

def get_first_and_end_day():
    year = datetime.today().year
    month = datetime.today().month

    first_month_day = datetime.strptime(str(year)+"-"+str(month)+"-1","%Y-%m-%d")
    days_in_week = datetime.strftime(first_month_day,'%w')
    start_day_of_month = (first_month_day-timedelta(days=int(days_in_week))).strftime("%Y-%m-%d")
    if month<12:
        last_month_day = datetime.strptime(str(year)+"-"+str(month+1)+"-1","%Y-%m-%d")-timedelta(days=1)
    else:
        last_month_day = datetime.strptime(str(year+1)+"-1-1","%Y-%m-%d")-timedelta(days=1)
    days_in_week = datetime.strftime(last_month_day,"%w")
    end_day_of_month = (last_month_day+timedelta(days=(6-int(days_in_week)))).strftime("%Y-%m-%d")
    return start_day_of_month,end_day_of_month
 
def getRecords(username,password):
    requests.adapters.DEFAULT_RETRIES = 5
    Session = requests.session()
    Session.keep_alive = False
    # Session.proxies={"http":"47.104.193.87:8080"}
    url = r'http://xt.mediway.com.cn/ylxt/Loginajax.ashx?OperationType=login&mode=new'
    # r'http://xt.mediway.com.cn/ylxt/Loginajax.ashx?OperationType=login&mode=new' 
    body = {'j_username':username,'j_password':password,'hidaddress':'','isRemember':'1'}
    header = {'UserAgent':r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
              'Accept':r'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            #   'Accept-Encoding':'gzip, deflate',
            #   'Accept-Language':r'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
              'Host': r'xt.mediway.com.cn',
            #   'Connection':'close',
              'Referer': r'http://xt.mediway.com.cn/ylxt/',
              'Upgrade-Insecure-Requests': r'1'}
              
    rs = Session.post(url,data=body,headers=header)
    GroupId=json.loads(rs.json()['Msg'])[0]['G_ID']
    body['DrpGroup']=GroupId
    cookies = Session.cookies.get_dict()
    rs.close()
    rs = Session.post(url,headers=header,data=body,cookies=cookies)

    days=get_first_and_end_day()
    url =r'http://xt.mediway.com.cn/ylxt/HR/UIWorkAttendance.ashx?OperationType=WorkAttendance&start={}&end={}&date=270'.format(days[0],days[1])
    rs = Session.get(url,headers=header,cookies=cookies,timeout=1000)
    msg = json.loads(rs.json()['Msg'])
    rs.close()
    daysinfo={}
    ID = {}

    for d in msg:
        daysinfo[d['start']]=d['title']
        ID[d['start']] = d['ID']
    result = ""
    today = (datetime.today()).strftime("%Y-%m-%d")+" 00:00:00"
    if today not in daysinfo:
        result = '您还未进行'+(datetime.today()).strftime("%Y-%m-%d")+'的{上班打卡}，请及时登录微信打卡，以免影响您的考勤。'
    elif daysinfo[today].find("不足时") != -1:
        # hvid = ID[today]
        # url = f'http://xt.mediway.com.cn/ylxt/HR/UILeaveAppyDetail.aspx?hvid={hvid}'
        url = f'http://xt.mediway.com.cn/ylxt/HR/UILeaderOverTMApply.ashx?OperationType=wxkq&idList=24300,&datestr={(datetime.today()).strftime("%Y-%m-%d")}'
        rs = Session.get(url,headers=header)  
        html = etree.HTML(rs.json()['Msg'])   
        firsttime = html.xpath('//table[@class="form_table"][1]/tr[3]/td[position()=2]/text()')[0]
        lasttime = html.xpath('//table[@class="form_table"][1]/tr[last()]/td[position()=2]/text()')[0]  
        if (firsttime == lasttime):
            result = '您还未进行'+(datetime.today()).strftime("%Y-%m-%d")+'的{下班打卡}，请及时登录微信打卡，以免影响您的考勤。'
        else:
            firsttime = datetime.strptime(firsttime,'%Y/%m/%d %H:%M:%S')
            lasttime = datetime.strptime(lasttime,'%Y/%m/%d %H:%M:%S')
            hours = lasttime-firsttime
            if (hours< timedelta(hours=9) and hours>timedelta(hours=2)):
                result = "您今日的打卡时长不足9小时，请登陆微信查询详细信息，以免影响您的考勤"
    return result

def send_email(SMTP_host, from_account, from_passwd, to_account, subject, content):

    email_client = smtplib.SMTP(SMTP_host)
    email_client.login(from_account, from_passwd)
    # create msg
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')  # subject
    msg['From'] = from_account
    msg['To'] = ",".join(to_account)
    print(msg)
    email_client.sendmail(from_account, to_account, msg.as_string())
    email_client.quit()


'''
author:Lixin
date:20181217
desc:HTML格式邮件
input:
return:
'''
def send_html_email(SMTP_host, from_account, from_passwd, to_account, subject, content):
    email_client = smtplib.SMTP(SMTP_host)
    email_client.login(from_account, from_passwd)
    # create msg
    msg = MIMEText(content,_subtype='html',_charset='gb2312')
    msg['Subject'] = Header(subject, 'utf-8')  # subject
    msg['From'] = from_account
    msg['To'] = ",".join(to_account)
    print(msg)
    email_client.sendmail(from_account, to_account, msg.as_string())
    email_client.quit()

# 第三方 SMTP 服务
def send_tips_via_email(account,password,email):
    mail_host = "smtp.qq.com"      # SMTP服务器
    mail_pass = "xzicqvbuxlpibcjf"               # 授权密码，非登录密码
    sender = '844099269@qq.com'    # 发件人邮箱(最好写全, 不然会失败)
    receivers = [email,]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    tip = getRecords(account,password)
    content = f'''
    <div style="display:block;background-color:#d2d2d2;margin-left: 30%;width: 40%;height:30%;text-align: center;border-radius:6px;">
        <div style="background-color: #393D49;display: block;padding:0.1em 0px;color: white"><h3><b>打卡提醒</b></h3></div>
        <div style="padding:0px 20px;text-align:left">
            <p>打卡提醒系统提示您：</p>
            <p style="text-indent:2em;">{tip}，请您立即使用微信考勤系统打卡，以免影响您的考勤。</p>
        </div>
        <div style="margin-top: 30px;">
            <a style="color: #01AAED" href="http://xt.mediway.com.cn/ylxt/">医疗协同</a>  |  <a style="color: #01AAED" href="http://127.0.0.1:8000/xtcheat/login/">打卡提醒</a>
        </div>
    </div>
    '''
    title = '打卡信息提醒'  # 邮件主题
    if (tip != ""):
        send_html_email(mail_host, sender, mail_pass,receivers, title, content)



'''
author:Lixin
date:20181217
desc:短信发送
input:
return:
'''
def send_tips_via_phone(account,password,phone):
    appId = 100188
    apiUrl = r"https://sms_developer.zhenzikj.com"
    appSecret = "4eb9b575-ca25-4ccb-9bcf-5bdbf85042a5"
    client = smsclient.ZhenziSmsClient(apiUrl, appId, appSecret)
    tip = getRecords(account,password)
    if tip!="":
        content = f"【打卡提醒】{tip},请及时登录微信打卡，以免影响您的考勤。"
        client.send(phone,content)

def send_tips_to_everyone():
    print(getRecords('lixin0501','844099269'))
    users = Userinfo.objects.all()
    for user in users:
        username = user.account
        password = user.password
        phone = user.phone
        email = user.email 
        phoneon = user.phoneon
        emailon = user.emailon

        if (phoneon):
            send_tips_via_phone(username,password,phone)
        if (emailon):
            send_tips_via_email(username,password,email)
