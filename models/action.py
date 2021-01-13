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