from NyaaPy.nyaa import Nyaa
import json
from os.path import exists
import os
import time
import re

global dataFolder
dataFolder = "E:\\Projects\\vscode\\_MachineLearning\\nyaaCategorizer\\data"

mullvadLocations = ["al", "it", "at", "be", "br", "bg", "ca", "hr", "cz", "dk", "ee", "fi", "fr", "de", "hk", "hu", "ie", "il", "au"]

def nyaaScraper():
    sorting = ["comments", "size", "id", "seeders", "leechers", "downloads"]
    order = ["asc", "desc"]
    
    catsubcatdict = {
        "All categories": ['0', '0'],
        
        "Anime": ['1', '0'],
        'Anime - Anime Music Video': ['1', '1'],
        'Anime - English-translated': ['1', '2'],
        'Anime - Non-English-translated': ['1', '3'],
        'Anime - Raw': ['1', '4'],
        
        'Audio': ['2', '0'],
        'Audio - Lossless': ['2', '1'],
        'Audio - Lossy': ['2', '2'],
        
        'Literature': ['3', '0'],
        'Literature - English-translated': ['3', '1'],
        'Literature - Non-English-translated': ['3', '2'],
        'Literature - Raw': ['3', '3'],
        
        'Live Action': ['4', '0'],
        'Live Action - English-translated': ['4', '1'],
        'Live Action - Idol_Promotional Video': ['4', '2'],
        'Live Action - Non-English-translated': ['4', '3'],
        'Live Action - Raw': ['4', '4'],
        
        'Pictures': ['5', '0'],
        'Pictures - Graphics': ['5', '1'],
        'Pictures - Photos': ['5', '2'],
        
        'Software': ['6', '0'],
        'Software - Applications': ['6', '1'],
        'Software - Games': ['6', '2']
    }

    nyaa = Nyaa("https://nyaa.si")
    allids = set()
    for key in catsubcatdict:
        val = catsubcatdict[key]
        incat = set()
        
        for s in sorting:
            for o in order:
                for i in range(1, 14): # 14 is enough for 1000
                    test_search = nyaa.search(" ", category=val[0], subcategory=val[1], page=i, sorting=s, order=o)
                    ids = [torrent.id for torrent in test_search]
                    allids |= set(ids)
                    incat |= set(ids)
        print(f"Found {len(incat)} ids in {key}")
        f = open(f"data/{key}.txt", "w")
        for x in incat:
            f.write(x + "\n") # files one extra \n
        
    print(f"Found total: {len(allids)} ids")

    f = open("data/everything.txt", "w+")
    for x in allids:
        f.write(x + "\n")

def printTorrent(torrent):
    print(vars(torrent))

def sbsScraper():
    nyaa = Nyaa("https://nyaa.sbs")
    file = open("trueIds.txt", "a+")
    for i in range(1, 3586):
        print(f"Page: {i}")
        test_search = nyaa.search("", url=f"?page={i}")
        ids = [torrent.id for torrent in test_search]
        for x in ids:
            file.write(x + "\n")
    file.close()

def saveUnique(filename):
    f = open(filename, "r", encoding="utf-8").read().split('\n')
    f = set(f)
    nf = open(filename.replace('.txt', '') + '_uq.txt', "w+", encoding="utf-8")
    for x in f:
        nf.write(x + "\n")


global files
files = {}# so they dont have to be opened repetedly

def savePost(postData):
    fname = dataFolder + "\\" + postData.category.replace('/', '_') + ".txt"
    if fname not in files:
        files[fname] = open(fname, "a", encoding="utf-8")
    files[fname].write(str(vars(postData)) + ",\n")

def getAllPostInfo():
    nyaa = Nyaa("https://nyaa.sbs")
    idFile = open(dataFolder + "\\tids.txt", "r")
    idList = idFile.read().split('\n')
    mullvadLocIndex = 0
    print(len(idList))
    for i in range(54700, len(idList)):
        id = idList[i]
        if i % 100 == 0:
            print(f"Working on: {i}")
        result = nyaa.get(id)
        while result == None:
            print(f"Changing VPN server to {mullvadLocations[mullvadLocIndex]} on index {i}:{id}: ")
            os.system(f"mullvad.exe relay set location {mullvadLocations[mullvadLocIndex]}")
            mullvadLocIndex = (mullvadLocIndex + 1) % len(mullvadLocations)
            time.sleep(20) # give time to actually switch servers
            result = nyaa.get(id)
        
        result.id = id
        if len(result.files) > 100:
            print(f"{i}:{id} has {len(result.files)} files. Truncating to 100.")
            result.files = result.files[0:100]
            result.files.append("...")
        savePost(result)

def saveAllDataUnique():
    for x in os.listdir(dataFolder):
        saveUnique(dataFolder + "\\" + x)

def attrVariants(txt, someKey):
    keyStr1 = f"', '{someKey}': '"
    keyStr2 = f"\", '{someKey}': '"
    keyStr3 = f"', '{someKey}': \""
    keyStr4 = f"\", '{someKey}': \""
    correct = f'", "{someKey}": "'
    return txt.replace(keyStr1, correct).replace(keyStr2, correct).replace(keyStr3, correct).replace(keyStr4, correct)

def repFilesVar(txt):
    # hash is before files, so no need to check for " in hash string
    txt = txt.replace("', 'files': ['", "\", 'files': ['") # fix hash string
    lines = txt.split('\n')
    ntext = ""
    for line in lines:
        filesStart = line.find("'files': [")
        filesEnd = line.find("], 'description': ")
        nline = line[:filesStart] + line[filesStart:filesEnd].replace("', '", "\", \"").replace("', \"", "\", \"").replace("\", '", "\", \"") + line[filesEnd:]
        ntext += nline + "\n"
    ntext = ntext.replace("'files': ['", "\"files\": [\"").replace("'files': [", "\"files\": [").replace("'], 'description': ", "\"], 'description': ")
    return ntext

def repDescVar(txt):
    return txt.replace("'description': '", '"description": "').replace("'description': \"", '"description": "')

def repVars(txt):
    txt = txt.replace("'title': '", '"title ": "') # manual for first '
    txt = txt.replace("'title': \"", '"title": "')
    txt = repFilesVar(txt) # files done separately since it contains array of elements
    txt = repDescVar(txt) # description done separately since its after files
    keys = ["category", "uploader", "uploader_profile", "website", "size", "date", "seeders", "leechers", "completed", 
            "hash", "id"]
    for x in keys:
        txt = attrVariants(txt, x)
    txt = txt.replace("'},", '"},') # manual for last '
    return txt

def escapeFilesAttr(line): # might separate a file into two files accidentaly, will still yield valid json
    middleStart = line.find(", 'files': [") + 3 + len("files") + 5
    middleEnd = line.find(", 'description': ") - 2 # middle = a", 'b', "'v", "arsta
    middle = line[middleStart:middleEnd]
    # print(middle)
    fileSepIdx = [int(m.start()) for m in re.finditer("', '", middle)]
    fileSepIdx += [int(m.start()) for m in re.finditer("\", '", middle)]
    fileSepIdx += [int(m.start()) for m in re.finditer("', \"", middle)]
    fileSepIdx += [int(m.start()) for m in re.finditer("\", \"", middle)]
    fileSepIdx = list(sorted(set(fileSepIdx)))
    fixedMiddle = ""
    # print(fileSepIdx)
    for i in range(len(fileSepIdx)):
        if i == 0:
            prevInd = 0
        else:
            prevInd = fileSepIdx[i - 1] + 4
        curInd = fileSepIdx[i]
        fixedMiddle += middle[prevInd:curInd].replace("\"", "\\\"")
        fixedMiddle += '", "'
            
    # add last file
    if len(fileSepIdx) > 0: 
        fixedMiddle += middle[(fileSepIdx[len(fileSepIdx) - 1] + 4):].replace("\"", "\\\"")
    else:
        fixedMiddle += middle.replace("\"", "\\\"")
    
    nline = f", \"files\": [\"" + fixedMiddle + '"]'
    return nline

def escapeJSON(txt):
    # i want to escape all doublequotes(") that do not mark a variable
    keys = ["title", "category", "uploader", "uploader_profile", "website", "size", "date", "seeders", "leechers", "completed", "hash", "files", "description", "id"]
    lines = txt[:-2].replace("\\", "\\\\").split('\n')
    ntext = ""
    for line in lines:
        if lines.index(line) % 100 == 0: 
            print("Line: " + str(lines.index(line)))
        nline = ""
        for i in range(len(keys)):
            if keys[i] == "files":
                nline += escapeFilesAttr(line)
                continue
            
            if i != len(keys) - 1:
                curKey = keys[i]
                nextKey = keys[i + 1]
                if i == 0:
                    ckStart = 11
                else:
                    ckStart = line.find(f", '{curKey}': ") + 3 + len(curKey) + 4
                ckEnd = line.find(f", '{nextKey}': ") - 1 # exclusive
            else:
                curKey = keys[i]
                ckStart = line.find(f", '{curKey}': ") + 3 + len(curKey) + 4
                ckEnd = line[ckStart:].find("},") - 1
            
            if i != 0:
                nline += f", \"{curKey}\": \"" + line[ckStart:ckEnd].replace('"', '\\\"') + '"'
            else:
                nline += f"\"{curKey}\": \"" + line[ckStart:ckEnd].replace('"', '\\\"') + '"'
        ntext += "{" + nline + "},\n"
    return "[" + ntext[:-2] + "]"

def saveAllAsJson():
    for x in os.listdir(dataFolder):
        if ".json" in x or x == "nonUnique" or x == "pureUnique" or x == "tids_uq.txt":
            continue
        print(f"On {x}.")
        f = open(dataFolder + "\\" + x, "r", encoding="utf-8")
        txt = escapeJSON(f.read())
        nf = open(dataFolder + "\\" + x.replace("_uq.txt", ".json"), "w", encoding="utf-8")
        nf.write(txt)
        
        #check if correct:
        data = json.loads(txt)
        print(len(data))

def testJSON():
    f = open("E:\\Projects\\vscode\\_MachineLearning\\nyaaCategorizer\\src\\testfile.txt", "r", encoding="utf-8")
    txt = escapeJSON(f.read())
    nf = open("E:\\Projects\\vscode\\_MachineLearning\\nyaaCategorizer\\src\\testfile.json", "w", encoding="utf-8")
    nf.write(txt)
    
def getLens():
    total = 0
    ptotal = 0
    for x in os.listdir(dataFolder + "\\json"):
        f = open(dataFolder + "\\json\\" + x, "r", encoding="utf-8")
        data = json.load(f)
        total += len(data)
        print(x + ": " + str(len(data)))
    print(f"Total: {total}")
    
def combineJSON():
    everything = []
    for x in os.listdir(dataFolder + "\\json"):
        f = open(dataFolder + "\\json\\" + x, "r", encoding="utf-8")
        data = json.load(f)
        everything += data
    f = open("all_Pretty.json", "w", encoding="utf-8")
    json.dump(everything, f, ensure_ascii=False, indent=4)
    
combineJSON()