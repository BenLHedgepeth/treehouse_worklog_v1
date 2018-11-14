import datetime
import re

from itertools import count
from test_funcs import test_date_format, test_time_format

class Task:

	NUM_TASKS = count(0)

	def __init__(self):
		self.task = self.store_task()
		self.date = self.store_date()
		self.details = self.store_task_details()
		self.minutes = self.store_time()

	def __str__(self):
		string_date = self.date.strftime('%Y-%m-%d')
		return f'Date: {string_date} - Task: {self.task}'

	def store_task(self):
		'''Record the type of task completed'''

		record_task = input("Provide the type of task performed: ").title()
		
		while not record_task or "No" in record_task:
			record_task = input(f'{record_task} is an invalid entry. Please provide a valid task: ')

		return record_task

	def store_date(self):
		'''Record the date the task took place'''
				
		calender_date = input("\nProvide the date the task was performed (YYYY-MM-DD): ")	

		official_date = test_date_format(calender_date)
		date_info = [item.lstrip('0') for item in official_date.split('-')] #intended for datetime object; datetime can't handle arguments with leading 0's
		year, month, day = date_info

		try:
			accept_date = datetime.date(year=int(year), month=int(month), day=int(day)) # test whether the arguments fall within datetime range values
		except ValueError: 				
		# exception occurs if user provides value(s) that fall outside the range permitted by datetime objects											
			return self.store_date()
		else:
			# return official_date
			return accept_date	

	def store_task_details(self):
		'''Record any relevant information about the task'''
		while True:
			work_info = input("\nProvide relevant notes about the task: ").title()

			if work_info:
				return work_info

	def store_time(self):
		'''Record the amount of time spent on the task'''
		while True:
			try:
				clocked_time = abs(int(input("\nProvide the amount of time spent on the task (in minutes): ")))
			except ValueError:
				print(f"Time must be recorded for the task that occurred. Whole integers only accepted.")
			else:
				if not clocked_time:
					continue
				break
		if clocked_time > 59:
			minutes = int(clocked_time % 60)
			hours = int((clocked_time - minutes) / 60)
		else: 
			minutes = clocked_time
			hours = 0

		return datetime.time(hour=hours, minute=minutes)





