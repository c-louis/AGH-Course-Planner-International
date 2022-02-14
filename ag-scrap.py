#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import re
from enum import Enum
import csv
import sys
import json

class Examination(Enum):
	EXAM = 0
	ASSESSMENT = 1



class Course:
	def __init__(self, tr):
		cases = tr.find_all('td')
		self.id = cases[0].contents[1].get('id')
		self.name = cases[0].get_text().strip()

		lecture = re.findall(r'Lecture: ([0-9]{1,3})', cases[1].get_text())
		self.lecture = int(lecture[0]) if len(lecture) > 0 else 0
		laboratory = re.findall(r'Laboratory classes: ([0-9]{1,3})', cases[1].get_text())
		self.laboratory = int(laboratory[0]) if len(laboratory) > 0 else 0
		auditorium = re.findall(r'Auditorium classes: ([0-9]{1,3})', cases[1].get_text())
		self.auditorium = int(auditorium[0]) if len(auditorium) > 0 else 0
		project = re.findall(r'Project classes: ([0-9]{1,3})', cases[1].get_text())
		self.project = int(project[0]) if len(project) > 0 else 0
		
		self.credit = int(float(cases[2].get_text().strip()))

		self.examination = Examination.EXAM if cases[3].get_text().strip() == 'Exam' else Examination.ASSESSMENT
		#print(f'{self.name} ({self.id}) : \n\tL:{self.lecture} \n\tLAB:{self.laboratory} \n\tA:{self.auditorium} \n\tP:{self.project} \n\tCredit:{self.credit} \n\tExamination:{self.examination}')
	def asArray(self):
		return [self.id, self.name, self.lecture, self.laboratory, self.auditorium, self.project, self.credit, self.examination.name]
	def getDetailHtml(self):
		response = requests.get('https://sylabusy.agh.edu.pl/en/document/' + self.id + '.jsonHtml')
		html = json.loads(response.content)['html']
		soup = BeautifulSoup(html, 'html.parser')
		elements = soup.body.contents[1:-1]
		elemStr = [str(elem) for elem in elements]
		asString = "<div>" + "".join(elemStr) + "</div>"

		with open('./data/' + self.id + '.html', 'w') as htmlFile:
			htmlFile.write(asString)


# Winter : syl-grid-group syl-group-57571-element
# Summer : syl-grid-group syl-group-55100-element
def getCourses():
	response = requests.get('https://sylabusy.agh.edu.pl/en/2/2/17/1/9/55/137')
	if response.status_code != 200:
		print(f"Can't get page data, got : {response.status_code}")
		exit()

	soup = BeautifulSoup(response.content, 'html.parser')

	winters = soup.find_all(class_="syl-grid-group syl-group-57571-element")
	summers = soup.find_all(class_="syl-grid-group syl-group-55100-element")

	winterAvailableCourses = []
	summerAvailableCourses = []
	for tr in winters:
		winterAvailableCourses.append(Course(tr))
	for tr in summers:
		summerAvailableCourses.append(Course(tr))
	return winterAvailableCourses, summerAvailableCourses

def main():
	winters, summers = getCourses()

	with open('winter_courses.csv', 'w', newline='') as csvfile:
		winterWriter = csv.writer(csvfile)
		for course in winters:
			winterWriter.writerow(course.asArray())
	with open('summer_courses.csv', 'w', newline='') as csvfile:
		summerWriter = csv.writer(csvfile)
		for course in summers:
			summerWriter.writerow(course.asArray())

	for course in winters:
		course.getDetailHtml()
	for course in summers:
		course.getDetailHtml()

if __name__ == '__main__':
	sys.exit(main())

# https://sylabusy.agh.edu.pl/en/document/b39fbd3f-6e23-4845-9649-9b7e2f25acd6.jsonHtml