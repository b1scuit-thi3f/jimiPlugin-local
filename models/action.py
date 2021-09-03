from core.models import action, webui
from core import helpers
import os
import json
import csv

class _localDelete(action._action):
    localFile = str()
    
    def doAction(self,data):
        localFile = helpers.evalString(self.localFile,{"data" : data["flowData"]})

        if os.path.exists(localFile):
            try:
                os.remove(localFile)
                return {"result":True,"rc":0,"msg":"File removed succesfully"}
            except Exception as errMsg:
                return {"result":False,"rc":500,"msg":errMsg}
        return {"result":False,"rc":404,"msg":"File not found"}

class _localWrite(action._action):
    localFile = str()
    fileData = str()
    append = bool()
    insert_newlines = bool()
    
    def doAction(self,data):
        localFile = helpers.evalString(self.localFile,{"data" : data["flowData"]})
        fileData = helpers.evalString(self.fileData,{"data" : data["flowData"]})

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
            return {"result":True,"rc":0,"msg":"File written to successfully"}
        except Exception as errMsg:
            return {"result":False,"rc":500,"msg":errMsg}

class _localRead(action._action):
    localFile = str()
    outputType = "raw"
    defaultToRaw = True #Just reads file as is if csv/json etc fails
    customCSVOptions = bool()
    delimiter = ","
    quoteCharacter = "\""

    def doAction(self,data):
        localFile = helpers.evalString(self.localFile,{"data" : data["flowData"]})

        if os.path.exists(localFile):
            try:
                if self.outputType == "raw":
                    with open(localFile,"r") as inputFile:
                        resultData = inputFile.read()

                elif self.outputType == "json":
                    with open(localFile,"r") as inputFile:
                        resultData = json.load(inputFile)

                elif self.outputType == "csv":
                    resultData = []
                    with open(localFile,"r") as inputFile:
                        csvReader = csv.reader(inputFile, delimiter=self.delimiter, quotechar=self.quoteCharacter)
                        for row in csvReader:
                            resultData.append(",".join(row))
                    resultData = "\n".join(resultData)

                return {"result":True,"rc":0,"data":resultData,"msg":"File read successfully"}

            except Exception as errMsg:
                return {"result":False,"rc":500,"msg":str(errMsg)}

        else:
            return {"result":False,"rc":404,"msg":"File not found"}
