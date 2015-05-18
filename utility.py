#!/usr/bin/python

# import required classes
import datetime
from datetime import timedelta

def get_date_now():
	return datetime.datetime.now().strftime("%Y-%m-%d")

def get_date_preweek():
	lastHourDateTime = datetime.datetime.now() - timedelta(days = 7)
	return lastHourDateTime.strftime("%Y-%m-%d")