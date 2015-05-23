#!/usr/bin/python

# import required classes
import datetime
from datetime import timedelta

def get_date_now():
	return datetime.datetime.now().strftime("%Y-%m-%d")

def get_date_preweek():
	lastHourDateTime = datetime.datetime.now() - timedelta(days = 7)
	return lastHourDateTime.strftime("%Y-%m-%d")

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

def print_pageview_results(results):
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
      i = 0
      for cell in row:
        if i == 0:
          #cell = cell[:-18]
          #print type(cell)
          cell = cell.split('|')[0]
        output.append('%30s' % cell)
        i = i + 1
      print ''.join(output)

  else:
    print 'No Rows Found'