from colorama import Fore, Style
import requests
import json

class TeamScrap:
	def __init__(self, bearer_token):
		self.header = {
			'Authorization': 'Bearer ' + bearer_token
		}

	def get_classes(self, ids=None):
		if not ids:
			class_list_endpoint = 'https://assignments.onenote.com/api/v1.0/edu/me/classes/'

			req = requests.get(class_list_endpoint, headers=self.header)

			if int(req.status_code) == 401:
				raise Exception('401 Unauthorized - Token inválido')
				return
			else:
				return json.loads(req.text)
		else:
			class_list_endpoint = 'https://assignments.onenote.com/api/v1.0/edu/me/classes/{}'
			classesInfo = []

			for classId in ids:
				req = requests.get(class_list_endpoint.format(classId), headers=self.header)

				if int(req.status_code) == 401:
					raise Exception('401 Unauthorized - Token inválido')
					return
				else:
					classeInfo = json.loads(req.text)
					classesInfo.append(classeInfo)

			return classesInfo


	def get_all_classes_assignments(self):
		class_assignments_endpoint = 'https://assignments.onenote.com/api/v1.0/edu/classes/{}/assignments'

		classesInfo = self.get_classes()
		classesId = []
		classesAssignments = []

		for classInfo in classesInfo['value']:
			classesId.append(classInfo['id'])

		for classId in classesId:
			req = requests.get(class_assignments_endpoint.format(classId), headers=self.header)

			assignmentsJson = json.loads(req.text)

			for assignment in assignmentsJson['value']:
				currentClassInfo = self.get_classes([classId])

				if not assignment['isCompleted']:
					classesAssignments.append({ 'assignmentInfo': assignment, 'classInfo': currentClassInfo })

		return classesAssignments
