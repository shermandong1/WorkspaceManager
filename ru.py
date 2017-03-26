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


# takes an array of menu items corresponding to workspace names
# sets callback functions for each item

def updateOpenListeners(menuItems):
    for item in menuItems:
        function = createOpenCallback(item[1].title)
        #print(function)
        item[1].set_callback(function)


def createOpenCallback(workspaceName):
    def callback():
        os.system('python3 workspaceManager.py open ' + workspaceName)
    return callback


class AwesomeStatusBarApp(rumps.App):
    def __init__(self):

        super(AwesomeStatusBarApp, self).__init__("Awesome App")
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
        #print(applications)
        self.menu = [["Open", workspaceNames], ["Add", workspaceNames], ["Remove", applications]]
        print(self.menu["Open"].items())
        updateOpenListeners(self.menu["Open"].items())

    # @rumps.clicked("Say hi")
    # def sayhi(self, _):
    #     rumps.notification("Awesome title", "amazing subtitle", "hi!!1")

    colors = ["red", "green", "blue"]

    for color in colors:
        @rumps.clicked(color)
        def sayColor(self, _):
            rumps.notification(color)

    # for workspace in workspaces:
    #     for app in workspaces[workspace]:
    #         menuitem.set_callback(os.system())

    # @rumps.clicked(workspaceNames[0])
    # def sayhi(self, _):
    #     rumps.notification("This worked")

if __name__ == "__main__":
    AwesomeStatusBarApp().run()

