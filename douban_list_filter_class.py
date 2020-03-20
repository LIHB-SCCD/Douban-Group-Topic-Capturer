from douban_record_class import *

class DoubanFilter(DoubanRecord):

	__ERR_TYPE = "ERROR_TYPE"
	__ERR_EMPTY = "ERROR_EMPTY"
	__VALID = "VALID"

	#auto detect bad author method
	BY_AUTHOR_REPET = 0;
	BY_RESP_NUM = 1;
	BY_MIX = 2;


	__bad_word_list = [];
	__bad_author_list = [];

	__good_word_list = [];
	__good_author_list = [];	
	def __init__(self,bad_author_list,bad_word_list,good_author_list = [],good_word_list=[]):

		chk_vld_1 = self.__is_valid_list(bad_author_list);
		chk_vld_2 = self.__is_valid_list(bad_word_list);
		chk_vld_3 = self.__is_valid_list(good_author_list);
		chk_vld_4 = self.__is_valid_list(good_word_list);

		if  chk_vld_1 == self.__VALID and \
		    chk_vld_2 == self.__VALID and \
		    chk_vld_3 == self.__VALID and \
		    chk_vld_4 == self.__VALID:
			pass
		else:
			print("@@ERROR@@ in __init__: init a empty instance!" );
			return;

		#self.__bad_author_list = bad_author_list;
		#self.__bad_word_list = bad_word_list;
		#self.__good_author_list = good_author_list;
		#self.__good_word_list = good_word_list;

		bad_author_set = set(bad_author_list);
		bad_word_set = set(bad_word_list);
		good_author_set = set(good_author_list);
		good_word_set = set(good_word_list);


		self.__bad_author_list = list(bad_author_set) ;
		self.__bad_word_list = list(bad_word_set);
		self.__good_author_list = list(good_author_set);
		self.__good_word_list = list(good_word_set);
		




	def filter_by_author_and_word(self,douban_list_in,exclude_good_author = False, exclude_good_word = False):

		if exclude_good_author:
			bad_author_set = set(self.__bad_author_list);
			good_author_set = set(self.__good_author_list);	
			bad_author_list = list(bad_author_set - good_author_set) ;
		else:
			bad_author_list = self.__bad_author_list;

		if exclude_good_word:			
			bad_word_set = set(self.__bad_word_list);
			good_word_set = set(self.__good_word_list);
			bad_word_list = list(bad_word_set - good_word_set);
		else:
			bad_word_list = self.__bad_word_list;



		chk_vld = self.__is_douban_list_valid(douban_list_in);
		if  chk_vld != self.__VALID:
			print("@@ERROR:%s@@ in filter_by_author_and_word: fail to filter" %chk_vld);
			return [];
		else:
			pass


		for one_record in douban_list_in:
			is_bad_author = one_record.get_author_name() in bad_author_list;
			one_record.set_is_bad_author(is_bad_author);

			has_bad_word = False;

			for bad_word in bad_word_list:
				if bad_word in one_record.get_topic_title():
					has_bad_word = True;
					break;
			one_record.set_has_bad_word(has_bad_word);
		return douban_list_in;

	def filter_by_read(self,new_douban_list,old_douban_list):
		chk_vld_1 = self.__is_douban_list_valid(new_douban_list);
		chk_vld_2 = self.__is_douban_list_valid(old_douban_list);

		if  chk_vld_1 == self.__VALID and chk_vld_2 == self.__VALID:
			pass
		else:
			print("@@ERROR:%s@@ in filter_by_author_and_word: fail to filter"  %chk_vld_1);
			return new_douban_list;

		readed_old_list = filter(lambda x: x.get_has_readed(),old_douban_list);
		readed_old_list = list(readed_old_list);

		for old_record in readed_old_list:
			author_name = old_record.get_author_name();
			topic_title = old_record.get_topic_title();
			for new_record in new_douban_list:
				if author_name == new_record.get_author_name():
					if topic_title == new_record.get_topic_title():
						new_record.set_has_readed(True);
						break;
		return new_douban_list;


	def auto_detect_bad_author(self, douban_list_in, method = 0,repet_num = 2, resp_num = 15):
		chk_vld = self.__is_douban_list_valid(douban_list_in);
		if chk_vld != self.__VALID:
			print("@@ERROR:%s@@ in auto_detect_bad_author: fail to detect bad author"  %chk_vld);
			return[];
		suspend_bad_authors = set();
		if method == self.BY_AUTHOR_REPET or method == self.BY_MIX: 
			total_author_list  = [];
			for record in douban_list_in:
				total_author_list.append(record.get_author_name());
			non_repet_list = list(set(total_author_list));
			#print("DEBUG:all author amount is %d", len(non_repet_list));
			for author in non_repet_list:
				num = total_author_list.count(author);		
				if num > repet_num:
					suspend_bad_authors.add(author);
					

		if  method == self.BY_RESP_NUM or method == self.BY_MIX:
			bad_record = filter(lambda x:int(x.get_response_num())>resp_num,douban_list_in)
			bad_record_list = list(bad_record);
			for record in bad_record_list:
				suspend_bad_authors.add(record.get_author_name());
				#print('DEBUG: %s----%s' %(record.get_response_num(),record.get_author_name()));
		
		if method != self.BY_RESP_NUM and method != self.BY_AUTHOR_REPET and method != self.BY_MIX:
			print("@@ERROR:ERROR_METHOD@@ in auto_detect_bad_author: fail to detect bad author");
			return [];
		return list(suspend_bad_authors);



	def get_bad_author_list(self):
		return self.__bad_author_list;
	def get_bad_word_list(self):
		return self.__bad_word_list;
	def get_good_author_list(self):
		return self.__good_author_list;
	def get_good_word_list(self):
		return self.__good_word_list;

		
	def set_bad_author_list(self,bad_author_list):
		chk_vld = self.__is_valid_list(bad_author_list);
		if chk_vld != self.__VALID:
			print("@@ERROR: %s@@ in set_bad_author_list: init a empty instance!" %chk_vld);
			return;
		merge_list = self.__bad_author_list + bad_author_list;
		merge_set = set(merge_list);
		self.__bad_author_list = list(merge_set);

	def set_bad_word_list(self,bad_word_list):
		chk_vld = self.__is_valid_list(bad_word_list);
		if chk_vld != self.__VALID:
			print("@@ERROR: %s@@ in set_bad_word_list: init a empty instance!" %chk_vld);
			return;
		merge_list = self.__bad_word_list + bad_word_list;
		merge_set = set(merge_list);
		self.__bad_word_list = list(merge_set);


	def set_good_author_list(self,good_author_set):
		chk_vld = self.__is_valid_list(good_author_set);
		if chk_vld != self.__VALID:
			print("@@ERROR: %s@@ in set_good_author_list: init a empty instance!" %chk_vld);
			return;
		merge_list = self.__good_author_set + good_author_set;
		merge_set = set(merge_list);
		self.__good_author_set = list(merge_set);			
		
	def set_good_word_list(self,good_word_list):
		chk_vld = self.__is_valid_list(good_word_list);
		if chk_vld != self.__VALID:
			print("@@ERROR: %s@@ in set_good_word_list: init a empty instance!" %chk_vld);
			return;
		merge_list = self.__good_word_list + good_word_list;
		merge_set = set(merge_list);
		self.__good_word_list = list(merge_set);	



	




			
	def __is_valid_list(self,input_list):
		if type(input_list) != type([]):
			return self.__ERR_TYPE;
		else:
			for elem in input_list:
				if type(elem) != type(' '):
					return self.__ERR_TYPE;
		return self.__VALID;

	def __is_douban_list_valid(self,input_list):
		if type(input_list) != type([]):
			return self.__ERR_TYPE;
		elif len(input_list) == 0:
			return self.__ERR_EMPTY;
		elif type(input_list[0]) != type(DoubanRecord()):
			return self.__ERR_TYPE;
		else:
			return self.__VALID;		