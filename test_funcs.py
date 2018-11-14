import csv
import re

from utils import compile_log, clear_screen


def test_duplicate_entry(dict_object):
	# Iterate over a .csv file for any duplicate worklog entries
	log_length = compile_log()
	fieldnames = ["date", "task", "details", "minutes"]

	with open('worklog_entries.csv', 'a') as table:
		if len(log_length) == 0:
			headers = csv.DictWriter(table, fieldnames=fieldnames)
			headers.writeheader()

	for item in log_length: # Need to coerce into a list; log record is an object of OrderedDicts not a list
		if dict_object == item:
			return True # entry is a duplicate
	return False


def test_date_format(date_string):
	# Check whether a provided date matches a required format

	date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
	date_match = date_pattern.match(date_string)

	while not date_match:
		date_string = input(f"\n{date_string} is a not date. Dates register only under the format (YYYY-MM-DD): ")

		date_match = date_pattern.match(date_string)

		if date_match:
			break
	return date_match.group()


def test_time_format(time_string):
	time_pattern = re.compile(r'\d{2}:\d{2}')
	time_match = time_pattern.match(time_string)

	while not time_match:
		time_string = input(f"\n{time_string} is a not a time. Times register only under the format: 'HH:DD'\n").strip()
		time_match = time_pattern.match(time_string)
	return time_match.group()