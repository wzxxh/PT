import requests,smtplib,json,time
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


# 写成了一个通用的函数接口，想直接用的话，把参数的注释去掉就好 
def send_email(subject,msg_from, passwd, msg_to, text_content, file_path=None):
    msg = MIMEMultipart()
    text = MIMEText(text_content)
    msg.attach(text)
    # file_path = r'read.md'  #如果需要添加附件，就给定路径
    if file_path:  # 最开始的函数参数我默认设置了None ，想添加附件，自行更改一下就好
        docFile = file_path
        docApart = MIMEApplication(open(docFile, 'rb').read())
        docApart.add_header('Content-Disposition', 'attachment', filename=docFile)
        msg.attach(docApart)
        print('发送附件！')
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        mailsender = smtplib.SMTP_SSL("smtp.qq.com", 465)
        mailsender.login(msg_from, passwd)
        mailsender.sendmail(msg_from, msg_to, msg.as_string())
        #print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("邮件发送失败")
        print('详情如下',e)
    finally:
        mailsender.quit()


class WeChat:
    def __init__(self,kwds):
        self.CORPID = kwds['CORPID']         #企业ID，在管理后台获取
        self.CORPSECRET = kwds['CORPSECRET'] #自建应用的Secret，每个自建应用里都有单独的secret
        self.AGENTID = kwds['AGENTID']    #应用ID，在后台应用中获取
        self.TOUSER = kwds['TOUSER']      # 接收者用户名,多个用户用|分割
        self.access_token_config_file_path = './config/wechat_access_token.conf'  # 临时存储 access_token
 
    def __get_new_access_token__(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
                  'corpsecret': self.CORPSECRET,
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def __save_and_return_new_access_token__(self):
        cur_time = time.time()
        access_token = self.__get_new_access_token__()
        with open(self.access_token_config_file_path, 'w') as f:
            f.write('\t'.join([str(cur_time), access_token]))
        return access_token
 
    def __get_access_token__(self):
        try:
            with open(self.access_token_config_file_path, 'r') as f:
                t, access_token = f.read().split()
        except:
            return self.__save_and_return_new_access_token__()
        else:
            cur_time = time.time()
            if 0 < cur_time - float(t) < 7260:
                return access_token
            else:
                return self.__save_and_return_new_access_token__()
 
    def send_data(self, message):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.__get_access_token__()
        send_values = {
            "touser": self.TOUSER,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {
                "content": message
                },
            "safe": "0"
            }
        send_msges=(bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()   #当返回的数据是json串的时候直接用.json即可将respone转换成字典
        return respone["errmsg"]

class notify:
    def __init__(self,notify_config:dict):
        self.notify_config = notify_config

    def __send_message_by_server酱__(self,content:str) -> None:
        api = 'https://sctapi.ftqq.com/' + self.notify_config['通知方式']['server酱']['sendkey'] + '.send'
        title = "PT签到通知"
        data = { 
            "text":title,
            "desp":content.replace('\n','\n\n')
            }
        req = requests.post(api,data = data)


    def __send_message_by_email__(self,message:str) -> None:
        sender = self.notify_config['通知方式']['邮箱']['发送邮箱账号']
        password = self.notify_config['通知方式']['邮箱']['发送邮箱授权码']
        receivers = self.notify_config['通知方式']['邮箱']['接收邮箱账号']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        subject = 'PT站定时签到' + time.strftime("%Y-%m-%d %X", time.localtime())
        send_email(subject,sender,password,receivers,message)




    def __send_message_by_wechat__(self,message:str) -> None:
        wechat_config = {   'CORPID':self.notify_config['通知方式']['企业微信']['企业ID'],
                            'CORPSECRET':self.notify_config['通知方式']['企业微信']['应用Secret'],
                            'AGENTID':self.notify_config['通知方式']['企业微信']['应用ID'],
                            'TOUSER':self.notify_config['通知方式']['企业微信']['接收者用户名']
                        }
        wechat = WeChat(wechat_config)
        wechat.send_data(message)


    def send_message(self,message:str) -> None:
        if self.notify_config['通知总开关'] == '开':
            if self.notify_config['通知方式']['server酱']['通知开关'] == '开':
                self.__send_message_by_server酱__(message)
                print('已通过server酱 发送签到记录')
            else:
                print('server酱通知开关已关闭')
            if self.notify_config['通知方式']['邮箱']['通知开关'] == '开':
                print('已通过邮箱 发送签到记录')
                self.__send_message_by_email__(message)
            else:
                print('邮箱通知开关已关闭')
            if self.notify_config['通知方式']['企业微信']['通知开关'] == '开':
                self.__send_message_by_wechat__(message)
                print('已通过企业版微信 发送签到记录')
            else:
                print('企业版微信通知开关已关闭')
        else:
            print('通知总开关已关闭，不发送通知')
