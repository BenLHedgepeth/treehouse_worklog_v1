import csv
import os


def display_results(results_list, category):
	clear_screen()

	print('{matches} tasks were matched:\n'.format(matches=str(len(results_list))))

	for i, unique_entry in enumerate(results_list):
		print('*' * 10, "Entry #", str(i + 1), 'of', str(len(results_list)), '*' * 10)
	
		print_result = '''
	Task : {task}
	Date of Task : {date}
	Note : {details}
	Time : {time}
		'''.format(**unique_entry)
		print(print_result)
		
		print("""
	[ C ] - Continue
	[ M ] - Back To Previous Menu
			""")
		next_match = input("Do you want to see the next match? ").upper()

		while next_match not in ["M", "C"]:
			next_match = input("\nPress [ M ]ain Menu or [ C ]ontinue: ").upper()

		if next_match == 'M':
			return False

		elif (i + 1) == len(results_list):
			print(f"There are no more results searched by {category}.")
			return True # return to 'search_entries'
		
		else:
			continue

def compile_log():

	with open('worklog_entries.csv', 'r') as read_csv_rows:

		fieldnames = ["date", "task", "details", "time"]

		date_entries = csv.DictReader(read_csv_rows, fieldnames=fieldnames)
		next(date_entries, None) #skips the first line of the csv; header

		return list(date_entries)


def no_results(search_item):
	print(f"\nNo entries are stored under the provided {search_item}.")

	user_key = input(f"\nWould you like to search under a new {search_item} ([ Y ] / [ N ]):  ").upper()

	while user_key not in ['Y', 'N']:
		user_key = input(
"""Cannot read with the provided key entry.\n
Please select [ Y ] - Search New Date; [ N ] - Back to Previous Menu\n\n
>>> """).upper()

	if user_key == 'Y':
		clear_screen()
		return True
	clear_screen()
	return


def clear_screen():
	return os.system('cls' if os.name=='nt' else 'clear')


def write_entry(dict_object):

	with open('worklog_entries.csv', 'a', newline='\n') as write_entries:
		fieldnames = ["date", "task", "details", "time"]

		logger = csv.DictWriter(write_entries, fieldnames=fieldnames)

		table_date = dict_object['date'].strftime('%Y-%m-%d')
		table_time = dict_object['time'].strftime('%H:%M')
		dict_object.update(date=table_date, time=table_time)
		
		logger.writerow(dict_object)







