from douban_record_class import *

class DoubanFilter(DoubanRecord):

	__ERR_TYPE = "ERROR_TYPE"
	__VALID = "VALID"

	__bad_word_list = [];
	__bad_author_list = [];

	__good_word_list = [];
	__good_author_list = [];	
	def __init__(self,bad_author_list,bad_word_list,good_author_list = [], good_word_list = [],good_first = True):

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

		if good_first:
			self.__bad_author_list = list(bad_author_set - good_author_set) ;
			self.__bad_word_list = list(bad_word_set - good_word_set);
			self.__good_author_list = list(good_author_set);
			self.__good_word_list = list(good_word_set);
		else:	
			self.__bad_author_list = list(bad_author_set) ;
			self.__bad_word_list = list(bad_word_set);	
			self.__good_author_list = list( good_author_set - bad_author_set) ;
			self.__good_word_list = list(good_word_set - bad_word_set);




	def filter_by_author_and_word(self,douban_list_in):
		chk_vld = self.__is_douban_list_valid(douban_list_in);
		if  chk_vld != self.__VALID:
			print("@@ERROR:%s@@ in filter_by_author_and_word: fail to filter" %chk_vld);
			return [];
		else:
			pass

		for one_record in douban_list_in:
			is_bad_author = one_record.get_author_name() in self.__bad_author_list;
			one_record.set_is_bad_author(is_bad_author);

			has_bad_word = False;

			for bad_word in self.__bad_word_list:
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
		else:
			for elem in input_list:
				if type(elem) != type(DoubanRecord()):
					return self.__ERR_TYPE;
		return self.__VALID;		