import classes.trec as trecCls
import classes.CWL as cwl
import classes.clsRetrievabilityCalculator as ret
import pandas as pd
import classes.general as gen


# *****************  AQUAINT Statistics ****************************************************
def extractAquaintPublishers(path):
    # Read AQUAINT res file then extract publishers (NYT-XIE - APW) and year from doc IDs
    df = pd.read_csv(path, sep=' ',header=None)
    df = df.iloc[:, 2]
    collection = df.str.slice(stop=3)
    year = df.str.slice(start=3, stop=7)
    df = pd.concat([collection, year], axis=1)
    df.columns = ['collection', 'year']
    return df

def getAquaintStatistics(path):
    # Given AQUAINT res File Extract Publishers (NYT-XIE - APW) and pulblish years from DocIDs
    # group data by them to get the count and average
    path = r'C:\Users\kkb19103\Desktop\TempFiles\AQ-BM25-UI-300K-C100-AX-fbdocs30-fbterms30-b0.75.res'
    df = extractAquaintPublishers(path)
    df = df.groupby(by=['collection', 'year']).size().reset_index()
    # df.rename(columns={0,'count'},inplace=True)
    df.columns = ['collection', 'year', 'count']
    aSum = df['count'].sum()
    df['avg'] = df['count'] / aSum
    print(df)
# **************************************************************************************

# *****************  Res Evaluation ****************************************************
def cwl(resFile, gainFile):
    # Get CWL Results given resfile and gainFile

    # result = cwlCls.cwlEval.getMetricsValues(resFile, gainFile)
    result = cwl.executeBash(resFile, gainFile)
    print (result)

def trec(resFile, gainFile):
    # Get Trec Results given resfile and gainFile
    # map , bpref , P.10 , ndcg'
    result = trecCls.getTrecData(resFile, gainFile)

    # result = trec.executeBash(resFile, gainFile)
    print (result)

def retrievability(resFile):
    # get Retrievability Results given resFile
    b=0.5
    c=100
    for b in [0,0.5]:
        result = ret.calculate(resFile,b,c,'WAPO','')
        result = str(result).replace(',','\t')
        print(b,result)
# **************************************************************************************

def main():
    resFile = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\LUCENE\anserini\revertedIndex\BiasRes\REV-WA-PL2-c1-beta0.25-docs25-terms50.res'
    resFile = gen.getLinuxPath(resFile)
    gainFile = gen.getGainFile('w')
    # newline = '\n-------------------------\n'
    # cwl(resFile,gainFile)
    # retrievability(resFile)
    trec(resFile, gainFile)

if __name__ == '__main__':
    main()