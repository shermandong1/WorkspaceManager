import rumps
import os

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

def verifyApplication(applicationName):
    applicationNames = open('applicationNames.txt', 'r')
    for name in applicationNames:
        if applicationName.strip().lower() == name.strip().lower():
            return True
    return False

class WorkspaceManager(rumps.App):

    def updateOpenListeners(self, menuItems):
        for item in menuItems: 
            item[1].set_callback(self.createCallback('', item[1].title))

    def updateRemoveListeners(self, menu):
        for item in menu[1].items():
            item[1].set_callback(self.createCallback('remove', menu[1].title + ' ' + item[1].title))

    def updateAddListeners(self, menu):
        for item in menu:
            item[1].set_callback(self.createAddCallback(item[1].title))



    def createCallback(self, workspaceCommand, workspaceArgs):
        mainApplication = self;
        def callback(self):
            os.system('python3 workspaceManager.py ' + workspaceCommand + ' ' + workspaceArgs)
            mainApplication.update()
        return callback


    def createAddCallback(self, workspaceName):
        myApplication = self
        def myCallback(self):
            myWindow = rumps.Window("", "Add an application", "application name", cancel=True, dimensions=(320, 25))
            response = myWindow.run()
            os.system('open -a python')
            invalidApplicationName = True
            while invalidApplicationName:
                if response.clicked:
                    #do stuff for clicked
                    invalidApplicationName = not verifyApplication(response.text.strip().lower())
                    if not invalidApplicationName:
                        os.system('python3 workspaceManager.py ' + 'add' + ' ' + workspaceName + ' ' + response.text.strip().lower())
                        myApplication.update()
                        break
                    else:
                        myWindow.message = "Invalid application name -- try again"
                        response = myWindow.run()
                else:
                    break
        return myCallback

    def createAddWorkspaceCallback(self, workspaceNames):
        myApplication = self
        def myCallback(self):
            myWindow = rumps.Window("", "Add a workspace", "workspace name", cancel=True, dimensions=(320, 25))
            response = myWindow.run()
            os.system('open -a python')
            invalidWorkspaceName = True
            while invalidWorkspaceName:
                myWindow.message = "Add a workspace"
                if response.clicked:
                    #do stuff for clicked
                    invalidWorkspaceName = response.text.strip().lower() in workspaceNames or ' ' in response.text.strip()
                    if not invalidWorkspaceName:
                        os.system('python3 workspaceManager.py ' + 'create' + ' ' + response.text.strip().lower())
                        myApplication.update()
                        break
                    elif ' ' in response.text.strip():
                        myWindow.message = "Workspace names may only be one word long"
                        response = myWindow.run()
                    else:
                        myWindow.message = "Invalid workspace name -- try again"
                        response = myWindow.run()
                else:
                    break
        return myCallback

    def update(self):
        self.updateMenu()
        self.updateOpenListeners(self.menu["Open Workspace"].items())
        for it in self.menu["Remove Application"].items():
            self.updateRemoveListeners(it)
        self.updateAddListeners(self.menu["Add Application"].items())

    def __init__(self):
        super(WorkspaceManager, self).__init__("Workspace Manager", quit_button = None, icon = 'icon.png')
        self.update()


    def updateMenu(self):
        workspaces = readFile()
        workspaceNames = []
        for workspace in workspaces:
            workspaceNames.append(workspace)
        applications = []
        for workspace in workspaces:
            a = []
            a.append(workspace)
            arrayOfApps = []
            for app in workspaces[workspace]:
                arrayOfApps.append(app)
            a.append(arrayOfApps)
            applications.append(a)
        self.menu.clear()
        self.menu = ["Add Workspace", ["Open Workspace", workspaceNames], ["Add Application", workspaceNames], \
                     ["Remove Application", applications],  "Quit"]
        def quit(self):
            rumps.quit_application()
        self.menu["Quit"].set_callback(quit)
        self.menu["Add Workspace"].set_callback(self.createAddWorkspaceCallback(workspaceNames))


if __name__ == "__main__":
    WorkspaceManager().run()

