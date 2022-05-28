import yaml

surpoted_websites = {}
config_file_path = './config/config.yaml'
example_config_file_path = './config/config_example.yaml'
surpoted_websites_file_path = './config/surpoted_websites.yaml'

defult_config = {
    'UserAgent':'',
    '定时':{
        '周几至周几':'1-7',
        '时':8,
        '分':0
    },
    '通知':{
        '通知总开关':'关',
        '通知方式':{
            'server酱':{
                '通知开关':'关',
                'sendkey':''
                },
            '邮箱':{
                '通知开关':'关',
                '发送邮箱账号':'',
                '发送邮箱授权码':'',
                '接收邮箱账号':''
                },
            '企业微信':{
                '通知开关':'关',
                '企业ID':'',
                '应用ID':'',
                '应用Secret':'',
                '接收者用户名':''
                }
            }
        },
    '网站':{
        'hdzone':{
            '访问签到开关':'关',
            '账号':'',
            '密码':'',
            'cookies':''
        },
        'pthome':{
            '访问签到开关':'关',
            '账号':'',
            '密码':'',
            'cookies':''
        },
        'hdarea':{
            '访问签到开关':'关',
            '账号':'',
            '密码':'',
            'cookies':''
        },
        'hdatmos':{
            '访问签到开关':'关',
            '账号':'',
            '密码':'',
            'cookies':''
        },
        'pttime':{
            '访问签到开关':'关',
            '账号':'',
            '密码':'',
            'cookies':''
        },
        'm-team':{
            '访问签到开关':'关',
            '账号':'',
            '密码':'',
            'cookies':''
        }
            
    }
         
}

surpoted_websites['hdzone'] = {
    'Host':'hdzone.me',
    '登陆界面页':{'地址':'http://hdzone.me/login.php','访问方式':'get'},
    '登陆操作页':{'地址':'http://hdzone.me/takelogin.php','访问方式':'post','参数':{'username':'','password':'','imagestring':'','imagehash':''}},
    '首页':{'地址':'http://hdzone.me/index.php','访问方式':'get'},
    '签到页':{'地址':'http://hdzone.me/attendance.php','访问方式':'get' }
    } 

surpoted_websites['pthome'] = {
'Host':'pthome.net',
'登陆界面页':{'地址':'https://pthome.net/login.php','访问方式':'get'},
'登陆操作页':{'地址':'https://pthome.net/takelogin.php','访问方式':'post','参数':{'username':'','password':'','imagestring':'','imagehash':'','scode':''}},
'首页':{'地址':'https://pthome.net/index.php','访问方式':'get'},
'签到页':{'地址':'https://pthome.net/attendance.php','访问方式':'get'}
}

surpoted_websites['hdarea'] = {
    'Host':'www.hdarea.co',
    '登陆界面页':{'地址':'http://www.hdarea.co/login.php','访问方式':'get'},
    '登陆操作页':{'地址':'http://www.hdarea.co/takelogin.php','访问方式':'post','参数':{'username':'','password':''}},
    '首页':{'地址':'https://www.hdarea.co/index.php','访问方式':'get'},
    '签到页':{'地址':'https://www.hdarea.co/sign_in.php','访问方式':'post','参数':{'action':'sign_in'} }
    }

surpoted_websites['hdatmos']={
    'Host':'hdatmos.club',
    '登陆界面页':{'地址':'http://hdatmos.club/login.php','访问方式':'get'},
    '登陆操作页':{'地址':'http://hdatmos.club/takelogin.php','访问方式':'post','参数':{'username':'','password':'','imagestring':'','imagehash':'','two_step_code':'','secret':''}},
    '首页':{'地址':'https://hdatmos.club/index.php','访问方式':'get'},
    '签到页':{'地址':'https://hdatmos.club/attendance.php','访问方式':'get' }
    }

surpoted_websites['pttime'] = {
    'Host':'www.pttime.org',
    '登陆界面页':{'地址':'http://www.pttime.org/login.php','访问方式':'get'},
    '登陆操作页':{'地址':'http://www.pttime.org/takelogin.php','访问方式':'post','参数':{'username':'','password':''}},
    '首页':{'地址':'https://www.pttime.org/index.php','访问方式':'get'},
    '签到页':{'地址':'https://www.pttime.org/attendance.php','访问方式':'get' }
}

surpoted_websites['m-team'] = {
    'Host':'kp.m-team.cc/',
    '登陆界面页':{'地址':'https://kp.m-team.cc/login.php','访问方式':'get'},
    '登陆操作页':{'地址':'https://kp.m-team.cc/takelogin.php','访问方式':'post','参数':{'username':'','password':''}},
    '首页':{'地址':'https://kp.m-team.cc/index.php','访问方式':'get'}
}



def save_dict_to_yaml(filepath:str,dict_value:dict):
    with open(filepath,'w',encoding='utf-8') as file:
        file.write(yaml.dump(dict_value, allow_unicode=True,sort_keys=False))         # sort_keys=False : 表示dump后的字典数据按原有的顺序示，为True时按字母的排序展示，默认为为True

def save_default_config_to_yaml():
    save_dict_to_yaml(example_config_file_path,defult_config)
    save_dict_to_yaml(surpoted_websites_file_path ,surpoted_websites)

def read_yaml_to_dict(filepath:str):
    with open(filepath,encoding='utf-8') as file:
        dict_value = yaml.load(file.read(), Loader=yaml.FullLoader)
    return dict_value
    
def read_config():
    my_websites = []
    surpoted_websites = read_yaml_to_dict(surpoted_websites_file_path)
    myconfig = read_yaml_to_dict(config_file_path)
    surpoted_websites_names = list( surpoted_websites.keys() )

    for website_name,website_config_dict in myconfig['网站'].items():
        temp = {}        
        if website_name in  surpoted_websites_names:
            temp.update(surpoted_websites [ website_name ])
            temp.update(website_config_dict)        
            my_websites.append( { website_name: temp } )
    myconfig['网站'] = my_websites     #更新我的网站到config大字典并返回
    return myconfig
            
