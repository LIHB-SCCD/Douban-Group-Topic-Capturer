"""
Module description

get record in douban group

author: LIHB
email : huabing_li@zju.edu.cn
version: v0.1
date: 2020.3.20

"""
from douban_record_class import *
from requests_html import HTMLSession
from tkinter.messagebox import *
import tkinter.messagebox

#选择中值条件的宏定义
BY_TIME = 0 #抓取到某个时间点
BY_PAGES = 1#抓取若干页
BY_MIX = 2 #那个条件先满足就按哪个终止

BAD_URL_MAX = 5#连续连接失败的上限

#豆瓣小组连接的固定格式和页面内讨论列表的固定css selector
DOUBAN_TAOLUN_URL_FORM = 'https://www.douban.com/group/{}/discussion?start={} ' # 第一个 group_num 第二个 page_idx
DOUBAN_TAOLUN_TAB_FORM = 'table.olt>tr'  

"""函数输入：
    douban_list: 成员为doubanRecord的list,抓取结果添加在这个list中
    group_id : 小组的id，去小组连接里面找
    page_get : 需要扒多少页下来
    stop_time : 如果是以时间为抓取的截至条件的话，早于这个时间的就不抓了
    grab_end_condition : 指定终止条件，如果是BY_PAGES，就根据page_get的设置来终止抓取
                         如果是BY_TIME，就是根据 stop_time的设置来终止
                         如果是BY_MIX，则根据page_get 和 stop_time看哪个先满足
    函数输出：
    抓取成功与否

"""
def get_table_on_douban(douban_list,group_id, page_get, stop_time,  grab_end_condition = BY_TIME):

    if type(douban_list) != type([]):
        print("ERROR:bad input params")
        return False
        

    
    topic_title = []
    topic_link = []
    author_name = []
    author_link = []
    response_num = []
    time = []


    #一些控制进程的变量
    page_idx = 0 # 用于翻页的url
    page_time = [] #当前页面讨论的时间
    page_cnt = 0 #用于统计翻了几页
    bad_url_cnt = 0 # 连接失败统计


    session = HTMLSession()
 
    while (True):
        url = DOUBAN_TAOLUN_URL_FORM.format(str(group_id),str(page_idx))
        try:
            print("尝试打开 %s " %url)
            page = session.get(url)
        except:
            print("连接错误!")
            bad_url_cnt = bad_url_cnt +1#连接失败时计数+1, 连续若干次失败则跳出 
            if bad_url_cnt < BAD_URL_MAX:
                continue
            else:
                showinfo("ERROR","%d次尝试连接失败，抓取终止!"  %BAD_URL_MAX)
                return False        
        else:
            # print("成功！")
            if page.status_code != 200:
                print("访问错误，错误代码%d" %page.status_code)
                bad_url_cnt = bad_url_cnt +1             
                if bad_url_cnt < BAD_URL_MAX:
                    continue
                else:
                    showinfo("ERROR","访问错误,终止抓取，错误代码%d"  %page.status_code)
                    return False
            else:
                bad_url_cnt = 0    

        #已经成功获取到页面，开始提取讨论的列表内容
        print("开始抓取帖子列表")
        try:
            table = page.html.find(DOUBAN_TAOLUN_TAB_FORM)    
        except:
            print("列表获取失败！")
            continue
        else:
            if table == []:
                continue

        rows = len(table)
        for row_idx in range(1,rows):
            cols = table[row_idx].find('td')
            _topic_link = list(cols[0].links)[0]# change the set to str
            _topic_title = cols[0].text
            _author_link = list(cols[1].links)[0]
            _author_name = cols[1].text
            if len(cols[2].text) == 0:
                _response_num = str(0)
            else:
                _response_num = cols[2].text
            _time = cols[3].text

            topic_link.append(_topic_link)
            topic_title.append(_topic_title) 
            author_name.append(_author_name)
            author_link.append(_author_link)
            response_num.append(_response_num)
            time.append(_time)
            

        print("当前页面抓取完毕,获得%d条记录\n" %(rows - 1))
        page_idx = page_idx + rows-1#豆瓣网页的id是按记录数排列的
        page_cnt = page_cnt +1

        #判断是可以结束抓取了
        page_time = time[-1]#the last time
        if grab_end_condition == BY_PAGES:
            if page_cnt>=page_get:
                print("完成对id-%s小组%d页记录抓取,获得%d条记录" %(group_id,page_get,page_idx))
                break
            else:
                pass
        elif grab_end_condition == BY_TIME:
            if is_time_eary_enough(stop_time,page_time):
                print("完成对id-%s小组截至到%s的帖子抓取,获得%d条记录" %(group_id,stop_time,page_idx))
                break
            else:
                pass
        else:
            if page_cnt>=page_get or is_time_eary_enough(stop_time,page_time):
                print("完成对id-%s小组抓取!,获得%d条记录" %(group_id,page_idx))
                break
            else:
                pass
    #douban_list = []
    for i in range(0,len(time)):
        douban_list.append(DoubanRecord([topic_title[i],topic_link[i],author_name[i],author_link[i],response_num[i],time[i]]))  
    return True

"""
   函数输入： record文件路径
   函数输出：获取结果
"""
def get_history_from_file(file_path = '../records/record.history'):
    try:
        exist_record_file = open(file_path,'rb')
    except:
        print("ERROR IN FILE OPEN !")
        return []
    else:
        record = exist_record_file.read()
        strs_record = record.decode('utf-8')
        exist_record_file.close()
        cut_record  =  strs_record.splitlines()
        douban_list = []

        for one_record in cut_record:
            spt_record = one_record.split('#HIST#')

            is_bad_author = bool(spt_record[6] == 'True')
            has_bad_word = bool(spt_record[7] == 'True')
            has_readed = bool(spt_record[8] == 'True')
            #print("DEBUG: is_bad_author:%s has_bad_word:%s has_readed:%s" %(is_bad_author,has_bad_word,has_readed))
            record = DoubanRecord(spt_record[0:6],is_bad_author,has_bad_word,has_readed)
            douban_list.append(record)
        return douban_list



def write_history_to_file(douban_list, file_path = '../records/record.history'):
    try:
        file = open(file_path,'wb')
    except:
        print("ERROR IN FILE OPEN !")
        return False
    else:
        for record in douban_list:
            topic_title = record.get_topic_title()
            author_name = record.get_author_name()
            resp_num = record.get_response_num()
            time = record.get_time()
            topic_link = record.get_topic_link()
            author_link = record.get_author_link()
            is_bad_author = record.get_is_bad_author()
            has_bad_word = record.get_has_bad_word()
            has_readed = record.get_has_readed()

            strs = u'{}#HIST#{}#HIST#{}#HIST#{}#HIST#{}#HIST#{}#HIST#{}#HIST#{}#HIST#{}\n'.format\
            (topic_title,topic_link,author_name,author_link,resp_num,time,is_bad_author,has_bad_word,has_readed)
            file.write(strs.encode('utf-8'))
        file.close()
    return True



def get_filter_list_from_file(file_path = '../records/filter.list'):
    try:
        exist_filter_list = open(file_path,'rb')
    except:
        showinfo("ERROR","ERROR IN FILE OPEN !")
        return []
    else:
        lists = exist_filter_list.read()
        strs_lists = lists.decode('utf-8')
        exist_filter_list.close()
        cut_lists  =  strs_lists.splitlines()

        if len(cut_lists) != 4:
            print("BAD_FILTER_LIST,RETURN EMPTY LIST")
            bad_author = []
            good_author = []
            bad_word = []
            good_word = []

        else:
            bad_author = cut_lists[0].split('#FILT#')
            good_author = cut_lists[1].split('#FILT#')
            bad_word = cut_lists[2].split('#FILT#')
            good_word = cut_lists[3].split('#FILT#')
            return [bad_author,good_author,bad_word,good_word]  

def write_filter_list_to_file(bad_author_list,good_author_list,bad_word_list,good_word_list,file_path = '../records/filter.list'):
    try:
        file = open(file_path,'wb')
    except:
        showinfo("ERROR","ERROR IN FILE OPEN !")
        return False
    else:
        gp = [bad_author_list,good_author_list,bad_word_list,good_word_list]
        for one_list in gp:
            dep = '#FILT#'
            file.write(dep.encode('utf-8'))
            for item in one_list:
                strs = item+'#FILT#'
                file.write(strs.encode('utf-8'))
            dep = '\n'
            file.write(dep.encode('utf-8'))
        file.close()
        return True


# a small function used above
def is_time_eary_enough(time_target, time_now):

    [date_tar, time_tar] = time_target.split(' ')

    date_tar = date_tar.split('_')
    time_tar = time_tar.split(':')
    spt_target_time = date_tar + time_tar #[mon,day,hour,minute]

    [date_now, time_now] = time_now.split(' ')
    date_now = date_now.split('_')
    time_now = time_now.split(':')
    spt_now_time = date_now + time_now #[mon,day,hour,minute]
    
    #print ("DEBUG \n target: %s \n now: %s" %(spt_target_time,spt_now_time))

    return spt_target_time >= spt_now_time


#Exmaple:

"""
[topic_title,topic_link,author_name,author_link,response_num,time] = get_table_on_douban(467221,5,"03-18 0:0",BY_TIME)

record = open('C:/Users/LIHB/Desktop/get_list_from_douban/record_test.txt','wb')

for i in range(0,len(time)):
    strs = u'{}###{}###{}###{}###{}###{}\n'.format(topic_title[i],topic_link[i],author_name[i],author_link[i],response_num[i],time[i])
  
    
    strs_utf8 = strs.encode('utf-8')
    record.write(strs.encode('utf-8'))
record.close()"""


