
import python.src.pythonFiles.dedicatedProcess.XMLTopicsCreator as xml
import python.src.classes.trec  as trec
import python.src.classes.CWL as cwl
import python.src.classes.clsRetrievabilityCalculator as rc
import python.src.classes.bash as sh
import python.src.classes.general as gen

# File Types To Get with Function getFile
[
fQryList,
fBaseQryList,
fFirstStage
] = [*range(1, 4, 1)]

GQryDict = {}
GBaseDict = {}
GBias = False
GScoreBy = 'max'
GoutFile = False
GCorpus = ''
GModel = ''
GModelCoefficient = ''
GlobalDf = '10'

def runBash(out,index,qry):
    global GBias , GModel , GlobalDf

# WAPORevertedIndexDfbigger02 - WAPORevertedIndexDfbigger10

    # #     WAPO
    # 1)
    # corpusShort = core18
    # corpus = WAPO
    # corpusPrefix = WA \
    #     ;;
    # # CORE17
    # 2)
    # corpusShort = core17
    # corpus = CORE17
    # corpusPrefix = CO \
    #     ;;
    # # AQUAINT
    # 3)
    # corpusShort = robust05
    # corpus = AQUAINT
    # corpusPrefix = AQ

    if index.upper() == 'R' :
        index = '%sRevertedIndexDfbigger%s' % (GCorpus,GlobalDf)
    else:
        switcher = {
            'A': 'robust05',
            'C': 'core17',
            'W': 'core18'
        }
        corpusShort = switcher.get(GCorpus[0], '')
        index = 'lucene-index.%s.pos+docvectors+rawdocs' % corpusShort
    qry =  'revertedIndex/%sXML.qry' % qry
    hits = '100' if GBias else '1000'
    file = getFile('rindexRetrieval').replace('revertedIndex','bash') + '.sh'
    # file = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\LUCENE\anserini\bash\rindexRetrieval.sh'
    f = open(file,'r')
    lines = f.read()
    replacements = {
        '%index':index,
        '%qry':qry,
        '%hits':hits,
        '%out':out,
        '%model':GModel
    }

    for old,new in replacements.items():
        lines = lines.replace(old,new,2)
    newFile = file.replace('.sh','New.sh')
    f.close()
    f = open(newFile,'w')
    f.write(lines)
    f.close()
    cmd = r"cd ~/anserini/bash && cat %s | tr -d '\r' > %s && ./%s" % \
        ('rindexRetrievalNew.sh','rindexRetrievalNew1.sh','rindexRetrievalNew1.sh')
    sh.runBashCmd(cmd)

def getOutputLine (fbDocs , fbTerms , beta , eval):
    global GBias , GCorpus , GModel , GModelCoefficient , GlobalDf
    # Corpus,model,Df>,beta,fbDocs,fbTerms,RetrievalCoefficient,Trec-MAP,Trec-Bref,Trec-P10,
    # Trec-NDCG,CWL-MAP,CWL-NDCG,CWL-P10,CWL-RBP0.4,CWL-RBP0.6,CWL-RBP0.8

    # CSV
    # df =  '{:02d}'.format(GlobalDf)
    initial = 'REV,%s,%s,%s,%s,%d,%d,' % (GCorpus , GModel, GlobalDf , str(beta),fbDocs,fbTerms)
    if (GBias):
        temp = initial + '#b,%s,' % GModelCoefficient
        format = temp.replace('#b','0')  + ','.join(eval[:3] + [eval[6]]) + '\n' + \
                 temp.replace('#b','0.5') + ','.join(eval[3:])
    else :
        format = initial +  ','.join([GModelCoefficient] + eval)
    # Experiments Format
    # format = 'WAPO,123103,10,%d,%d,%s,' % (fbDocs,fbTerms,str(beta)) + ','.join(eval) + ',comments'
    return format

def getFile (inFile):
    mainFolder = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\LUCENE\anserini/'
    mainFolder = gen.getLinuxPath(mainFolder)
    # mainFolder = '~/anserini/revertedIndex/'
    rIndexFolder = mainFolder + 'revertedIndex/'
    fName = ''

    if (inFile == fQryList):
        qry = '300K' if GBias else '50'
        fName = mainFolder + 'Queries/standardQueries/%s/%s.qry' % (GCorpus,qry)
    elif (inFile == fBaseQryList):
        # WA-BaseQueries-Df-02.qry
        fName = mainFolder + 'Queries/baseQueries/%s/%s-BaseQueries-Df-%s.qry' % (GCorpus, GCorpus[:2],GlobalDf)
        
    elif (inFile == fFirstStage):
        # firstStage-WA-50-BM25.res
        qry = '300K' if GBias else '50'
        fName = rIndexFolder + 'firstStage/%s/firstStage-%s-%s-%s.res' % (GCorpus,GCorpus[:2],qry,GModel)
    elif (inFile.endswith('sh')):
        fName = mainFolder + 'bash/' + inFile
    # elif (inFile.__contains__('Second')):
    #     fName = '~/anserini/revertedIndex/' + inFile
    else:
        fName = rIndexFolder + inFile
    return fName

def fillMainDictionaries ():
    global GQryDict , GBaseDict
    GQryDict = getTermsDictionary(fQryList, ' ')
    GBaseDict = getTermsDictionary(fBaseQryList, '\t')

def getTermsDictionary(fType,sep):
    path = getFile(fType)
    f = open(path,'r',encoding='utf-8')
    headerExist = fType == fBaseQryList
    if headerExist :
        f.readline()
    termDict = {}
    for line in f:
        parts = line.replace('\n','').split(sep,maxsplit=1)
        termDict[parts[0]] = parts[1]
    return termDict

def evaluateResults(resFile,gainFile):
    # Use trec method in Eval Class to evaluate The Final Results File
    global  GBias
    if GBias:
        result = []
        for b in [0,0.5]:
            c = 100
            temp =  rc.calculate(resFile,b,c,GCorpus[0], '')
            result += [str(x) for x in temp]
    else:
        trecResults =  trec.getTrecData(resFile,gainFile) # map , bpref , P.10 , ndcg'
        cwlResults = cwl.getMetricsValues(resFile,gainFile) # [Map,NDCG, P10,R4, R6, R8]
        result = trecResults + cwlResults
        # result = trecResults
    return result

def processThirdRun (resFile):
    runBash(resFile,'','expandedTerms') # Retrieve Results From ExpandedQuery File
    # print('Third Stage : Final Run with Expanded terms is Done Successfully')

def getTermList (qry, fbTerms, termListDict):
    # Extract (given fbTerms count) terms separated by space from input term List Dictionary
    # By the following steps :
    # 1- if given OriginalQryWeight > 0 add OriginalQryWeight to matching words between given
    # qry and termListDict
    # 2- If TermList is changed - re-sort it by new scores
    # 3- Extract terms from termList Dictionary , concatenate them in termList  and output termList

    global GScoreBy
    changed = False
    qry = qry.split()
    # if (GScoreBy == 'max'):
    #     denominator = list(termListDict.values())[0] # Max
    # else:
    #     denominator = sum(termListDict.values()) # Sum

    for word in qry:
        # score = termListDict[term]
        if (word in termListDict):
            # To prepart to sort it with other values Multiply the weight by denominator
            # add 1 if term exist in query
            termListDict[word] += 1  # originalQryWeight * denominator
            changed = True

    termList = ""
    i = 0
    if (changed):
        termListDict = sorted(termListDict.items(), key=lambda x: x[1], reverse=True)
    else:
        termListDict = termListDict.items()

    for key,val in termListDict:
        termList += '%s^%f ' % (key, val)
        # termList += word[0] + ' '
        i += 1
        if (i == fbTerms):
            break
    return termList

def processSecondRun(resFile, outFile, beta, fbTerms):
    # 2- Implement revert query and generate Expanded Terms Query File
    # Given ( result file from Revert Query path - ExpandedTerms outFile path
    # bashFile path ' Used to run Lucene Retrieval from Reverted Index - fbTerms )
    global GQryDict, GBaseDict

    runBash(resFile,'r','revertQry')
    resFile = getFile(resFile)
    f = open(resFile,'r',encoding='utf-8')
    outf = open(outFile,'w',encoding='utf-8')
    outLine = 'qryID\tqry\n'
    outf.write(outLine)
    termListDict = {}
    prevQryID = -1
    beta = 1-beta
    for line in f:
        parts = line.split()
        qryid = parts[0]
        termid = parts[2]
        score = float(parts[4])
        if (prevQryID == -1):
            prevQryID = qryid
            max = score
            # maxScore = score
        if (prevQryID == qryid):
            term = GBaseDict[termid]
            score = beta * score / max
            termListDict[term] = score
        else:
            qry = GQryDict[prevQryID].lower()
            termList = getTermList(qry, fbTerms, termListDict)
            # outLine = prevQryID + '\t' + qry + ' ' + termList + '\n'
            outLine = '%s\t%s\n' % (prevQryID , termList)

            outf.write(outLine)
            term = GBaseDict[termid]
            max = score
            # termListDict = {term : beta * score / max}
            termListDict = {term: beta }
            prevQryID = qryid

    qry = GQryDict[prevQryID].lower()
    termList = getTermList(qry, fbTerms, termListDict)
    outLine = '%s\t%s\n' % (qryid , termList)
    # outLine = prevQryID + '\t' + termList + '\n'

    outf.write(outLine)
    f.close()
    outf.close()
    xml.generateXMLTopics(outFile,outFile.replace('Terms','TermsXML'))

def processFirstRun (resFile,outFile, fbDocs):
    # Extract Document ids from Initial Res File (Standard queries) and generate base Query File
    sep = '\t'
    resF = open(resFile,'r')
    baseqryF = open(outFile,'w')
    outLine = 'qryID%sqry\n' % sep
    baseqryF.write(outLine)
    prevQry = '0'
    docidList = ""
    for line in resF:
        parts = line.split()
        qryID = parts[0]
        docid = parts[2].replace('-','')
        rank = int(parts[3])
        if (prevQry == '0'):
            prevQry = qryID
        if (prevQry == qryID and rank <= fbDocs ):
            docidList += docid + ' '
        elif(prevQry != qryID):
            outLine = '%s%s%s\n' % (prevQry, sep, docidList)
            baseqryF.write(outLine)
            docidList = docid + ' '
            prevQry = qryID
        # elif (int(qryID) > 50):
        #     break
    outLine = '%s%s%s\n' % (prevQry, sep, docidList)
    baseqryF.write(outLine)
    baseqryF.close()
    resF.close()
    xml.generateXMLTopics(outFile,outFile.replace('Qry','QryXML'))

def runExperiment(fbDocs, fbTerms, beta):
    global GBias , GCorpus , GModel , GModelCoefficient
    t1 = gen.printCurrentTime('Start')
    resFile = getFile(fFirstStage)
    outFile = getFile('revertQry.qry')
    processFirstRun(resFile , outFile , fbDocs)
    t2 = gen.printCurrentTime('End First Stage')
    print('Elapsed ' , t2 - t1)
    resFile = 'SecondStage.res'
    outFile = getFile('expandedTerms.qry')
    processSecondRun(resFile, outFile, beta, fbTerms)
    t3 = gen.printCurrentTime('End Second Stage')
    print('Elapsed ' , t3 - t2)
    t2 = None
    resFile = 'FinalRun.res'
    processThirdRun(resFile)
    t4 = gen.printCurrentTime('End Third Stage')
    print('Elapsed ' , t4 - t3)
    t3 = None
    if GBias:
        resFile = getFile(resFile)
        # BiasRes/REV-WA-PL2-c1-beta0.6-docs10-terms05-b0.res
        coefficient =  gen.getModelCoefficient(GModel)
        destFile = 'BiasRes/REV-%s-%s-%s%s-beta%0.2f-docs%02d-terms%02d.res' % \
                   (GCorpus[:2], GModel, coefficient, GModelCoefficient, beta, fbDocs, fbTerms)

        destFile = getFile(destFile)
        gen.copyFile(resFile,destFile)
    else:
        resFile = '~/anserini/revertedIndex/' + resFile
    gainFile = gen.getGainFile(GCorpus[0])
    eval = evaluateResults(resFile,gainFile)
    t5 = gen.printCurrentTime('End Experiment')
    print('Elapsed ' , t5 - t4)
    exTime = str(t5 - t1)
    t5 = None
    t1 = None
    eval.append(exTime)
    print('Full Experiment Time ',exTime)
    outLine = getOutputLine(fbDocs, fbTerms, beta, eval)
    return outLine

def initialize ():
    global GBias, GScoreBy , GoutFile , GCorpus , GModel , GModelCoefficient , GlobalDf
    # max sum
    GScoreBy = 'max'
    GBias = True
    GoutFile = False
    GCorpus = gen.getCorpus('c')
    # BM25 - PL2
    GModel = 'PL2'
    GModelCoefficient = '0.75' if GModel == 'BM25' else '1'
    GlobalDf = '{:02d}'.format(10)

    fillMainDictionaries()
    docrng = range(10,35,5)
    # docrng = [10]
    termrng = range(30,55,5)
    # termrng = docrng
    # termrng = [30]
    beta = [0.25]
    # [0 , 0.05 ,0.1, 0.15, 0.2 , 0.25 ,0.3 ,0.35,0.4,0.6]
    return [beta,docrng,termrng]

def main():
    global GBias , GoutFile
    # terms = 5
    # docs = 10
    # pth = r'/mnt/c/Users/kkb19103/Desktop/My Files 07-08-2019/My Work/InformationRetrieval/python/src\\DocMaps\\WAPODocMap.txt'

    [allBeta,docrng,termrng] = initialize()
    lines = []
    # rng = range(5,55,5)
    for beta in allBeta:
        for docs in docrng:
            for terms in termrng:
                if (docs == 10 and terms == 30):
                    continue
                log = 'Start beta = %.2f , fbDocs = %s , fbTerms = %s ' % (beta, docs, terms)
                print(log)
                line = runExperiment(docs,terms,beta) + '\n'
                print('--------------------------\n',line,'\n------------------------\n')
                print(log.replace('Start','End',1))
                lines.append(line)

    if (GoutFile):
        path = 'Ret' if GBias else 'Per'
        path = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\3rd Experiment - Reverted Index\CSV\Ex3%s.csv' % path
        f = open(path, 'a', encoding='utf-8')
        # Print Header
        # Per Header Line
        for line in lines:

            # f.write(line)
            print(line)
        f.close()
    else:
        path = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\3rd Experiment - Reverted Index\CSV\test.csv'
        path = gen.getLinuxPath(path)
        f = open(path,'w')
        for line in lines:
            print(line[:len(line)-1])
            f.write(line)
        f.close()

if __name__ == '__main__':
    main()