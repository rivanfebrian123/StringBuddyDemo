import requests

class Strategy:
  GET, HEAD, TEXT = range(3)

class Status:
  AVAILABLE, UNAVAILABLE, UNKNOWN = range(3)

class SocialMediaStatus:
  name = None
  status = None
  
  def __init__(self, name, status=Status.UNKNOWN):
    self.name = name
    self.status = status
    
  def set_status(self, status):
    self.status = status
    
  def to_string(self):
    tab = '\t' if len(self.name) >= 8 else '\t\t'
    
    if self.status == Status.AVAILABLE:
      return f'{self.name}{tab}: Available'
    elif self.status == Status.UNAVAILABLE:
      return f'{self.name}{tab}: Has taken'
    elif self.status == Status.UNKNOWN:
      return f'{self.name}{tab}: Failed to fetch'
  
class SocialMedia:
  name = None
  url_prefix = None
  url_midfix = None
  url_suffix = None
  strategy = None
  status = None
    
  def __init__(self, name, url_prefix, url_midfix='',
               url_suffix='', strategy=Strategy.HEAD):
    self.name = name
    self.url_prefix = url_prefix
    self.url_midfix = url_midfix
    self.url_suffix = url_suffix
    self.strategy = strategy
    self.status = SocialMediaStatus(name)

  def is_available(self, username):
    url = f'{self.url_prefix}/{self.url_midfix}{username}/{self.url_suffix}'
    code = -1
    
    if self.strategy == Strategy.HEAD:
      code = requests.head(url).status_code
    # elif self.strategy == Strategy.TEXT:
    #   reqget = requests.get(url)
      
    #   if f'/{username}/' in reqget.text:
    #     code = 200
    #   elif reqget.status_code == 200:
    #     code = 999
    #   else:
    #     code = reqget.status_code
    else:
      code = requests.get(url).status_code
    
    if code == 200:
      self.status.set_status(Status.UNAVAILABLE)
    elif code == 404 or code == 503 or code == 410:
      self.status.set_status(Status.AVAILABLE)
    else:
      self.status.set_status(Status.UNKNOWN)
      
    return self.status

github = SocialMedia('Github', 'https://github.com')
gitlab = SocialMedia('Gitlab', 'https://gitlab.com', strategy=Strategy.GET)
bitbucket = SocialMedia('Bitbucket', 'https://bitbucket.org')
medium = SocialMedia('Medium', 'https://medium.com', '@', '', Strategy.GET)
dribbble = SocialMedia('Dribbble', 'https://dribbble.com',
                       strategy=Strategy.GET)
askfm = SocialMedia('Ask.fm', 'https://ask.fm',
                    strategy=Strategy.GET)
deviantart = SocialMedia('Deviantart', 'https://www.deviantart.com',
                         strategy=Strategy.GET)
youtube = SocialMedia('Youtube', 'https://www.youtube.com', 'c/',
                      strategy=Strategy.GET)
facebook = SocialMedia('Facebook', 'https://facebook.com',
                       strategy=Strategy.GET)

is_on_github = github.is_available
is_on_gitlab = gitlab.is_available
is_on_bitbucket = bitbucket.is_available
is_on_medium = medium.is_available
is_on_dribbble = dribbble.is_available
is_on_askfm = askfm.is_available
is_on_deviantart = deviantart.is_available
is_on_youtube = youtube.is_available
is_on_facebook = facebook.is_available

