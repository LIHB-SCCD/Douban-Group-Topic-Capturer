"""
Module description

filter the record by author  key word

author: LIHB
email : huabing_li@zju.edu.cn
version: v0.1
date: 2020.3.20

"""


TITLE_IDX = 0;
TITLE_LINK_IDX = 1;
AUTHOR_IDX  = 2;
AUTHOR_LINK_IDX = 3;
RESP_NUM_IDX = 4;
TIME_IDX = 5;

def print_list_pretty(list):
    for elem in list:
        print(elem);


"""
    function define

    input: 
        bad_author_list: the author you don't want to see, a string list
        bad_word_list: the topic containing some key word you don't want to see, a string list
        douban_list : the origin list of topics, a list of record list; every element in the record list is assigned as 
                      [topic_title,topic_link,author_name,author_link,response_num,time]
    output:
        [bad_record_by_author,bad_record_by_word,filtered_list]
        bad_record_by_author: the records picked out since their authors are in bad_author_list
        bad_record_by_word : the records picked out since their topic title is in bad_word_list
        filtered_list: the filted douban_list
"""
def douban_filter(bad_author_list, bad_word_list,douban_list):
    bad_record_by_author = [];
    bad_record_by_word = [];
    filtered_list = douban_list.copy();
    for bad_author in bad_author_list:
        for i in range(len(filtered_list)-1,0,-1):
            if filtered_list[i][AUTHOR_IDX] == bad_author:
                bad_record_by_author.append(filtered_list[i]);
                del filtered_list[i]
            else:
                #filtered_author_list.append(one_record);
                pass
    #print_list_pretty(filtered_author_list); 



    for bad_word in bad_word_list:
        for i in range(len(filtered_list)-1,0,-1):
            chk_res = filtered_list[i][TITLE_IDX].find(bad_word);
            if chk_res != -1:
                del filtered_list[i]
                bad_record_by_word.append(filtered_list[i]); 
            else:
                pass
                
    print ('bad author reord is %d' %len(bad_record_by_author));
    print ('bad word reord is %d' %len(bad_record_by_word));
    print ('keep reord is %d' %len(filtered_list));
    print ('total reord is %d' %len(douban_list));
    
    return [bad_record_by_author,bad_record_by_word,filtered_list];





exist_record_file = open('C:/Users/LIHB/Desktop/get_list_from_douban/record_test.txt','rb');
record = exist_record_file.read()
strs_record = record.decode('utf-8')

cut_record  =  strs_record.splitlines();

record_final = [];

author_list = [];


for one_record in cut_record:
    spt_record = one_record.split('###');
    record_final.append(spt_record);
for one_record in record_final:
    author_list.append(one_record[2]);
    #print(one_record[2])
author_list.sort();

    
BAD_AUTHOR_LIST = ['不够格','宝贝呀','红色体恤','龙小贱','DK生活', '🌴张先生🌞🌞'];
BAD_WORD_LIST = ['房东直租','1号'];

[bad_record_by_author,bad_record_by_word,final_list] = douban_filter(BAD_AUTHOR_LIST,BAD_WORD_LIST,record_final);
print_list_pretty(final_list); 

#print(len(final_list))
#print(len(record_final))



