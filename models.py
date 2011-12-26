# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from django.db import models
import re
import datetime
from os import sys

from urllib2 import Request, urlopen 
import html2text
import mechanize
import lxml.html
from lxml import etree

from model_utils import Choices

class Content(models.Model):
    """a content on the web, identified by the URL and the XPATH expression"""
    
    STATUS_NOT_CHANGED = 0
    STATUS_CHANGED = 1
    STATUS_ERROR = 2
    STATUS_CHOICES = (
        (STATUS_CHANGED, 'changed'), 
        (STATUS_NOT_CHANGED, 'unchanged'),
        (STATUS_ERROR, 'with errors')
    )
    TODO = (
        ('yes', 'Yes'),
        ('no', 'No')
    )
    
    title = models.CharField(max_length=250, 
                             verbose_name=_("the identifier of the url"), 
                             help_text="use the sequence IT - Name, where: I-Institution [C|G], T-type[R|P|C], Name, i.e. CR - Lazio)")
    url = models.URLField(verify_exists=True)
    xpath = models.CharField(blank=True, max_length=250)
    regexp = models.CharField(blank=True, max_length=250)
    meat = models.TextField(blank=True, verbose_name='Meaningful content')
    notes = models.TextField(blank=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    verification_status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_NOT_CHANGED)
    verification_error = models.CharField(blank=True, max_length=250)
    todo = models.CharField(max_length=3, choices=TODO)
    
    def __unicode__(self):
        return self.title
    
    
    def get_live_meat(self):
        # compile regexp used to remove session info (when needed)
        p = re.compile(self.regexp)
        
        # mechanize.Browser, con setup per evitare problemi
        br = mechanize.Browser()
        br.set_handle_robots(False)   # no robots
        br.set_handle_refresh(False)  # can sometimes hang without this
        
        # parse content from content.url
        br.addheaders = [
            ("Accept", "application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5"),
            ("Accept-Charset",  "ISO-8859-1,utf-8;q=0.7,*;q=0.3"),
            ("Accept-Encoding", "gzip,deflate,sdch"),
            ("Accept-Language", "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4"),
            ("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_7) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.71 Safari/534.24"),
        ] 
        br.open(self.url)
            
        # handle zipped content
        data = br.response().read()
        if  br.response().info().get('Content-Encoding') == 'gzip':
            import StringIO
            import gzip
            zipped_stream = StringIO.StringIO(data)
            gzipper = gzip.GzipFile(fileobj=zipped_stream)
            data = gzipper.read()
        
        parser = lxml.html.HTMLParser(remove_comments=True)
        tree = lxml.html.fromstring(data, parser=parser)
        
        # extract html_element using content.xpath
        html_elements = tree.xpath(self.xpath)
        if (len(html_elements)):
            html_element = html_elements[0]
        else:
            raise NameError('xpath non trova niente: %s' % self.xpath)
        
        # transform it into a string, extracting text content
        content = p.sub('', html_element.text_content())
        
        html2text.UNICODE_SNOB = 1
        return html2text.html2text(content)
    
    
    def verify(self, dryrun=False):
        if  (self.get_live_meat().replace(" ", "").replace("\n", "").replace("\t", "").replace(unichr(160), "") != 
             self.meat.replace(" ", "").replace("\n", "").replace("\t", "").replace(unichr(160), "")):
            self.verification_status = self.STATUS_CHANGED
        else:
            self.verification_status = self.STATUS_NOT_CHANGED
        self.verified_at = datetime.datetime.now()
        if dryrun == False:
            self.save()
        return self.verification_status
        
    
    
    def update(self):
        """update stored meat with live meat set verification status forward"""
        self.meat = self.get_live_meat()
        self.verification_status = self.STATUS_NOT_CHANGED
        self.verified_at = datetime.datetime.now()
        self.save()
    


class Recipient(models.Model):
    """a recipient of notifications about changes on web contents"""
    
    name = models.CharField(blank=True, max_length=100)
    email = models.EmailField(unique=True)
    
    
    def __unicode__(self):
        return self.name
