import os
import pandas as pd
import pythonFiles.paper2.AdditionalAnalysis.generateRetFile as genret

def getTwoNumbers (i):
    return '{:02d}' % int(i)

def getFileName(line):
    # WAPO,AX,0.4,BM25,25,25,0,0.75,0.471616151,13750,29207300
    # AQ-BM25-UI-300K-C100-AX-fbdocs05-fbterms05-b0.75.res
    parts = line.split(',')
    corpus = parts[0][:2]
    exp = parts[1]
    beta = parts[2]
    terms = '{:02d}'.format(int(parts[4]))
    docs = '{:02d}'.format(int(parts[5]))
    fName = '%s-BM25-UI-300K-C100-%s-fbdocs%s-fbterms%s-b0.75.res' % (corpus,exp,docs,terms)
    outName = '%s' * 5
    outName = '-'.join(outName) % (corpus,exp,beta,docs,terms) + '.csv'
    return [fName , outName]

def addRet (file):
    [corpus,exp,beta,docs,terms] = file.split('-')
    terms = terms.replace('.csv','')
    # docs = getTwoNumbers(docs)
    # terms = getTwoNumbers(terms)
    path = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\2nd Experiment - RM3 VS AX\DocLength Analysis\DocLength Analysis\RetFiles'
    df = genret.getRetrievabilityResults(corpus,exp,0,docs,terms)
    df2 = genret.getRetrievabilityResults(corpus,exp,0.5,docs,terms)
    df = df.merge(df2,'inner','docid')
    df.to_csv(path + '\\' + file,index=None)
    df = None
    df2 = None
    print('File Done:', file)

def main():
    # df1 = pd.DataFrame({
    #     "Name": ["Alice", "Bob", "Mallory"],
    #     "City": ["Seattle", "Seattle", "Portland"]})
    #
    # df2 = pd.DataFrame({
    #     "Name": ["Hani", "Hussain", "Mallory"],
    #     "City": ["Seattle", "Seattle", "Portland"]})
    # df3 = pd.concat([df1,df2],ignore_index=False)
    # print(df3)
    # path = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\2nd Experiment - RM3 VS AX\DocLength Analysis\DocLength Analysis\RetFiles'
    # enc = 'utf-8'
    # for file in os.listdir(path):
    #     file = path + '\\' + file
    #     df = pd.read_csv(file,encoding=enc)
    #     df = df['docid r0 r0.5'.split()]
    #     df.to_csv(file,encoding=enc,index=None)
    #     print ('Finished ' , file)

    csvFile = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\2nd Experiment - RM3 VS AX\CSV\Ex2Ret.csv'
    f = open(csvFile)
    f.readline()
    folder = r'D:\Backup 29-04-2021\2nd Experiment - RM3\AllRes\Bias Measurement'
    i = 0
    for line in f:
        i += 1
        if (i % 2 == 0) or i <= 6 :
            continue
        [inFile , outFile] = getFileName(line)
        file = folder + '\\' + inFile
        if os.path.isfile(file):
            addRet(outFile)

if __name__ == '__main__':
    main()