import re
from functools import lru_cache
from dateutil.parser import parse as parse_datetime

class Type:
  __name__ = None
  __pattern__ = None
  __regex__ = None

  def __init__(self, name, pattern=None):
    self.to_string = self.get_name
    self.__name__ = name
    self.__pattern__ = pattern

  def get_name(self):
    return self.__name__

  def get_pattern(self):
    return self.__pattern__

  @lru_cache(1000)
  def __is_matching__(self, text):
    if not self.__pattern__:
      return None

    if not self.__regex__:
      self.__regex__ = re.compile(self.__pattern__)

    return self.__regex__.match(text) != None
    
@lru_cache(1000)
def get_number_only(text):
  result = ''
  
  for char in text:
    if char in '1234567890':
      result += char
      
  return result
  
################ Daftar tipe #################

email = Type('email', r'^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$')
username = Type('username', r'^[a-zA-Z](?:\w|[.-](?=\w)){3,31}[a-zA-Z0-9]$.*(?<!\.com)(?<!\.org)(?<!\.net)$')
url = Type('URL', r'^([a-zA-Z]+:\/?\/?)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-zA-Z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#()?&//=]*)$')
phonenumber = Type('phone number', '^(?:(?:\(?(?:00|\+)([1-4]\d\d|[1-9]\d?)\)?)?[\-\.\ \\\/]?)?((?:\(?\d{1,}\)?[\-\.\ \\\/]?){0,})(?:[\-\.\ \\\/]?(?:#|ext\.?|extension|x)[\-\.\ \\\/]?(\d+))?$')
md5 = Type('MD5', '^[a-f0-9]{32}$')
currency = Type('currency', '^(S?\$|\₩|Rp|\¥|\€|\₹|\₽|fr|R$|R)?[ ]?[-]?([0-9]{1,3}[,.]([0-9]{3}[,.])*[0-9]{3}|[0-9]+)([,.][0-9]{1,2})?( ?(USD?|AUD|NZD|CAD|CHF|GBP|CNY|EUR|JPY|IDR|MXN|NOK|KRW|TRY|INR|RUB|BRL|ZAR|SGD|MYR))?$')

usernameUrl = Type('username/URL')
datetime = Type('date/time')
unknown = Type('unknown')

################ Validasi tipe #################

is_email = email.__is_matching__
is_username = username.__is_matching__
is_url = url.__is_matching__
is_phonenumber = phonenumber.__is_matching__
is_md5 = md5.__is_matching__
is_currency = currency.__is_matching__


@lru_cache(1000)
def is_datetime(text):
  try:
    parse_datetime(text)
  except:
    return False

  return True

################ Deteksi tipe #################

@lru_cache(1000)
def get_type(text):
  # Perhatikan urutan logikanya, uji sebanyak mungkin
  # di 'main.py', dan juga perhatikan performa

  # Kodingan if di sini jangan terlalu naive, karna
  # ada kalanya teks a formatnya mirip tipe b dan
  # sebaliknya, itulah kenapa kita perlu nested if.
  # Bisa dibayangkan dengan diagram venn. Meski
  # demikian, commonsense counts

  # Modifikasi pada regex di atas mungkin perlu dilakukan
  # sekiranya hasil deteksi tidak akurat
  
  if is_email(text):
    return email
  elif is_url(text):
    if is_username(text):
      return usernameUrl

    return url
  elif is_username(text):
    return username
  elif is_datetime(text):
    return datetime
  elif is_phonenumber(text):
    return phonenumber
  elif is_currency(text):
    return currency
  elif is_md5(text):
    return md5
  else:
    return unknown
