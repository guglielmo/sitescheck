from django.utils.translation import ugettext_lazy as _
from django.db import models
import hashlib
import re
import datetime
from urllib2 import Request, urlopen 
from lxml import etree

class Content(models.Model):
  """a content on the web, identified by the URL and the XPATH expression"""

  STATUS_NOT_CHANGED = 0
  STATUS_CHANGED = 1
  STATUS_ERROR = 2
  STATUS_CHOICES = (
    (STATUS_CHANGED, 'changed'), 
    (STATUS_NOT_CHANGED, 'unchanged'),
    (STATUS_ERROR, 'error')
  )
  
  title = models.CharField(max_length=250, 
                           verbose_name=_("the identifier of the url"), 
                           help_text="use the sequence IT - Name, where: I-Institution [C|G], T-type[R|P|C], Name, i.e. CR - Lazio)")
  url = models.URLField(verify_exists=True)
  xpath = models.CharField(blank=True, max_length=250)
  regexp = models.CharField(blank=True, max_length=250)
  hashed = models.CharField(blank=True, max_length=128, verbose_name='Hash')
  notes = models.TextField(blank=True)
  verified_at = models.DateTimeField(blank=True, null=True)
  verification_status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_NOT_CHANGED)
  verification_error = models.CharField(blank=True, max_length=250)

  def __unicode__(self):
    return self.title
  
  def get_html(self):
    # compile regexp used to remove session info (when needed)
    p = re.compile(self.regexp)

    
    # parse content from content.url
    # handle redirects with urlopen
    req_headers = { 
      "Accept": "application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5", 
      "Accept-Charset":  "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
      "Accept-Encoding": "gzip,deflate,sdch",
      "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4"
    }
    req = Request(self.url, headers=req_headers)
    resp = urlopen(req)
    parser = etree.HTMLParser()
    tree = etree.fromstring(resp.read(), parser)

    # extract html_element using content.xpath
    html_elements = tree.xpath(self.xpath)
    if (len(html_elements)):
      html_element = hteml_elements[0]
    else:
      raise NameError('xpath non trova niente')
      
    # transform it into a string and remove unwanted parts
    html_string = p.sub('', etree.tostring(html_element))

    return html_string


  def check_hash(self):
    html_string = self.get_html()

    # create a 512 bits hash out of the html string
    hash_algorythm = hashlib.sha512(html_string)
    hash_string = hash_algorythm.hexdigest()
    
    return hash_string


  def verify(self, dryrun):
    hash_string = self.check_hash()
    if  hash_string != self.hashed:
      self.hashed = hash_string
      self.verification_status = self.STATUS_CHANGED
    else:
      self.verification_status = self.STATUS_NOT_CHANGED
    self.verified_at = datetime.datetime.now()
    if dryrun == False:
      self.save()
    return self.verification_status
        

class Recipient(models.Model):
  """a recipient of notifications about changes on web contents"""

  name = models.CharField(blank=True, max_length=100)
  email = models.EmailField(unique=True)
  
  
  def __unicode__(self):
    return self.name
