import python.src.pythonFiles.dedicatedProcess.XMLTopicsCreator as xml
import classes.general as gen
import os

def removeDashes (path):
    files = os.listdir(path)
    for file in files:
        file = path + '/' + file
        f = open(file, 'r')
        lines = f.readlines()
        f.close()
        lines = ''.join(lines)
        lines = lines.replace('-','')
        f = open(file,'w')
        f.write(lines)
        f.close()
        print('Dashes Removed From File :', file)

def extractBaseQueries (inFile , outFile , df):
    # Extract Base Queries given specific df limit
    f = open(inFile,'r',encoding='utf-8')
    f2 = open(outFile,'w',encoding='utf-8')
    outLine = 'qryID\tqry\n'
    f2.write(outLine)
    seq = 1
    for line in f:
        parts = line.split('\t')
        numDf = int(parts[1])
        if (numDf > df):
            outLine = '%d\t%s\n' % (seq , parts[0])
            f2.write(outLine)
            seq += 1
    f.close()
    f2.close()

def countIDs(path):
    # Count ids in specific input file
    f = open(path,'r')
    ctr = 0
    for line in f:
        if line.__contains__('"id"'):
            ctr += 1
            print ("id",ctr)
    f.close()

def removeCharacter(path):
    # Remove specific character from all lines in input File
    f = open(path,'r')
    lines = []
    ctr = 0
    found = 0
    targetChar = chr(28)
    for line in f :
        ctr += 1
        if line.__contains__(targetChar):
            found += 1
            newLine = line.replace(targetChar,'')
        else:
            newLine = line
        lines.append(newLine)
        print('append',ctr)
    f.close()
    path = '/mnt/c/Users/kkb19103/Desktop/test.jsonl'
    f = open(path,'w')
    ctr = 0
    for line in lines:
        ctr+=1
        f.write(line)
        print('write', ctr)
    print ('Total Found ',found)
    f.close()
    lines = None

def findMissingQueries(resFile):
    # Find Missing sequence numbers in queryIDs of Res File
    f = open(resFile,'r')
    i = 1
    ctr = 0
    f.readline()
    for line in f:
        # qryID = line.split(' ',1)[0]
        qryID = line.split(',')[1]
        qryID = int(qryID)
        while(qryID > i):
            i+=1
            if (qryID > i):
                print(i,'is Missing')
                ctr += 1
    print('Total Missing',ctr)
    f.close()

def findDocument(resFile,indocid):
    # given WAPO docID with removed dashes - Find it in the given res file
    ctr = 0
    with open(resFile,'r') as f:
        for line in f:
            parts = line.split()
            docid = parts[2].replace('-','')
            if (indocid == docid):
                print(line.replace('\n',''))
                ctr += 1
    print('Found Times : ' , ctr)
    return ctr

def extractTopicListFromXML (xmlQryFile):
    numDef =  '<num> Number:'
    titleDef = '<title> '
    f = open(xmlQryFile,'r')
    outfName = xmlQryFile.replace('XML.qry','.qry')
    outf = open(outfName,'w')
    for line in f:
        if (line.startswith(numDef)):
            num = line.replace(numDef,'').strip()
        elif (line.startswith(titleDef)):
            title = line.replace(titleDef,'').strip()
            outLine = '%s %s\n' % (num,title)
            outf.write(outLine)
    f.close()
    outf.close()

def main():
    mainFolder = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\LUCENE\anserini\revertedIndex\prior\Core17'
    # path = mainFolder + '\CO-Df.sts'
    # df = 10
    # outPath = mainFolder +  '\DFBigger%s\CO-BaseQueries-Df-%s.qry' % (df,df)
    # extractBaseQueries(path,outPath,int(df))
    # xml.generateXMLTopics(outPath,outPath.replace('-' + str(df),'-%dXML' % df))
    # path = r'C:\Users\kkb19103\Desktop\new\data\data\TREC_Washington_Post_collection.v2_Modifiedcollection.jsonl'
    # resFile = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\LUCENE\anserini\revertedIndex\prior\CORE17\DFBigger10\CO-BaseScore.res'
    # resFile = gen.getLinuxPath(resFile)
    # countIDs(path)
    # removeCharacter(path)
    mainFolder = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\2nd Experiment - RM3 VS AX\DocLength Analysis\DocLength Analysis\Anserini-DocLength'
    resFile = mainFolder + r'\CO-Doclengths - Copy.csv'
    findMissingQueries(resFile)
    # removeDashes(path)

    # file = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\LUCENE\anserini\Queries\CORE17\50XML.qry'
    # extractTopicListFromXML(file)
    print('Done')

if __name__ == '__main__':
    main()