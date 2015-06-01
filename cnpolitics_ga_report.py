#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2012 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple intro to using the Google Analytics API v3.

This application demonstrates how to use the python client library to access
Google Analytics data. The sample traverses the Management API to obtain the
authorized user's first profile ID. Then the sample uses this ID to
contstruct a Core Reporting API query to return the top 25 organic search
terms.

Before you begin, you must sigup for a new project in the Google APIs console:
https://code.google.com/apis/console

Then register the project to use OAuth2.0 for installed applications.

Finally you will need to add the client id, client secret, and redirect URL
into the client_secrets.json file that is in the same directory as this sample.

Sample Usage:

  $ python hello_analytics_api_v3.py

Also you can also get help on all the command-line flags the program
understands by running:

  $ python hello_analytics_api_v3.py --help
"""

import argparse
import sys
import cnpolitics_ga_report_auth
import utility

from apiclient.errors import HttpError
from apiclient import sample_tools
from oauth2client.client import AccessTokenRefreshError


def main(argv):
  s_date = utility.get_date_preweek()
  e_date = utility.get_date_now()
  print "\t政见网站运营报告\n （", s_date, '至', e_date, "）"
  print

  service = cnpolitics_ga_report_auth.initialize_service()
  # Authenticate and construct service.
  #service, flags = sample_tools.init(
  #    argv, 'analytics', 'v3', __doc__, __file__,
  #    scope='https://www.googleapis.com/auth/analytics.readonly')

  # Try to make a request to the API. Print the results or handle errors.
  try:
    cnpolitics_profile_id = get_cnpolitics_profile_id(service)
    if not cnpolitics_profile_id:
      print 'Could not find a valid profile for this user.'
    else:

      print '一、总览'
      results = get_total_metrics(service, cnpolitics_profile_id, s_date, e_date)
      utility.print_total_metrics(results)

      results = get_usertype_metrics(service, cnpolitics_profile_id, s_date, e_date)
      utility.print_usertype_metrics(results)

      print
      print '二、读者'

      results = get_audience_info(service, cnpolitics_profile_id, s_date, e_date)
      utility.print_audience_info(results)

      """
      results = service.data().ga().get(
      ids='ga:' + cnpolitics_profile_id,
      start_date=s_date,
      end_date=e_date,
      metrics='ga:visits',
      dimensions='ga:visitorGender',
      sort='-ga:visits',
      start_index='1',
      max_results='10').execute()
      utility.print_results(results)
      """

      results = get_top_continents(service, cnpolitics_profile_id, s_date, e_date)
      utility.print_top_continents(results)

      results = get_top_country(service, cnpolitics_profile_id, s_date, e_date)
      utility.print_top_country(results)

      results = get_top_cities(service, cnpolitics_profile_id, s_date, e_date)
      utility.print_top_cities(results)
      #utility.print_results(results)

      print '三、内容'
      results = get_top_pageviews(service, cnpolitics_profile_id, s_date, e_date)
      utility.print_top_pageviews(results)

      #results = get_top_browsers(service, cnpolitics_profile_id, s_date, e_date)
      #utility.print_results(results)

      #results = get_top_os(service, cnpolitics_profile_id, s_date, e_date)
      #utility.print_results(results)

      #results = get_top_devices(service, cnpolitics_profile_id, s_date, e_date)
      #utility.print_results(results)

  except TypeError, error:
    # Handle errors in constructing a query.
    print ('There was an error in constructing your query : %s' % error)

  except HttpError, error:
    # Handle API errors.
    print ('Arg, there was an API error : %s : %s' %
           (error.resp.status, error._get_reason()))

  except AccessTokenRefreshError:
    # Handle Auth errors.
    print ('The credentials have been revoked or expired, please re-run '
           'the application to re-authorize')


def get_cnpolitics_profile_id(service):
  """Traverses Management API to return the first profile id.

  This first queries the Accounts collection to get the first account ID.
  This ID is used to query the Webproperties collection to retrieve the first
  webproperty ID. And both account and webproperty IDs are used to query the
  Profile collection to get the first profile id.

  Args:
    service: The service object built by the Google API Python client library.

  Returns:
    A string with the first profile ID. None if a user does not have any
    accounts, webproperties, or profiles.
  """

  accounts = service.management().accounts().list().execute()

  if accounts.get('items'):
    cnpoliticsAccountId = accounts.get('items')[1].get('id')       # get the nth item
    webproperties = service.management().webproperties().list(
        accountId=cnpoliticsAccountId).execute()

    if webproperties.get('items'):
      cnpoliticsWebpropertyId = webproperties.get('items')[0].get('id')
      profiles = service.management().profiles().list(
          accountId=cnpoliticsAccountId,
          webPropertyId=cnpoliticsWebpropertyId).execute()

      if profiles.get('items'):
        return profiles.get('items')[0].get('id')

  return None


def get_total_metrics(service, profile_id, s_date, e_date):

  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=s_date,
      end_date=e_date,
      metrics='ga:visits,ga:pageviews,ga:sessions,ga:sessionDuration',
      sort='-ga:visits',
      start_index='1',
      max_results='25').execute()

def get_usertype_metrics(service, profile_id, s_date, e_date):

  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=s_date,
      end_date=e_date,
      dimensions='ga:userType',
      metrics='ga:sessions',
      start_index='1',
      max_results='25').execute()

def get_top_keywords(service, profile_id):
  """Executes and returns data from the Core Reporting API.

  This queries the API for the top 25 organic search terms by visits.

  Args:
    service: The service object built by the Google API Python client library.
    profile_id: String The profile ID from which to retrieve analytics data.

  Returns:
    The response returned from the Core Reporting API.
  """

  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date='2015-04-01',
      end_date='2015-05-18',
      metrics='ga:visits,ga:sessions',
      dimensions='ga:source,ga:keyword',
      sort='-ga:visits',
      filters='ga:medium==organic',
      start_index='1',
      max_results='25').execute()

def get_top_pageviews(service, profile_id, s_date, e_date):
  """Executes and returns data from the Core Reporting API.

  This queries the API for the top 25 organic search terms by visits.

  Args:
    service: The service object built by the Google API Python client library.
    profile_id: String The profile ID from which to retrieve analytics data.

  Returns:
    The response returned from the Core Reporting API.
  """

  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=s_date,
      end_date=e_date,
      metrics='ga:pageviews,ga:avgTimeOnPage',
      dimensions='ga:pageTitle',
      sort='-ga:pageviews',
      start_index='1',
      max_results='20').execute()

def get_top_continents(service, profile_id, s_date, e_date):
  """Executes and returns data from the Core Reporting API.

  This queries the API for the top 25 organic search terms by visits.

  Args:
    service: The service object built by the Google API Python client library.
    profile_id: String The profile ID from which to retrieve analytics data.

  Returns:
    The response returned from the Core Reporting API.
  """

  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=s_date,
      end_date=e_date,
      metrics='ga:visits,ga:pageviews,ga:avgTimeOnPage,ga:sessions,ga:sessionDuration',
      #metrics='ga:visits,ga:avgPageLoadTime,ga:avgServerResponseTime',
      dimensions='ga:continent',
      sort='-ga:visits',
      start_index='1',
      max_results='10').execute()

def get_top_country(service, profile_id, s_date, e_date):
  """Executes and returns data from the Core Reporting API.

  This queries the API for the top 25 organic search terms by visits.

  Args:
    service: The service object built by the Google API Python client library.
    profile_id: String The profile ID from which to retrieve analytics data.

  Returns:
    The response returned from the Core Reporting API.
  """

  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=s_date,
      end_date=e_date,
      metrics='ga:visits,ga:pageviews,ga:avgTimeOnPage,ga:sessions,ga:sessionDuration',
      dimensions='ga:country',
      sort='-ga:visits',
      #filters='ga:medium==organic',
      start_index='1',
      max_results='10').execute()

def get_top_cities(service, profile_id, s_date, e_date):
  """Executes and returns data from the Core Reporting API.

  This queries the API for the top 25 organic search terms by visits.

  Args:
    service: The service object built by the Google API Python client library.
    profile_id: String The profile ID from which to retrieve analytics data.

  Returns:
    The response returned from the Core Reporting API.
  """

  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=s_date,
      end_date=e_date,
      metrics='ga:visits,ga:pageviews,ga:avgTimeOnPage,ga:sessions,ga:sessionDuration',
      dimensions='ga:city',
      sort='-ga:visits',
      #filters='ga:medium==organic',
      start_index='1',
      max_results='10').execute()

def get_top_browsers(service, profile_id, s_date, e_date):
  """Executes and returns data from the Core Reporting API.

  This queries the API for the top 25 organic search terms by visits.

  Args:
    service: The service object built by the Google API Python client library.
    profile_id: String The profile ID from which to retrieve analytics data.

  Returns:
    The response returned from the Core Reporting API.
  """

  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=s_date,
      end_date=e_date,
      metrics='ga:visits',
      dimensions='ga:browser',
      sort='-ga:visits',
      start_index='1',
      max_results='5').execute()

def get_top_os(service, profile_id, s_date, e_date):
  """Executes and returns data from the Core Reporting API.

  This queries the API for the top 25 organic search terms by visits.

  Args:
    service: The service object built by the Google API Python client library.
    profile_id: String The profile ID from which to retrieve analytics data.

  Returns:
    The response returned from the Core Reporting API.
  """

  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=s_date,
      end_date=e_date,
      metrics='ga:visits',
      dimensions='ga:operatingSystem',
      sort='-ga:visits',
      start_index='1',
      max_results='5').execute()

def get_top_devices(service, profile_id, s_date, e_date):
  """Executes and returns data from the Core Reporting API.

  This queries the API for the top 25 organic search terms by visits.

  Args:
    service: The service object built by the Google API Python client library.
    profile_id: String The profile ID from which to retrieve analytics data.

  Returns:
    The response returned from the Core Reporting API.
  """

  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=s_date,
      end_date=e_date,
      metrics='ga:visits',
      dimensions='ga:mobileDeviceModel',
      sort='-ga:visits',
      start_index='1',
      max_results='10').execute()

def get_audience_info(service, profile_id, s_date, e_date):
  """Executes and returns data from the Core Reporting API.

  This queries the API for the top 25 organic search terms by visits.

  Args:
    service: The service object built by the Google API Python client library.
    profile_id: String The profile ID from which to retrieve analytics data.

  Returns:
    The response returned from the Core Reporting API.
  """

  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=s_date,
      end_date=e_date,
      metrics='ga:visits,ga:pageviews,ga:avgTimeOnPage,ga:sessions,ga:sessionDuration,ga:bounceRate',
      dimensions='ga:visitorGender',
      sort='-ga:visits',
      #filters='ga:medium==organic',
      start_index='1',
      max_results='10').execute()


def print_top_pageviews(results):
  """Prints out the top pageviews.

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


if __name__ == '__main__':
  main(sys.argv)
