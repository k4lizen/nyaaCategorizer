import pandas as pd
import math


def setupFileAmount(df):
    fileAmount = []
    for index, row in df.iterrows():
        if row['files'][-1] == "...":
            fileAmount.append(200)
        else:
            fileAmount.append(len(row['files']))
        
    df["fileAmount"] = fileAmount
    df["more100Files"] = (df.fileAmount > 100).astype(int)
    return df

def setupFileSize(df):
    fileSize = []
    for index, row in df.iterrows():
        szval = 0
        last3 = row['size'][-3:]
        match last3:
            case "tes":
                szval += float(row['size'][:-6])
            case "KiB":
                szval += float(row['size'][:-4]) * 1024
            case "MiB":
                szval += float(row['size'][:-4]) * 1024 * 1024
            case "GiB":
                szval += float(row['size'][:-4]) * 1024 * 1024 * 1024
            case "TiB":
                szval += float(row['size'][:-4]) * 1024 * 1024 * 1024 * 1024
            case _:
                df.drop(index, inplace=True)
                
        if szval != 0:
            szvalnorm = math.log(szval)
            fileSize.append(szvalnorm)
    df = df.drop('size', axis=1)
    df["fileSize"] = fileSize
    return df

def concatFiles(df):
    filesArr = []
    for index, row in df.iterrows():
        runStr = ""
        for i in range(len(row['files'])):
            runStr += row['files'][i]
            if i != len(row['files']) - 1:
                runStr += " / "
        filesArr.append(runStr)
    df["files"] = filesArr
    return df
    
def noSubCategory(df):
    ncat = []
    for index, row in df.iterrows():
        ncat.append(row['category'].split('-')[0])
    df['category'] = ncat
    return df

df = pd.read_json("data/all.json")
# df = pd.read_json("data/json/Anime-Anime Music Video.json")

df = df[['title', 'size', 'files', 'description', 'category']]

df = setupFileAmount(df)
df = setupFileSize(df)
df = concatFiles(df)
df = noSubCategory(df)

df.to_csv('procData_nosub.csv', index=False)