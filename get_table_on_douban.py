"""
Module description

get record in douban group

author: LIHB
email : huabing_li@zju.edu.cn
version: v0.1
date: 2020.3.20

"""

from requests_html import HTMLSession

#选择中值条件的宏定义
BY_TIME = 0; #抓取到某个时间点
BY_PAGES = 1;#抓取若干页
BY_MIX = 2; #那个条件先满足就按哪个终止

BAD_URL_MAX = 5;#连续连接失败的上限

#豆瓣小组连接的固定格式和页面内讨论列表的固定css selector
DOUBAN_TAOLUN_URL_FORM = 'https://www.douban.com/group/{}/discussion?start={} '; # 第一个 group_num 第二个 page_idx
DOUBAN_TAOLUN_TAB_FORM = 'table.olt>tr';  

"""函数输入：
    group_id : 小组的id，去小组连接里面找
    page_get : 需要扒多少页下来
    stop_time : 如果是以时间为抓取的截至条件的话，早于这个时间的就不抓了
    grab_end_condition : 指定终止条件，如果是BY_PAGES，就根据page_get的设置来终止抓取
                         如果是BY_TIME，就是根据 stop_time的设置来终止
                         如果是BY_MIX，则根据page_get 和 stop_time看哪个先满足
    函数输出：
        6个list, lsit的成员为str
        [topic_title,topic_link,author_name,author_link,response_num,time]

"""
def get_table_on_douban(group_id, page_get, stop_time,  grab_end_condition = BY_TIME):

    #return values
    topic_title = [];
    topic_link = [];
    author_name = [];
    author_link = [];
    response_num = [];
    time = [];


    #一些控制进程的变量
    page_idx = 0 # 用于翻页的url
    page_time = [] #当前页面讨论的时间
    page_cnt = 0 #用于统计翻了几页
    bad_url_cnt = 0 # 连接失败统计


    session = HTMLSession()
 
    while (True):
        url = DOUBAN_TAOLUN_URL_FORM.format(str(group_id),str(page_idx));
        try:
            print("尝试打开 %s " %url);
            page = session.get(url)
        except:
            print("连接错误!")
            bad_url_cnt = bad_url_cnt +1;#连接失败时计数+1, 连续若干次失败则跳出 
            if bad_url_cnt < BAD_URL_MAX:
                continue
            else:
                print("%d次尝试连接失败，抓取终止!"  %BAD_URL_MAX);
                break;         
        else:
            # print("成功！")
            if page.status_code != 200:
                print("访问错误，错误代码%d" %page.status_code)
                bad_url_cnt = bad_url_cnt +1;             
                if bad_url_cnt < BAD_URL_MAX:
                    continue
                else:
                    print("%d次尝试连接失败，抓取终止!"  %BAD_URL_MAX);
                    break; 
            else:
                bad_url_cnt = 0;    

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

        rows = len(table);
        for row_idx in range(2,rows):
            cols = table[row_idx].find('td');
            _topic_link = list(cols[0].links)[0];# change the set to str
            _topic_title = cols[0].text;
            _author_link = list(cols[1].links)[0];
            _author_name = cols[1].text;
            if len(cols[2].text) == 0:
                _response_num = str(0);
            else:
                _response_num = cols[2].text;
            _time = cols[3].text;

            topic_link.append(_topic_link);
            topic_title.append(_topic_title); 
            author_name.append(_author_name);
            author_link.append(_author_link);
            response_num.append(_response_num);
            time.append(_time);
            

        print("当前页面抓取完毕,获得%d条记录\n" %(rows - 1))
        page_idx = page_idx + rows-1;#豆瓣网页的id是按记录数排列的
        page_cnt = page_cnt +1;

        #判断是可以结束抓取了
        page_time = time[-1];#the last time
        if grab_end_condition == BY_PAGES:
            if page_cnt>=page_get:
                print("完成%d页记录抓取" %page_get);
                break
            else:
                pass
        elif grab_end_condition == BY_TIME:
            if is_time_eary_enough(stop_time,page_time):
                print("完成截至到%s的帖子抓取" %stop_time);
                break;
            else:
                pass
        else:
            if page_cnt>=page_get or is_time_eary_enough(stop_time,page_time):
                print("完成抓取!\n" );
                break;
            else:
                pass
    
    return [topic_title,topic_link,author_name,author_link,response_num,time];

# a small function used above
def is_time_eary_enough(time_target, time_now):

    [date_tar, time_tar] = time_target.split(' ');

    date_tar = date_tar.split('_');
    time_tar = time_tar.split(':');
    spt_target_time = date_tar + time_tar; #[mon,day,hour,minute]

    [date_now, time_now] = time_now.split(' ');
    date_now = date_now.split('_');
    time_now = time_now.split(':');
    spt_now_time = date_now + time_now; #[mon,day,hour,minute]
    
    #print ("DEBUG \n target: %s \n now: %s" %(spt_target_time,spt_now_time))

    return spt_target_time >= spt_now_time;

"""
Exmaple:

[topic_title,topic_link,author_name,author_link,response_num,time] = get_table_on_douban(467221,10,"03-19 0:0",BY_TIME);


for i in range(0,len(time)):
    strs = u'{}###{}###{}###{}###{}###{}\n'.format(topic_title[i],topic_link[i],author_name[i],author_link[i],response_num[i],time[i]);
  
    
    strs_utf8 = strs.encode('utf-8');
    record.write(strs.encode('utf-8'));
record.close();

"""
