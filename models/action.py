from core.models import action, webui
from core import helpers, logging
import os

class _localDelete(action._action):
    localFile = str()

    class _properties(webui._properties):
        def generate(self,classObject):
            formData = []
            formData.append({"type" : "break", "start" : True, "schemaitem": "Local Options"})
            formData.append({"type" : "input", "schemaitem" : "localFile", "textbox" : classObject.localFile, "label" : "local file", "tooltip" : "The local filename (including full path) to be deleted"})
            formData.append({"type" : "break", "start" : False, "schemaitem": "Local Options"})
            formData.append({"type" : "break", "start" : True, "schemaitem": "Core Options"})
            formData.append({"type" : "input", "schemaitem" : "_id", "textbox" : classObject._id})
            formData.append({"type" : "input", "schemaitem" : "name", "textbox" : classObject.name})
            formData.append({"type" : "checkbox", "schemaitem" : "enabled", "checked" : classObject.enabled})
            formData.append({"type" : "json-input", "schemaitem" : "varDefinitions", "textbox" : classObject.varDefinitions})
            formData.append({"type" : "input", "schemaitem" : "logicString", "textbox" : classObject.logicString})
            formData.append({"type" : "checkbox", "schemaitem" : "log", "checked" : classObject.log})
            formData.append({"type" : "input", "schemaitem" : "comment", "textbox" : classObject.comment})
            return formData
    
    def run(self,data,persistentData,actionResult):
        localFile = helpers.evalString(self.localFile,{"data" : data})

        actionResult["result"] = False
        actionResult["rc"] = 404
        if os.path.exists(localFile):
            try:
                os.remove(localFile)
                actionResult["msg"] = "File removed succesfully"
                actionResult["result"] = True
                actionResult["rc"] = 0
            except Exception as errMsg:
                actionResult["msg"] = errMsg
                actionResult["rc"] = 500
        else:
            actionResult["msg"] = "File does not exist"
        return actionResult

class _localWrite(action._action):
    localFile = str()
    fileData = str()
    append = bool()
    insert_newlines = bool()

    class _properties(webui._properties):
        def generate(self,classObject):
            formData = []
            formData.append({"type" : "break", "start" : True, "schemaitem": "Local Options"})
            formData.append({"type" : "input", "schemaitem" : "localFile", "textbox" : classObject.localFile, "label" : "local file", "tooltip" : "The local filename (including full path) to be written"})
            formData.append({"type" : "input", "schemaitem" : "fileData", "textbox" : classObject.fileData, "label" : "file data", "tooltip" : "The data to be written to the file"})
            formData.append({"type" : "checkbox", "schemaitem" : "append", "checked" : classObject.append, "label" : "append", "tooltip" : "Whether to append or overwrite the file"})
            formData.append({"type" : "checkbox", "schemaitem" : "insert_newlines", "checked" : classObject.insert_newlines, "label" : "insert newlines", "tooltip" : "Automatically add a newline when appending"})
            formData.append({"type" : "break", "start" : False, "schemaitem": "Local Options"})
            formData.append({"type" : "break", "start" : True, "schemaitem": "Core Options"})
            formData.append({"type" : "input", "schemaitem" : "_id", "textbox" : classObject._id})
            formData.append({"type" : "input", "schemaitem" : "name", "textbox" : classObject.name})
            formData.append({"type" : "checkbox", "schemaitem" : "enabled", "checked" : classObject.enabled})
            formData.append({"type" : "json-input", "schemaitem" : "varDefinitions", "textbox" : classObject.varDefinitions})
            formData.append({"type" : "input", "schemaitem" : "logicString", "textbox" : classObject.logicString})
            formData.append({"type" : "checkbox", "schemaitem" : "log", "checked" : classObject.log})
            formData.append({"type" : "input", "schemaitem" : "comment", "textbox" : classObject.comment})
            return formData
    
    def run(self,data,persistentData,actionResult):
        localFile = helpers.evalString(self.localFile,{"data" : data})
        fileData = helpers.evalString(self.fileData,{"data" : data})

        actionResult["result"] = False
        actionResult["rc"] = 404
        try:
            #Fixing new lines
            fileData = fileData.replace("\\n","\n")
            if self.append:
                with open(localFile,"a") as outputFile:
                    if self.insert_newlines:
                        outputFile.write("\n")
                    outputFile.write(fileData)
            else:
                with open(localFile,"w") as outputFile:
                    outputFile.write(fileData)
            actionResult["msg"] = "File written to successfully"
            actionResult["result"] = True
            actionResult["rc"] = 0
        except Exception as errMsg:
            actionResult["msg"] = errMsg
            actionResult["rc"] = 500
        return actionResult