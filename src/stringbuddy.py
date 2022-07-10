import re
from functools import lru_cache
from dateutil.parser import parse as parse_datetime

class Type:
  # Eq dan Hash perlu diimplementasikan manual karena regex itu konflik dan
  # itu memungkinkan terjadinya konflik
  
  __name__ = None
  __pattern__ = None
  __regex__ = None

  def __init__(self, name, pattern=None):
    self.to_string = self.get_name
    self.__name__ = name
    self.__pattern__ = pattern

  def __eq__(self, other):
    return self.__name__ == other.__name__

  def __hash__(self):
    return hash(self.__pattern__)

  def get_name(self):
    return self.__name__

  def get_pattern(self):
    return self.__pattern__

  def __get_ready__(self):
    if not self.__pattern__:
      return None

    if not self.__regex__:
      self.__regex__ = re.compile(self.__pattern__)

  @lru_cache(1000)
  def __is_matching__(self, text):
    self.__get_ready__()
    return self.__regex__.match(text) != None

  @lru_cache(1000)
  def __get_results__(self, text):
    self.__get_ready__()
    return self.__regex__.findall(text)
    
  @lru_cache(1000)
  def __get_non_results__(self, text):
    self.__get_ready__()
    return self.__regex__.split(text)

curr_sym = {"€": "EUR", "L": "ALL", "Br": "BYN", "KM": "BAM", "лв": "BGN", "kn": "HRK", "Kč": "CZK", "kr": "DKK", "₾": "GEL", "ft": "HUF", "Íkr": "ISK", "ден": "MKD", "zł": "PLN", "lei": "RON", "₽": "RUB", "₺": "TRY", "₴": "UAH", "£": "GBP", "$": "USD", "ƒ": "AWG", "B$": "BSD", "BZ$": "BZD", "Bs": "BOB", "R$": "BRL", "CA$": "CAD", "CI$": "KYD", "₡": "CRC", "CUC$": "CUP", "RD$": "DOP", "FK£": "FKP", "Q": "GTQ", "G$": "GYD", "G": "HTG", "J$": "JMD", "C$": "NIO", "B/.": "PAB", "₲": "PYG", "S/.": "PEN", "Sr$": "SRD", "TT$": "TTD", "$U": "UYU", "Bs.": "VED", "؋": "AFN", "֏": "AMD", "դր": "AMD", "₼": "AZN", ".د.ب": "BHD", "ლარი": "GEL", "ع.د": "IQD", "﷼": "YER", "₪": "ILS", "ينار": "JOD", "ك": "KWD", "ل.ل": "LBP", "£S": "SYP", "ر.ع": "OMR", "ر.ق": "QAR", "SR": "SAR", "دج": "DZD", "Kz": "AOA", "P": "BWP", "FBu": "BIF", "CF": "KMF", "FC": "CDF", "Fdj": "DJF", "E£": "EGP", "Nkf": "ERN", "D": "GMD", "GH₵": "GHS", "FG": "GNF", "KSh": "KES", "LD$": "LRD", "LD": "LYD", "Ar": "MGA", "K": "MWK", "₨": "MUR", "UM": "MRU", "DH": "MAD", "MT": "MZN", "N$": "NAD", "₦": "NGN", "R₣": "RWF", "Db": "STN", "Le": "SLL", "Sh.So.": "SOS", "R": "ZAR", "SS£": "SSP", "TSh": "TZS", "د.ت": "TND", "USh": "UGX", "A$": "AUD", "৳": "BDT", "Nu": "BTN", "៛": "KHR", "元": "CNY", "HK$": "HKD", "¥": "JPN", "Rp": "IDR", "₹": "INR", "₸": "KZT", "som": "KGS", "₭": "LAK", "MOP$": "MOP", "RM": "MYR", "MRf": "MVR", "₮": "MNT", "K": "MMK", "Rs": "PKR", "₩": "KRW", "₱": "PHP", "S$": "SGD", "NT$": "TWD", "TJS": "TJS", "US$": "USD"}
curr_sym_part = None
curr_code = ['ADP', 'AED', 'AFA', 'AFN', 'ALK', 'ALL', 'AMD', 'ANG', 'ANG', 'ANG', 'AOA', 'AOK', 'AON', 'AOR', 'ARA', 'ARP', 'ARS', 'ARY', 'ATS', 'AUD', 'AUD', 'AUD', 'AUD', 'AUD', 'AUD', 'AUD', 'AUD', 'AWG', 'AYM', 'AZM', 'AZN', 'BAD', 'BAM', 'BBD', 'BDT', 'BEC', 'BEF', 'BEL', 'BGJ', 'BGK', 'BGL', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BOP', 'BOV', 'BRB', 'BRC', 'BRE', 'BRL', 'BRN', 'BRR', 'BSD', 'BTN', 'BUK', 'BWP', 'BYB', 'BYN', 'BYR', 'BZD', 'CAD', 'CDF', 'CHC', 'CHE', 'CHF', 'CHF', 'CHW', 'CLF', 'CLP', 'CNY', 'COP', 'COU', 'CRC', 'CSD', 'CSJ', 'CSK', 'CUC', 'CUP', 'CVE', 'CYP', 'CZK', 'DDM', 'DEM', 'DJF', 'DKK', 'DKK', 'DKK', 'DOP', 'DZD', 'ECS', 'ECV', 'EEK', 'EGP', 'ERN', 'ESA', 'ESB', 'ESP', 'ESP', 'ETB', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'FIM', 'FIM', 'FJD', 'FKP', 'FRF', 'FRF', 'FRF', 'FRF', 'FRF', 'FRF', 'FRF', 'FRF', 'FRF', 'FRF', 'FRF', 'FRF', 'GBP', 'GBP', 'GBP', 'GBP', 'GEK', 'GEL', 'GHC', 'GHP', 'GHS', 'GIP', 'GMD', 'GNE', 'GNF', 'GNS', 'GQE', 'GRD', 'GTQ', 'GWE', 'GWP', 'GYD', 'HKD', 'HNL', 'HRD', 'HRK', 'HRK', 'HTG', 'HUF', 'IDR', 'IDR', 'IEP', 'ILP', 'ILR', 'ILS', 'INR', 'INR', 'IQD', 'IRR', 'ISJ', 'ISK', 'ITL', 'ITL', 'ITL', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF', 'KPW', 'KRW', 'KWD', 'KYD', 'KZT', 'LAJ', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LSM', 'LTL', 'LTT', 'LUC', 'LUF', 'LUL', 'LVL', 'LVR', 'LYD', 'MAD', 'MAD', 'MDL', 'MGA', 'MGF', 'MKD', 'MLF', 'MMK', 'MNT', 'MOP', 'MRO', 'MRU', 'MTL', 'MTP', 'MUR', 'MVQ', 'MVR', 'MWK', 'MWK', 'MXN', 'MXP', 'MXV', 'MYR', 'MZE', 'MZM', 'MZN', 'NAD', 'NGN', 'NIC', 'NIO', 'NLG', 'NOK', 'NOK', 'NOK', 'NPR', 'NZD', 'NZD', 'NZD', 'NZD', 'NZD', 'OMR', 'PAB', 'PEH', 'PEI', 'PEN', 'PEN', 'PES', 'PGK', 'PHP', 'PKR', 'PLN', 'PLZ', 'PTE', 'PYG', 'QAR', 'RHD', 'ROK', 'ROL', 'RON', 'RON', 'RSD', 'RUB', 'RUR', 'RUR', 'RUR', 'RUR', 'RUR', 'RUR', 'RUR', 'RUR', 'RUR', 'RUR', 'RUR', 'RWF', 'SAR', 'SBD', 'SCR', 'SDD', 'SDG', 'SDG', 'SDP', 'SEK', 'SGD', 'SHP', 'SIT', 'SKK', 'SLL', 'SOS', 'SRD', 'SRG', 'SSP', 'STD', 'STN', 'SUR', 'SVC', 'SYP', 'SZL', 'SZL', 'THB', 'TJR', 'TJS', 'TMM', 'TMT', 'TND', 'TOP', 'TPE', 'TRL', 'TRY', 'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UAK', 'UGS', 'UGW', 'UGX', 'USD', 'USD', 'USD', 'USD', 'USD', 'USD', 'USD', 'USD', 'USD', 'USD', 'USD', 'USD', 'USD', 'USD', 'USD', 'USD', 'USD', 'USD', 'USD', 'USN', 'USS', 'UYI', 'UYN', 'UYP', 'UYU', 'UYW', 'UZS', 'VEB', 'VEF', 'VEF', 'VEF', 'VES', 'VNC', 'VND', 'VUV', 'WST', 'XAF', 'XAF', 'XAF', 'XAF', 'XAF', 'XAF', 'XAG', 'XAU', 'XBA', 'XBB', 'XBC', 'XBD', 'XCD', 'XCD', 'XCD', 'XCD', 'XCD', 'XCD', 'XCD', 'XCD', 'XDR', 'XEU', 'XFO', 'XFU', 'XOF', 'XOF', 'XOF', 'XOF', 'XOF', 'XOF', 'XOF', 'XOF', 'XPD', 'XPF', 'XPF', 'XPF', 'XPT', 'XRE', 'XSU', 'XTS', 'XUA', 'XXX', 'YDD', 'YER', 'YUD', 'YUM', 'YUN', 'ZAL', 'ZAL', 'ZAR', 'ZAR', 'ZAR', 'ZMK', 'ZMW', 'ZRN', 'ZRZ', 'ZWC', 'ZWD', 'ZWD', 'ZWL', 'ZWN', 'ZWR']
curr_code_part = None
digitspace = Type('digit and space', '[0-9,. \t]+')

def sanitize_part(lst):
  for i in lst:
    if i[0] in '.+*?^$()[]{}|\\':
      yield f'\\{i}'
    else:
      yield i

def init_part():
  global curr_code_part
  global curr_sym_part
  
  if not curr_code_part:
    curr_code_part = '|'.join(curr_code)

  if not curr_sym_part:
    curr_sym_part = '|'.join(sanitize_part(curr_sym.keys()))

@lru_cache(1000)
def get_words(text):
  words = digitspace.__get_non_results__(text)
  
  if not words[0]:
    del words[0]
  
  return words

@lru_cache(1000)
def get_currency(text):
  init_part()

  for i in get_words(text):
    if i in curr_code:
      return i
    
    if i in curr_sym:
      return curr_sym[i]

  return 'EUR'        

@lru_cache(1000)
def get_thousand_separator(text):
  i = 0
  count_i = False
  
  for char in text:
    if char == ',':
      count_i = True
      
    if i == 4 and char == ',':
      return ','
      
    if count_i:
      i += 1
    
  if i == 4:
    return ','
    
  return '.'

@lru_cache(1000)
def get_number_only(text, add_chars='', prefixes='+-'):
  result = ''
  prefix = ''
  allowed_chars = '1234567890'
  all_chars = allowed_chars + add_chars
  can_add_number = False
  can_add_prefix = True
  
  for char in text:
    if can_add_prefix and char in prefixes:
      prefix = char
      
    if char in allowed_chars:
      can_add_number = True
      
    if can_add_number and char in all_chars:
      if can_add_prefix:
        can_add_prefix = False
        
      result += char
    
  for i in range(len(result) - 1, -1, -1):
    if result[i] in allowed_chars:
      return result[:i + 1]
  
@lru_cache(1000)
def parse_number(text, prefix='-'):
  rawnumber = get_number_only(text, ',.', prefix)
  
  if get_thousand_separator(rawnumber) == ',':
    return rawnumber.replace(',', '')
  else:
    return rawnumber.replace('.', '').replace(',', '.')
  
################ Daftar tipe #################

email = Type('email', r'^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$')
username = Type('username', r'^[a-zA-Z](?:\w|[.-](?=\w)){3,31}[a-zA-Z0-9]$.*(?<!\.com)(?<!\.org)(?<!\.net)$')
url = Type('URL', r'^([a-zA-Z]+:\/?\/?)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-zA-Z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#()?&//=]*)$')
phonenumber = Type('phone number', '^(?:(?:\(?(?:00|\+)([1-4]\d\d|[1-9]\d?)\)?)?[\-\.\ \\\/]?)?((?:\(?\d{1,}\)?[\-\.\ \\\/]?){0,})(?:[\-\.\ \\\/]?(?:#|ext\.?|extension|x)[\-\.\ \\\/]?(\d+))?$')
md5 = Type('MD5', '^[a-f0-9]{32}$')

currency = None
usernameUrl = Type('username/URL')
datetime = Type('date/time')
unknown = Type('unknown')

################ Validasi tipe #################

is_email = email.__is_matching__
is_username = username.__is_matching__
is_url = url.__is_matching__
is_phonenumber = phonenumber.__is_matching__
is_md5 = md5.__is_matching__

def is_currency(text):
  global currency
    
  init_part()
  currency = Type('currency', '^(' + curr_sym_part + ')?([. -]+)?([0-9]{1,3}[,.]([0-9]{3}[,.])*[0-9]{3}|[0-9]+)([,.][0-9]{1,2})?(,-)?( +?(' + curr_code_part + '))?$')
  
  return currency.__is_matching__(text)

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
  elif is_currency(text):
    return currency
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
  elif is_md5(text):
    return md5
  else:
    return unknown
