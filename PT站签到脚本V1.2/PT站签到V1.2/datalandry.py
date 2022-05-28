from bs4 import BeautifulSoup,element
from re import compile,findall



def 分析登陆页信息(html_content):
        soup = BeautifulSoup( html_content,'lxml' )
        标题 = soup.title.string
        是否有验证码 = False
        try:
                '''  
                验证码图片链接 = soup.find(('img',{'alt':'CAPTCHA'}))['src'] # HOST+此链接才是完整验证码链接
                以上查找方式 在pthome会失败
                '''
                验证码图片链接 = soup.find(text = '验证图片：').parent.find_next_sibling().img['src']
                验证码hash = 验证码图片链接.split('imagehash=')[1]            # 链接格式固定才能用，否则报错只能正则   
                是否有验证码 = True
        except:
                验证码图片链接 =  验证码hash = None
        #   有些网站登录页无验证码，无剩余登陆机会次数限制
        try:
                剩余登陆机会次数 =  soup.find(text = compile( r'还有(\s\w+)?') ).find_next_sibling().get_text().replace('[','').replace(']','')
        except:
                剩余登陆机会次数 =  None
        '''
        查找剩余登录机会次数也可用以下代码，但多了一步

        try:
                剩余登陆机会次数 = soup.find(text='你还有 ').find_next_sibling().get_text().replace('[','').replace(']','')    #pttime 会查找失败
        except:
                剩余登陆机会次数 = soup.find(text=' 次机会').find_previous_sibling().get_text().replace('[','').replace(']','')
        '''
        
        return {'标题':标题,'是否有验证码':是否有验证码,'验证码图片链接':验证码图片链接,'验证码hash':验证码hash,'剩余登陆机会次数':剩余登陆机会次数}

def 分析登陆操作页信息():
        return

def 分析首页信息(网站名,html_content) -> dict :
        #print('网站名：{} \n html:'.format(网站名,html) )
        soup = BeautifulSoup(html_content,'lxml' )  
  
        if 网站名 == 'pttime':
                return  分析首页信息_pttime(soup)

        用户标签 = soup.find('span','nowrap').a
        连接数标签 = soup.find('font',{'class':'color_slots'}) 

        用户等级 = 用户标签['class'][0].replace('_Name','').strip()
        用户名 =  用户标签.b.get_text().strip()
        魔力值 = soup.find('a',{'href':'mybonus.php'}).findNextSibling(text=True).replace(']:','').replace(u'\xa0','').strip()
        分享率 = soup.find('font',{'class':'color_ratio'}).findNextSibling(text=True).strip()
        上传量 = soup.find('font',{'class':'color_uploaded'}).findNextSibling(text=True).strip()
        下载量 = soup.find('font',{'class':'color_downloaded'}).findNextSibling(text=True).strip()
        当前做种 = soup.find('img',{'class':'arrowup'}).findNextSibling(text=True).strip()
        当前下载 = soup.find('img',{'class':'arrowdown'}).findNextSibling(text=True).strip()
        是否可连接 =  连接数标签.findPreviousSibling().font.getText() if 网站名 != 'hdatmos' else 连接数标签.findPreviousSibling().getText()
        连接数 =  连接数标签.findNextSibling(text=True).strip()
        if 网站名 == 'pthome' or 网站名 == 'hdzone':
                是否已签到 = True if '签到已得' in 魔力值 else False
        elif  网站名 == 'hdatmos':
                tmp = soup.find('a',{'href':'attendance.php'}).get_text()
                是否已签到 = True if '签到已得' in tmp else False
        elif 网站名 == 'hdarea':
                是否已签到 = False if soup.find(text = '[签到]') else True
        elif 网站名 == 'm-team':
                # 该网站已成功访问，页面中无 签到按钮，无签到功能，是否已签到 设置为None
                是否已签到  = None
        return {'用户等级':用户等级,'用户名':用户名,'魔力值':魔力值,'分享率':分享率,'上传量':上传量,'下载量':下载量,'当前做种':当前做种,'当前下载':当前下载,'是否可连接':是否可连接,'连接数':连接数,'是否已签到':是否已签到}

def 分析首页信息_pttime(soup) -> dict :
        用户标签 = soup.find('span','medium left')
        temp = 用户标签.a.nextSibling.get_text()        
        temp1 = findall('\]\[.*?\]\[',temp)[0]
        用户名 =  用户标签.b.get_text().strip() +  temp.replace(temp1,'') + ']'
        用户等级 = temp1.replace(']','').replace('[','')
        #连接数标签 = soup.find('font',{'class':'color_slots'}) 
        魔力值 = soup.find('a',{'href':'mybonus.php'}).findNextSibling(text=True).replace(']:','').replace(u'\xa0','').strip()
        分享率 = soup.find('font',{'class':'color_ratio'}).findNextSibling(text=True).strip()
        上传量 = soup.find('font',{'class':'color_uploaded'}).findNextSibling(text=True).strip()
        下载量 = soup.find('font',{'class':'color_downloaded'}).findNextSibling(text=True).strip()
        当前做种 = soup.find(title='当前做种').findNextSibling(text=True).strip()
        当前下载 = soup.find(title='当前下载').findNextSibling(text=True).strip()
        是否可连接 = ''
        连接数 = ''
        #是否可连接 =  soup.find('span',{'class':'mr5'})[4].get_text().strip()
        #连接数 = soup.find('span',{'class':'mr5'})[5].get_text().strip()
        是否已签到 = True if '获得' in 魔力值 else False
        
        return {'用户等级':用户等级,'用户名':用户名,'魔力值':魔力值,'分享率':分享率,'上传量':上传量,'下载量':下载量,'当前做种':当前做种,'当前下载':当前下载,'是否可连接':是否可连接,'连接数':连接数,'是否已签到':是否已签到}
 

def 分析签到页信息(网站名,html) -> dict :
        log = ''
        is_successed = False
        if 网站名  == 'pthome' or 网站名 == 'hdzone' or 网站名 == 'hdatmos' or 网站名 == 'pttime':
                soup = BeautifulSoup(html,"lxml")
                if soup.find(text = '签到成功'):  #非None则签到成功
                        is_successed = True
                        text = '这是你的第 ' if 网站名 == 'pttime' else '这是您的第 '
                        temps = soup.find(text = text).findParent().children
                        for temp in temps:
                                if isinstance( temp,element.NavigableString):
                                        log += temp.strip()
                                if isinstance( temp,element.Tag):
                                        log += temp.get_text()
                else:
                        #None 未找到“签到成功”标签，签到失败
                        log = '你今天已签到过了，请勿重复刷新'
        elif 网站名 == 'hdarea':
                log = html.decode('utf8')
                if '已连续签到' in log:
                        is_successed = True
                #log = 'hdarea签到成功待定' #待定   
                       
        return {'签到是否成功':is_successed,'日志':log}
