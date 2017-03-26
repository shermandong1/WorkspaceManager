import os, sys

def readFile():
	inputfile = open('homework.workspace', 'r')
	workspaces = {}
	workspace = []
	for line in inputfile.readlines():
		if '\\' in line:
			name = line[2:].strip()
			workspaces[name] = workspace
			workspace = []
		else:
			workspace.append(line.strip())
	
	inputfile.close()

	return workspaces


def listWorkspaces(workspaces):
	for workspace in workspaces:
		print(workspace)
		for application in workspaces[workspace]:
			print('\t' + application)

def addWorkspace(workspaces, newWorkspaceName):
	# newWorkspaceName = input("Enter the name of your new workspace: ")
	if newWorkspaceName not in workspaces:
		workspaces[newWorkspaceName] = []

def addApplicationToWorkspace(workspaces, workspaceName, newApplicationName):
	if workspaceName not in workspaces:
		print('Error: this workspace does not exist')
		return
	if newApplicationName in workspaces[workspaceName]:
		print('Error: this application is already in this workspace')
	else:
		workspaces[workspaceName].append(newApplicationName)

# takes in workspaces and saves it into a file in the correct format
def saveFile(workspaces):
	outputfile = open('homework.workspace', 'w')
	fileString = ''
	for workspace in workspaces:
		for application in workspaces[workspace]:
			fileString += application + '\n'
		fileString += '\\ ' + workspace + '\n'
	outputfile.write(fileString)
	outputfile.close()

def openWorkspace(workspaces, workspaceName):
	if workspaceName not in workspaces:
		print('invalid request')
		return
	for applicationName in workspaces[workspaceName]:
		print("Application Name: " + applicationName)
		os.system('open -a \'' + applicationName + '\'')

def removeApplicationFromWorkspace(workspaces, workspaceName, applicationName):
	if workspaceName not in workspaces:
		print('invalid workspace name')
		return
	if applicationName not in workspaces[workspaceName]:
		print('application not in workspace')
		return
	workspaces[workspaceName].remove(applicationName)

# returns true if the given application exists,
# returns false otherwise

def logApplications():
	applicationsArray = []
	os.system('sudo find / -iname *.app > applications.txt')
	applications = open('applications.txt', 'r')
	for line in applications:
		words = line.split('/')
		appName = words[len(words) - 1].strip().lower()
		appName = appName[ : len(appName) - 4]
		print(appName)
		if appName not in applicationsArray:
			applicationsArray.append(appName)
	applications.close()
	applications = open('applicationNames.txt', 'w')
	for applicationName in applicationsArray:
		applications.write(applicationName + '\n')
	applications.close()

def verifyApplication(applicationName):
	applicationNames = open('applicationNames.txt', 'r')
	for name in applicationNames:
		if applicationName.strip().lower() == name.strip().lower():
			return True
	return False



# CREATE: creates new workspace
#	CREATE workspace_name
# ADD: add new application to a workspace
#	ADD workspace_name application_name
# OPEN: opens workspace
#	python workspaceManager.py workspace_name
# LIST: lists workspaces
#	LIST
# LOG: logs application names
# REMOVE: removes application from workspace
# 
def main():
	workspaces = readFile()
	argv = sys.argv
	# print(argv)
	if len(argv) == 1:
		print('usage: ')
		return

	command = argv[1].lower()

	if command == 'create':
		newWorkspaceName = argv[2].strip()
		addWorkspace(workspaces, newWorkspaceName)

	elif command == 'add':
		if len(argv) < 4:
			print('invalid request')
		newApplicationName = ''
		workspaceName = argv[2]
		for i in range(3, len(argv)):
			newApplicationName += argv[i] + ' '
		newApplicationName = newApplicationName.strip().lower()
		if not verifyApplication(newApplicationName):
			print('invalid application name')
			return
		addApplicationToWorkspace(workspaces, workspaceName, newApplicationName)

	elif command == 'list':
		listWorkspaces(workspaces)
		return

	elif command == 'remove':
		applicationName = ''
		workspaceName = argv[2]
		for i in range(3, len(argv)):
			applicationName += argv[i] + ' '
		applicationName = applicationName.strip().lower()
		removeApplicationFromWorkspace(workspaces, workspaceName, applicationName)

	elif command == 'log':
		logApplications()

	else:
		openWorkspace(workspaces, argv[1])
	# listWorkspaces(workspaces)
	saveFile(workspaces)



main()