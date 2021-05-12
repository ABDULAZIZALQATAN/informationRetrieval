from datetime import datetime
import shutil as shu
def printCurrentTime(title):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(title , ": date and time =", dt_string)
    return now

def getCorpus(c):
    switcher = {
        'A': 'AQUAINT',
        'C': 'CORE17',
        'W': 'WAPO'
    }
    return switcher.get(c.upper())

def getModelCoefficient(model):
    switcher = {
        'BM25': 'b',
        'PL2': 'c',
        'LMD': 'mu'
    }
    return switcher.get(model)

def getQryExpansion(c):
    switcher = {
        'A': 'AX',
        'B': 'Baseline',
        'R': 'RM3'
    }
    return switcher.get(c.upper())

def getResHeader():
    return ['qryID','dum','docid','rank','score','tag']

def getGainFile(c):
    # switcher = {
    #     'A': 'Aquaint-AnseriniQrel.qrel',
    #     'C': '307-690.qrel',
    #     'W': 'qrels.core18.txt'
    # }
    # result = '~/trec_eval/Qrels/' + switcher.get(c[0].upper())

    corpus = getCorpus(c[0])
    result = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\Resources\%s\%s.qrel' % (corpus,corpus)
    return result

def copyFile (src,dest):
    # copyFile(src,dest)
    shu.copy2(src,dest)

def getLinuxPath (path):
    # Windows Path : C:\Users\kkb19103\Desktop\new\data
    # Linux Path : /mnt/c/Users/kkb19103/Desktop/new/data
    replacements = {
        'C:':'/mnt/c',
        '\\':'/',
        # '\\':'\\'
    }
    result = path
    for key , val in replacements.items():
        result = result.replace(key,val)
    return result