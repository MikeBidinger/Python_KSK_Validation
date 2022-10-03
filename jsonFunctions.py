import json

def writeJSON(filePath:str, dictData:dict):
    f = open(filePath, 'w')
    #pp(dictData)
    jsStr = json.dumps(dictData, indent=4)
    #print(jsStr)
    f.write(jsStr)
    f.close()

def readJSON(filePath:str):
    dict = {}
    f = open(filePath, 'r')
    jsStr = f.read()
    #print(jsStr)
    dict = json.loads(jsStr)
    #pp(dict)
    f.close()
    return dict
