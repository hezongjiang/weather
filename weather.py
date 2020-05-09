import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import datetime
import os

def get_weather():

    url = 'https://free-api.heweather.net/s6/weather/forecast?location=深圳&key=your_key'
    res = requests.get(url).json()
    print(res)
    result = res['HeWeather6'][0]['daily_forecast']
    
    # 今天的天气
    today_date = result[0]['date']  # 日期
    today_day = result[0]['cond_txt_d']  # 白天天气
    today_night = result[0]['cond_txt_n']  # 晚上天气
    today_max_tmp = result[0]['tmp_max']  # 最高温度
    today_min_tmp = result[0]['tmp_min']  # 最低温度
    
    # 明天的天气
    tomorrow_date = result[1]['date']
    tomorrow_day = result[1]['cond_txt_d']
    tomorrow_night = result[1]['cond_txt_n']
    tomorrow_max_tmp = result[1]['tmp_max']
    tomorrow_min_tmp = result[1]['tmp_min']
    
    weather_msg = '天气预报来啦~\n深圳今天(' + today_date + ')' + today_day + '转' + today_night + '，' + today_min_tmp + '℃ ~ ' + today_max_tmp + '℃。\n'
    weather_msg += '深圳明天(' + tomorrow_date + ')' + tomorrow_day + '转' + tomorrow_night + '，' + tomorrow_min_tmp + '℃ ~ ' + tomorrow_max_tmp + '℃。'
    
    # print(weather_msg)
    return weather_msg


def send_email(msg):
    """
    发送邮件
    """
    # 设置邮箱的域名
    HOST = 'smtp.qq.com'
    # 设置邮件标题
    SUBJECT = '叮咚~ 明儿的天气到账啦~'
    # 设置发件人邮箱
    FROM = 'xxxx@qq.com'
    # reciver
    TO = 'xxxx@qq.com'  # 可以同时发送到多个邮箱，逗号分割

    message = MIMEMultipart('related')

    msg_alternative = MIMEMultipart('alternative')
    message.attach(msg_alternative)

    mail_msg = msg + '<br>'

    # 指定图片为当前目录
    today = datetime.date.today()  # 获得今天的日期
    # 注意这里的图片路径，需要和上一步截图中的路径一致
    img_path = '/user/weather/' + str(today) + '.png'

    # 如果图片存在，则使用图片
    if os.path.exists(img_path):
        mail_msg = mail_msg + '<p><img src="cid:image1"></p>'
        msg_alternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))
        with open(img_path, 'rb') as fp:
            msg_image = MIMEImage(fp.read())
            # 定义图片 ID，在 HTML 文本中引用
            msg_image.add_header('Content-ID', '<image1>')
            message.attach(msg_image)
            fp.close()
    else: # 如果图片不存在，则使用链接
        mail_msg = mail_msg + '<a href="https://your/hefeng/weather/url">🎈爱心天气❤</a>'
        msg_alternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))

    # 设置邮件发件人
    message['From'] = FROM
    # 设置邮件收件人
    message['To'] = TO
    # 设置邮件标题
    message['Subject'] = SUBJECT

    # 获取简单邮件传输协议的证书
    email_client = smtplib.SMTP_SSL(host=HOST)
    # 设置发件人邮箱的域名和端口，端口为465
    email_client.connect(HOST, '465')
    # 登录邮箱
    login_result = email_client.login(FROM, 'your authorization code')
    print('login result: ' + login_result)
    # 发送邮件
    email_client.sendmail(from_addr=FROM, to_addrs=TO.split(','), msg=message.as_string())
    # 关闭邮件发送客户端
    email_client.close()
    
send_email(get_weather())
