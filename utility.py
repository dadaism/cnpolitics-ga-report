#!/usr/bin/python
# -*- coding: utf-8 -*-

# import required classes
import datetime
from datetime import timedelta
from tabulate import tabulate

def get_date_now():
	return datetime.datetime.now().strftime("%Y-%m-%d")

def get_date_preweek():
	lastHourDateTime = datetime.datetime.now() - timedelta(days = 7)
	return lastHourDateTime.strftime("%Y-%m-%d")

def print_total_metrics(results):
  """Prints out the results.

  This prints out the profile name, the column headers, and all the rows of
  data.

  Args:
    results: The response returned from the Core Reporting API.
  """

  data = results.get('rows')
  print 
  print "日均访问人数: ", int(data[0][0])/7
  print "日均页面访问数: ", int(data[0][1])/7
  second = float(data[0][3])/float(data[0][2])
  print "人均网站停留时间: %d分%d秒" % (second/60, second%60)

def print_usertype_metrics(results):
  """Prints out the results.

  This prints out the profile name, the column headers, and all the rows of
  data.

  Args:
    results: The response returned from the Core Reporting API.
  """

  #print results.get('rows')[0]
  print "初次访问总人数: ", int(results.get('rows')[0][1])
  print "非初次访问总人数: ", int(results.get('rows')[1][1])
  #print tabulate(results.get('rows'))

def print_results(results):
  """Prints out the results.

  This prints out the profile name, the column headers, and all the rows of
  data.

  Args:
    results: The response returned from the Core Reporting API.
  """

  print
  print 'Profile Name: %s' % results.get('profileInfo').get('profileName')
  print

  # Print header.
  output = []
  for header in results.get('columnHeaders'):
    output.append('%30s' % header.get('name'))
  print ''.join(output)

  # Print data table.
  if results.get('rows', []):
    for row in results.get('rows'):
      output = []
      for cell in row:
        output.append('%30s' % cell)
      print ''.join(output)

  else:
    print 'No Rows Found'

def print_top_pageviews(results):
  """Prints out the results.

  This prints out the top pageviews of different articles.

  Args:
    results: The response returned from the Core Reporting API.
  """
  #print tabulate(results.get('rows'), headers=["page title","page view", "time on page"], tablefmt="grid" )

  data = []
  print 
  max_len = 0
  if results.get('rows'):
    for row in results.get('rows'):
      #print "processing ", row[0]
      row[0] = row[0].split('|')[0]
      row[0] = row[0].strip()
      if filter_page_title(row[0]) == False:
        data.append(row)
        if max_len < len(row[0]):
          max_len = len(row[0])
  else:
    print "No rows Found"
  #print len(data)
  #print max_len
  print "%s|%s|%s" % (unicode_align(u"文章标题",31), unicode_align(u"访问次数",6), unicode_align(u"阅读时间(s)",6))
  print "==========================================================================================="
  for row in data:
    #pad_len =  70 - str_len(row[0])
    #print str_len(row[0])
    #print ord(u'\u6697') == ord(row[0][0])
    #print "%s|%6s|  %.2f" % (row[0].ljust(80), row[1].center(20), float(row[2]) )
#    print "%s|%6s|  %.2f" % (myAlign(row[0],30), row[1].center(10), float(row[2]) )
    print "| %s|%s|%10.2f    |" % (unicode_align_left(row[0],30), row[1].center(12), float(row[2]) )
    print "-------------------------------------------------------------------------------------------"
  #return

def filter_page_title(title):
  if title == u"(not set)":
    return True
  if title == u"团队成员":
    return True
  if title == u"全部政见":
    return True
  elif title == u"政见 CNPolitics.org - 发掘海内外研究中国政治的智慧成果，引进思想资源":
    return True
  elif title == u"政见合辑下载":
    return True
  elif title == u"读图识政治":
    return True
  elif title == u"民主制度":
    return True
  elif title == u"研究速览":
    return True
  elif title == u"政府治理":
    return True
  elif title == u"张跃然":
    return True
  else:
    return False

def str_len(str):  
  simbol_len = 0;
  try:  
    row_l=len(str)  
    utf8_l=len(str.encode('utf-8'))
    for i in range(len(str)):
      """
        65311: ?
        65306: :
        8220:“
        8221:”
        65292:，
        12289:、
        65288:（
        65289:）
        12304:【
        12305:】
      """
      #if ord(str[i])==65311 or ord(str[i])==65306 or ord(str[i])==8220 or ord(str[i])==8221 \
      #      or ord(str[i])==65292 or ord(str[i])==12289 or ord(str[i])==65288 or ord(str[i])==65289 \
      #      or ord(str[i])==12304 or ord(str[i])==12305 :
        #print ord(u'\u4e00'), ord(str[i]), ord(u'\u9520'), str[i]
      #  simbol_len = simbol_len + 1
    #print "Total simbol: ", simbol_len
    #print "Original length: ", (utf8_l-row_l)/2+row_l
    return (utf8_l-row_l)/2+row_l#-simbol_len
  except:  
    return row_l


def unicode_align_left(string, length=0):
  if length == 0:
    return string
  slen = len(string)
  re = string
  half_width_num = 0;

  if isinstance(string, str):
    placeholder = ' '
  else:
    placeholder = u'　'
    
  """ count number of halfwidth characters for padding """
  for i in range(slen):
    if ord(string[i]) < 12200: # not a fully correct solution
      half_width_num = half_width_num + 1

  while slen < length:
    re += placeholder
    slen += 1

  #print half_width_num
  for i in range(half_width_num):
    re += ' '
  return re

def unicode_align(string, length=0):
  if length == 0:
    return string
  slen = len(string)
  re = ""
  half_width_num = 0;

  placeholder_num = length - slen
  if isinstance(string, str):
    placeholder = ' '
    for i in range(placeholder_num/2):
      re += placeholder
    re += string
    for i in range(placeholder_num/2, placeholder_num):
      re += placeholder
  else:
    placeholder = u'　'

    """ count number of halfwidth characters for padding """
    for i in range(slen):
      if ord(string[i]) < 12200: # not a fully correct solution
        half_width_num = half_width_num + 1
    
    """  pad left  """
    for i in range(half_width_num):
      re += ' '
    for i in range(placeholder_num/2):
      re += placeholder
    
    re += string
    """  pad right  """
    for i in range(placeholder_num/2, placeholder_num):
      re += placeholder
    for i in range(half_width_num/2, half_width_num):
      re += ' '

  return re

