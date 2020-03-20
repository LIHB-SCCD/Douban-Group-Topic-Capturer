TITLE_IDX = 0;
TITLE_LINK_IDX = 1;
AUTHOR_IDX  = 2;
AUTHOR_LINK_IDX = 3;
RESP_NUM_IDX = 4;
TIME_IDX = 5;

class DoubanRecord:
	"""docstring for ClassName"""
	__ERR_LIST = ['VALID','ERROR_TYPE','ERROR_LEN','ERROR_OTHER', ]

	__RECD_LEN = 6;


	__topic_link = '';
	__topic_title = '';
	__author_link = '';
	__author_name = '';
	__response_num = '';     
	__time = '';
	__is_bad_author = False;
	__has_bad_word = False;
	__has_readed = False;
	__other_param = '';



	def __init__(self, one_record=['','','','','',''], is_bad_author = False, has_bad_word = False, has_readed = False, other_param = [],shut_warning = False):
		chk_valid = self.__is_valid_record(one_record);
		if (chk_valid != self.__ERR_LIST[0]):
			print("@@ERROR:%s@@ in __init__: init a empty instance!" %chk_valid);
			return;
		else:
			self.__topic_title = one_record[TITLE_IDX];
			self.__topic_link =  one_record[TITLE_LINK_IDX];
			self.__author_name = one_record[AUTHOR_IDX];
			self.__author_link = one_record[AUTHOR_LINK_IDX];
			self.__response_num = one_record[RESP_NUM_IDX];
			self.__time = one_record[TIME_IDX];


			self.__is_bad_author = self.__check_and_trans_to_bool(is_bad_author,shut_warning);
			self.__has_bad_word = self.__check_and_trans_to_bool(has_bad_word,shut_warning);
			self.__has_readed = self.__check_and_trans_to_bool(has_readed,shut_warning);
			self.__other_param = other_param;

	def get_record(self):
		return [self.__topic_title,self.__topic_link,self.__author_name,self.__author_link,self.__response_num,self.__time]


	def get_topic_title(self):
		return self.__topic_title;
	def get_topic_link(self):
		return self.__topic_link;
	def get_author_name(self):
		return self.__author_name;
	def get_author_link(self):
		return self.__author_link;
	def get_response_num(self):
		return self.__response_num;
	def get_time(self):
		return self.__time;
	def get_is_bad_author(self):
		return self.__is_bad_author;
	def get_has_bad_word(self):
		return self.__has_bad_word;
	def get_has_readed(self):
		return self.__has_readed;

	def set_is_bad_author(self,val,shut_warning = 1):
		self.__is_bad_author = self.__check_and_trans_to_bool(val,shut_warning);
	def set_has_bad_word(self,val,shut_warning = 1):
		self.__has_bad_word = self.__check_and_trans_to_bool(val,shut_warning);
	def set_has_readed(self,val,shut_warning = 1):
		self.__has_readed = self.__check_and_trans_to_bool(val,shut_warning);



	def set_record(self,input_record):
		chk_valid = self.__is_valid_record(input_record);

		if (chk_valid != self.__ERR_LIST[0]):
			print("@@ERROR:%s@@ in set_record: Refuse to change the record!" %chk_valid);
			return;
		else:
			self.__topic_title = input_record[TITLE_IDX];
			self.__topic_link =  input_record[TITLE_LINK_IDX];
			self.__author_name = input_record[AUTHOR_IDX];
			self.__author_link = input_record[AUTHOR_LINK_IDX];
			self.__response_num = input_record[RESP_NUM_IDX];			
			self.__time = input_record[TIME_IDX];

	def get_flag(self,name):
		if type(name) != type(' '):
			print("@@ERROR@@ in get_flag: error name type, get flag failed!");
			return False;
		else:
			if name == 'is_bad_author':
				return self.__is_bad_author;

			elif name == 'has_bad_word':
				return self.__has_bad_word;

			elif name == 'has_readed':
				return self.__has_readed;

			else:
				print("@@ERROR@@ in get_flag: error name, get flag failed!");
				return False;
	def set_flag(self,name,val,shut_warning = False):
		_val = self.__check_and_trans_to_bool(val,shut_warning);

		if name == 'is_bad_author':
			self.__is_bad_author = _val;

		elif name == 'has_bad_word':
			self.__has_bad_word = _val;

		elif name == 'has_readed':
			self.__has_readed = _val;

		else:
			print("@@ERROR@@ in get_flag: error name type, set flag failed!");

	def cmp_by_author(self,obj):
		return self.__author_name > obj.__author_name;

	def __is_valid_record(self,input_record):
		if type(input_record) != type([]):
			return self.__ERR_LIST[1];
		elif len(input_record) != self.__RECD_LEN:
			return self.__ERR_LIST[2];
		else:
			for elem in input_record:
				if type(elem) != type(' '):
					return self.__ERR_LIST[1];
		return self.__ERR_LIST[0];
	def __check_and_trans_to_bool(self,val,shut_warning = False):
		if type(val) != type(True) :
			if shut_warning == False: print('@@WARNING@@ set flag : input type is not bool! ');
			return int(val)> 0;
		return val;
	def __repr__( self ):
		return '\''+self.__topic_title+'\', \''+\
		    self.__topic_link +'\', \''+\
		    self.__author_name+'\', \''+\
		    self.__author_link+'\', \''+\
		    self.__response_num+'\', \''+\
		    self.__time+ '\n';



		