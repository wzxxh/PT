import datetime,webaction,本地Sqlite,notify

def send_notify(message:str,message_config:dict) -> None:
    message_sender = notify.notify(message_config)
    message_sender.send_message(message)

def save_file(file_path,file_name,content):
    with open(file_path+file_name,'w') as file:
        file.write(content)
        
def save_log(*args):
    时间,log = args
    时间 = 时间.replace(':','：') #windows中 文件名不能包含英文冒号:，故替换为中文冒号：
    save_file('./log/',时间+'签到记录.log',log)  
    print('已保存日志文件')

def visit_and_signin_one_website(UserAgent,one_website_config_dict,nativedb):
    pt = webaction.PTwebaction(UserAgent,one_website_config_dict)
    website_name = list(one_website_config_dict.keys() )[0]
    if one_website_config_dict[website_name]['访问签到开关'] == '关':
        msg = '{} 站访问及签到开关已关闭'.format(website_name)
        return msg
    if one_website_config_dict[website_name]['cookies'] == '':
        msg = '{} 站未配置cookies，无法签到。请配置cookies！'.format(website_name)
        return msg
    else:
        final_data = pt.check_and_qiandao()
        final_data.update ( { '时间': datetime.datetime.now() } )
        #print(final_data)
        if final_data['访问是否成功']:
            if final_data['签到是否成功'] is None:
                msg = '{} 站{}'.format(website_name, final_data['日志']) 
            else:
                if final_data['签到是否成功']:
                    nativedb.保存数据(final_data) 
                    is_successed_msg = '成功,{}'.format( final_data['日志'] ) 
                else:
                    is_successed_msg = ( '失败，原因为：' + final_data['日志'] )
                msg = '{} 站签到{}'.format(website_name, is_successed_msg ) 
        else:
            msg = '{} 站访问失败,{}'.format(website_name,final_data['日志'])
        return msg

def visit_and_signin_all_websites(my_config_dict):
    时间 = datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
    print('{} 执行一次签到'.format( 时间 ) )
    nativedb = 本地Sqlite.Nativedb()
    UserAgent = my_config_dict['UserAgent']
    log = 时间 + '\n'
    for each_website in my_config_dict['网站']:
        try:
            msg = visit_and_signin_one_website(UserAgent,each_website,nativedb)
        except Exception as e:
            site_name = list(each_website.keys())[0]
            msg = '{} 站于{}签到发生错误,错误明细:{}'.format(site_name,时间,str ( e ) ) 
        log += msg + '\n' 
        print(msg)           
    send_notify(log,my_config_dict['通知'])
    save_log(时间,log)
