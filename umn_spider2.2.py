#2.1版本：从程序目录启动谷歌浏览器驱动
#2.0版本：下载内容从网站动态获得
#1.3版本：显示已找到多少个资源
#1.2版本：加入了文本进度条显示
#1.1版本：新增自动创建文件夹功能，文件检索功能，文件已存在时不会重复下载
#umn一键视频爬取器：用于爬取umn教学平台上的的教学视频
import time
import pyautogui
import re
import requests
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def video_url_get(url_course):
#----爬取视频的url----#
    video_list=[]
    #----设置浏览器静默模式（已停用，否则无法下滑鼠标）----#
    chrome_options=Options()
    chrome_options.add_argument('--headless')
    #----指定当前目录下的谷歌浏览器驱动文件----#
    diver=webdriver.Chrome(executable_path='chromedriver.exe')
    #----访问到首页----#  
    diver.get(url_course)
    time.sleep(4)
    #----鼠标往下滑两次----#
    for i in range(5):
        pyautogui.scroll(-10000)
        time.sleep(2)
    #----获取整个页面的数据，提取出视频后缀----#
    Pagesource=diver.page_source
    video_tails=re.compile('(\d*\.\d*\.\d*.{0,10}).mp4',re.S).findall(Pagesource)
    diver.close()
    for video_tail in video_tails:
        video_url='https://statics0.umustatic.cn/videoweike/teacher/weike/4kXW2806/transcoding/'+video_tail+'.mp4'
        video_list.append(video_url)
    return video_list

def downloader(url):
#----下载器----#
    start=time.time()
    size=0            #定义已下载文件的大小（byte）
    chunk_size=1024   #定义每次下载的数据大小（byte）
    root='d://umn_spider_video//'
    path=root+url.split('/')[-1]
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            res=requests.get(url,stream=True)
            content_size=int(res.headers['content-length'])
            if res.status_code==200:
                print('[文件大小]：%0.2f MB'%(content_size/1024/1024)) #将byte换算成MB
                print("急速爬虫器正在疯狂下载！！！".center(50,'-'))            
                with open(path,'wb') as f:
                    for data in res.iter_content(chunk_size=chunk_size):
                        f.write(data)
                        size+=len(data)
                        print("\r[下载进度]:{}{:.2f}%".format('>'*int(size*50/content_size),size*100/content_size),end='')
                    print('\n下载成功,文件自动帮您保存在d:/umn_spider_video/')
        else:
            print('文件已存在')
    except:
        print('爬取失败')

if __name__=='__main__':
    url_course=input('请输入课程首页的网址，如果不清楚请看教程：')
    # url_course='https://m.umu.cn/course/?groupId=4138993&sKey=0e6490a0d5ef477593326d2e8cd53faa&from_type=myparticipate'#专业教学设计与案例分析
    # url_course='https://m.umu.cn/course/?groupId=5001078&sKey=e30c05f1c34302d77478bf49a21daec2&from_type=myparticipate'  #职业教育德育研究
    video_list=video_url_get(url_course)
    print('已找到资源共%d个'%len(video_list))
    for url in video_list:
        downloader(url)
    input('任务全部完成，欢迎您的再次使用，按任意键退出。')

