"""
文件名：webaction.py
用途：web请求相关

"""

import requests
import datalandry

class PTwebaction:
    def __init__(self,UserAgent,website_dict):
        self.website_name = list( website_dict.keys() ) [0]
        self.website_config = list( website_dict.values() ) [0]
        self.session = requests.Session()
        self.session.headers.clear()
        self.session.headers.update( {'Cookie': self.website_config['cookies'],'User-Agent':UserAgent} )


    def __visit_one_page__(self,page_config):
        访问方式 = page_config['访问方式']
        网址 = page_config['地址']
        参数 = page_config['参数'] if 访问方式 == 'post' else None
        if 访问方式 == 'get':
            res = self.session.get(网址)
        elif 访问方式 == 'post':
            res = self.session.post(网址,参数)         
        return res  
    '''
    #验证码识别
    def __get_img_bytes_and_ocr__(self,Host,img_half_link):        
        link =  'http://' + Host + '/' + img_half_link
        #print(link)
        res = requests.get(link)
        img_string = OCR.img_to_string_by_ocr(res.content)
        with open('img.jpg','wb') as file:
            file.write(res.content)
        return img_string

    #登录页验证码获取
    def __get__identify_image_before_login__(self) -> dict:
        identify_image_dict = {}
        res = self.__visit_one_page__(self.website_config['登陆界面页']) 
        if res.status_code == 200:     
            data = datalandry.分析登陆页信息(res.content)    #获取网页标题、验证码链接后半部分、验证码哈希，剩余登陆机会次数
            if data['是否有验证码']:
            #找出验证码图片并识别
                img_string = self.__get_img_hex_and_ocr__(self.website_config['Host'],data['验证码图片链接'])
                identify_image_dict .update( {'imagehash':data['验证码hash'],'imagestring':img_string } )
            identify_image_dict.update( {'chance':data['剩余登陆机会次数']} )
            identify_image_dict.update({'访问是否成功':True})
            return identify_image_dict
        elif res.status_code == 503:
            print('{}__visit_first_page__() 出错,res.status_code:{}'.format(self.website_config['首页'],res.status_code) )       
            return {'访问是否成功':False,'日志':'需要cloudflare认证'}
        else:
            return {'访问是否成功':False,'日志':'网络出错'}

    def __login__(self):
        identify_image_before_login = self.__get__identify_image_before_login__()
        #添加post参数
        self.website_config['登陆操作页']['参数']['username'] = self.website_config['账号']
        self.website_config['登陆操作页']['参数']['password'] = self.website_config['密码']
        self.website_config['登陆操作页']['参数']['imagehash'] = identify_image_before_login['imagehash']
        self.website_config['登陆操作页']['参数']['imagestring'] =identify_image_before_login['imagestring']
        res = self.__visit_one_page__(self.website_config['登陆操作页'])
        data = datalandry.分析登陆操作页信息()
        return data
'''
    def __visit_first_page__(self):         
        res = self.__visit_one_page__(self.website_config['首页']) 
        #if self.website_name == 'pttime':
        #    print('pttime  res.text:',res.text)
        if res.status_code == 200:     
            # 2021-11-08 
            # 部分网站（如hdarea）以br压缩响应，缺少brotli包则无法解压，连带使用res.content传入beatifualsoup都会查找元素失败
            # pip install brotli 安装即可，且py文件内无需import该包，requests会自动调用解压，也无需使用  以下 被备注代码            # 
            #————————————————————————————————————————————————————————————————————————————————————————————————————————————
            # if res.headers.get('Content-Encoding') == 'br':
            #    data = brotli.decompress(res.content)
            #    print ( data.decode('utf-8') )
            #————————————————————————————————————————————————————————————————————————————————————————————————————————————

            data =  datalandry.分析首页信息(self.website_name,res.content)
            return {'访问是否成功':True,'data':data,'日志':'访问首页成功'}
        elif res.status_code == 503:    
            return {'访问是否成功':False,'日志':'cookies已过期，或者需要cloudflare认证，请更新cookies试试'}
        else:
            return {'访问是否成功':False,'日志':'访问首页网络错误！'}

    def __sign_in__(self):
        res = self.__visit_one_page__( self.website_config['签到页'])
        if res.status_code == 200: 
            data =   datalandry.分析签到页信息(self.website_name,res.content)
            return {'访问是否成功':True,'data':data,'日志':'访问签到页成功'}
        elif res.status_code == 503:
            print('{}__sign_in__() 出错,res.status_code:{}'.format(self.website_config['签到页'],res.status_code) )       
            return {'访问是否成功':False,'日志':'需要cloudflare认证'}
        else:
            return {'访问是否成功':False,'日志':'访问签到页网络错误！'}
     
    def check_and_qiandao(self):
        is_visit_succesed = False
        is_sign_in_successed = False
        log = ''
        this_pt_website_data = {}
        shouye_data = self.__visit_first_page__()
        is_visit_succesed = shouye_data['访问是否成功']
        if is_visit_succesed:
            this_pt_website_data = shouye_data['data']
            if this_pt_website_data['是否已签到'] is None:
                # 该网站已成功访问，页面中无 签到按钮  
                is_sign_in_successed = None 
                log= '访问首页成功，无需签到'
            if this_pt_website_data['是否已签到']:
                log= '今日已签到过了'
            if this_pt_website_data['是否已签到'] == False :
                if '签到页' in list( self.website_config.keys() ):
                    qiandao_data = self.__sign_in__()
                    is_visit_succesed = qiandao_data['访问是否成功']
                    is_sign_in_successed = qiandao_data['data']['签到是否成功'] if is_visit_succesed else  False
                    log = qiandao_data['data']['日志'] if is_visit_succesed else  qiandao_data['日志']
                else:
                    log = '可以签到，但未在配置文件中 配置签到页 项'
        else:
            is_sign_in_successed = False
            log = shouye_data['日志']
        this_pt_website_data.update( {'网站名': self.website_name,'访问是否成功':is_visit_succesed,'签到是否成功':is_sign_in_successed,'日志':log} )
        return this_pt_website_data
    
