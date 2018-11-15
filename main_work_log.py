import csv
import datetime
import re
import shutil
import os
import sys

from task_factory import Task
from test_funcs import test_duplicate_entry, test_date_format
from utils import display_results, compile_log, no_results, clear_screen, write_entry

class WorkLog:

	def __init__(self):
		self.main_menu()


	def main_menu(self):
		clear_screen()
		while True:
			print(
			'''Please select from the following options...\n\t
 A - Add entry
 S - Search entry
 D - Delete entry
 X - QUIT
			''')

			log_option = input("Please select an option: ").upper()

			if log_option== 'A':
				
				clear_screen()
				
				new_task = Task()
				self.log_entry(new_task) 

			elif log_option == "S":

				clear_screen()
				self.search_entries()

			elif log_option == "D":
				self.delete_entry()

			else:
				clear_screen()
				sys.exit()

	def search_entries(self):

		search_methods = {
						'D' : self.exact_date,
						'R' : self.search_dates,
						'S' : self.search_string, 
						'T' : self.search_time,
						'P' : self.search_pattern
					}

		clear_screen()

		while True:

			print("""Search by:\n
[ D ] - Date
[ R ] - Range of Dates
[ T ] - Time
[ S ] - String
[ P ] - Pattern
[ M ] - Return to Main Menu
			  """)
			search_type = input("Specify how you want to query your search: ").upper()

			if search_type == 'M':
				clear_screen()
				return

			while search_type not in ['D', 'T', 'S', 'P', 'R']:
				search_type = input("Cannot search entries with the given option.\n Please select: [ D(ate) ], [ T(ime) ], [ S(tring) ], [ P(attern) ],  [ R(ange) ]").upper()

			filter_worklog = search_methods[search_type]

			find_entries = filter_worklog()

			run_search = input("""\nWould you like to run another type of search?\n[ Y ] - Yes\n[ N ] - No\n\n>>> """).upper()

			while run_search not in ['Y', 'N']:
				run_search = input("""Do you want to conduct another search or go to the main menu?
[ Y ] - Yes
[ N ] - No \n\n >>>
			   """).upper()

			if run_search == "N":
				clear_screen()
				break # reverts back to the main menu
				
			else:
				clear_screen()
				self.search_entries()



	def log_entry(self, task_object):
		
		task_data = vars(task_object) # represents a dictionary of all Task instance attributes
		
		duplicated = test_duplicate_entry(task_data) # tests the dictionary against each entry in the csv file

		if duplicated:
			user_decision = input("That task is already recorded. Would you like to enter a new task (Y/N): ").upper()
		else:
			write_entry(task_data)

		user_decision = input("\nWould you like to enter a new task (Y/N): ").upper()

		while user_decision not in ['Y', 'N']:
			user_decision = input("\nCannot read input. To add a new entry press [ Y ]; to go back to the main menu press [ N ]: ").upper()

		if user_decision == "Y":
			clear_screen()
			add_new_task = Task()
			self.log_entry(add_new_task)	
		else:
			clear_screen()
			return # go back to the main menu
		
	
	def exact_date(self):

		clear_screen()

		search_item = "date"

		while True:

			date_object, log_entries = Task.store_date(self), compile_log() 
			
			provided_date = date_object.strftime("%Y-%m-%d")
			
			matched_dates = list(filter(lambda x: x['date'] == provided_date, log_entries)) #filters tasks

			if not matched_dates:
				empty_results = no_results(search_item)

				if empty_results:
					continue # prompt for a new date input if 0 results are generated from the previous date
				break # prompt the user for a new search; N - Main Menu; Y - Search Menu
			else:
				date_criteria = display_results(matched_dates, search_item) # iterates over the entries that meet user's criteria

				if not date_criteria or date_criteria:
					break # prompt the user for a new search; N - Main Menu; Y - Search Menu

	
	def search_dates(self):

		clear_screen()

		search_item = 'date'

		while True:

			date_origin, log_entries = Task.store_date(self), compile_log()

			while True:
				try:
					date_margin = abs(int(input("\nHow many days before and after your date do you want to look: ")))
				except ValueError:
					print("The value provided can't establish the desired date range.")
				else:
					break


			clear_screen()

			search_item = "time"
			start_date = date_origin - datetime.timedelta(days=date_margin)
			end_date = date_origin + datetime.timedelta(days=date_margin)
				
			dates_wanted = []

			for date_log in log_entries:
				date_object = datetime.datetime.strptime(date_log['date'], '%Y-%m-%d').date()

				if date_object >= start_date and date_object <= end_date:
					dates_wanted.append(date_log)

			if not dates_wanted:
				empty_results = no_results(search_item) # iterates over the entries that meet user's criteria

				if empty_results:
					continue # prompt for a new date input if 0 results are generated from the previous date and date range
				break # prompt the user for a new search; N - Main Menu; Y - Search Menu
			
			else:
				date_range = display_results(dates_wanted, search_item)

				if not date_range or date_range:
					break # prompt the user for a new search; N - Main Menu; Y - Search Menu

	
	def search_string(self):

		clear_screen()

		search_item = "phrase"

		while True:

			string_criteria = input(f"Provide a {search_item} in order to search entries within the work log?\n\n>>> ").title()

			while not string_criteria:
					string_criteria = input("The worklog cannot be searched with empty criteria.\nPlease search under a different phrase:\n\n>>>")

			log_details = compile_log()

			strings_matched = list(filter(lambda x: string_criteria in x['task'] or string_criteria in x['details'], log_details))

			if not strings_matched:
				empty_results = no_results(search_item)

				if empty_results:
					continue # prompt for a new string input if 0 results are generated from the previous string
				break # prompt the user for a new search; N - Main Menu; Y - Search Menu
			
			else:
				string_results = display_results(strings_matched, search_item) # iterates over the entries that meet user's criteria

				if not string_results or string_results:
					break # prompt the user for a new search; N - Main Menu; Y - Search Menu


	def search_pattern(self):

		clear_screen()

		search_type = 'regular expression'

		while True:

			search_item = "regular expression"

			log_entries = compile_log()

			pattern = input(r"Provide a regular expression pattern to match up entries in the work log: ")

			while not pattern:
				pattern = input(r"Sorry. The pattern provided is not accepted: ")

			re_pattern = re.compile(pattern)

			pattern_matches = []

			for single in log_entries:
				if re_pattern.match(single['task']) or re_pattern.match(single['details']):
					pattern_matches.append(single)

			if not pattern_matches:
				empty_results = no_results(search_item)

				if empty_results:
					continue #prompt for a new string input if 0 results are generated from the previous string
				break # prompt the user for a new search; N - Main Menu; Y - Search Menu
				
			else:
				pattern_results = display_results(pattern_matches, search_item) # iterates over the entries that meet user's criteria

				if not pattern_results or pattern_results:
					break # prompt the user for a new search; N - Main Menu; Y - Search Menu


	def search_time(self):


		clear_screen()

		search_item = "time"

		while True:

			log_details = compile_log()

			while True:
				try:
					minutes_criteria = int(input("\nProvide an amount of time (in minutes) in order to search entries within the work log: "))
				except ValueError:
					print("To search time entries, only integers are permitted (15, 30, etc.)")
				else:
					break

			minutes_tasked = []

			for t_entry in log_details:
				minutes_logged =  datetime.datetime.strptime(t_entry['minutes'], "%H:%M").time() # a datetime time object 

				if minutes_logged.hour >= 1:
					total_task_minutes = (60 * minutes_logged.hour) + minutes_logged.minute
				else:
					total_task_minutes = minutes_logged.minute

				if minutes_criteria == total_task_minutes:
					minutes_tasked.append(t_entry)

			if not minutes_tasked:
				empty_results = no_results(search_item)

				if empty_results:
					continue # prompt for a new time input if 0 results are generated from the previous time
				break # prompt the user for a new search; N - Main Menu; Y - Search Menu
			else:
				timing_results = display_results(minutes_tasked, search_item) # iterates over the entries that meet user's criteria

				if not timing_results or timing_results:
					break # prompt the user for a new search; N - Main Menu; Y - Search Menu


	def delete_entry(self):

		clear_screen()

		read_data = compile_log()

		string_query = input("\nProvide the task that you want to remove from the log: ").title().strip()

		while not string_query:
			string_query = input("Cannot delete a task with an empty query: ")

		entries_present = filter(lambda x: x['task'] == string_query, read_data)

		if not entries_present:
			print("The provided information doesn't exist in the log. You will be redirected to the Main Menu.")
			return

		remove_entry = None

		for _task in entries_present:
			delete_row = input("Do you want to delete the following: {date} / {task} / {details}\n\n>>>".format(**_task)).upper()

			while delete_row != "Y":
				delete_row = input("To select this row to be deleted please press [ Y ]: ").upper()
				
			remove_entry = _task
			clear_screen()
			break

		if not remove_entry:
			print("No entry was selected to be deleted. You will be redirected to the Main Menu.")
			return
		else:
			with open("worklog_entries.csv", 'r') as read_log, open("updated_entries.csv",'w') as write_log:
			
				fieldnames = ["date", "task", "details", "minutes"]

				data_writer= csv.DictWriter(write_log, fieldnames=fieldnames)
				data_reader = csv.DictReader(read_log, fieldnames=fieldnames)

				for unique in data_reader:
					if unique != _task:
						data_writer.writerow(unique)

		shutil.copyfile("updated_entries.csv", "worklog_entries.csv")
		os.remove("updated_entries.csv")

				
if '__main__' == __name__:
	WorkLog()