import pandas as pd
from pathlib import Path as pth
import python.src.classes.general as gen

def getMapFile(corpus):
    mapFolder = r'C:\Users\kkb19103\Desktop\DocMaps'
    # mapFolder = str(pth(__file__).parent.parent) + '\DocMaps'
    # corpus = resFile.rsplit('\\', 1)[1][0]
    corpus = gen.getCorpus(corpus[0])
    # mapFile = '%s\%sDocMap.txt' % (mapFolder, corpus)
    # mapFile = '~/python/DocMaps/%sDocMap.txt' % corpus
    mapFile = mapFolder + '\%sDocMap.txt' % corpus
    # mapFile = gen.getLinuxPath(mapFile)
    return mapFile


def calculate(resFile, b, c, corpus, outFile):
    # [G, ctr_zero, rSum]
    # result = DataframeCalculation.calculate(resFile, b, c, corpus, outFile)
    result = inlineCalculation.calculate(resFile, b, c, corpus, outFile)
    return result

def getRetDf (resFile,b,c,corpus):
    df = inlineCalculation.getRetDf (resFile,b,c,corpus)
    return df

class inlineCalculation () :
    def getRetDf (resFile,b,c,corpus):
        docMap = inlineCalculation.getDocMap(corpus)
        resF = open(resFile, 'r', encoding='utf-8')
        for line in resF:
            # print(line)
            parts = line.split()
            # qryid = parts[0]
            docid = parts[2]
            rank = int(parts[3])
            r = rank ** -b
            docMap[docid] += r
        resF.close()
        items = docMap.items()
        df = pd.DataFrame(items, columns='docid r'.split())
        return df

    def getDocMap (corpus):
        mapFile = getMapFile(corpus)
        f = open(mapFile,'r')
        docMap = {}
        for line in f:
            docid = line.replace('\n','')
            docMap[docid] = 0
        return docMap

    def calculateG(docMap):
        # Calculate G - Count of zero r values - rSum
        docMap = sorted(docMap.items(), key=lambda x: x[1])
        rSum = 0
        zeroCtr = 0
        numerator = 0
        N = len(docMap) + 1
        i = 1
        for docid , r in docMap :
            if (r == 0):
                zeroCtr += 1
            else:
                rSum += r
                numerator += (2 * i - N) * r
            i += 1
        G = numerator / ((N-1) * rSum)
        return [G , zeroCtr , rSum]


    def calculate(resFile, b, c, corpus, outFile):
        docMap = inlineCalculation.getDocMap(corpus)
        resF = open(resFile,'r',encoding='utf-8')
        for line in resF:
            # print(line)
            parts = line.split()
            # qryid = parts[0]
            docid = parts[2]
            rank = int(parts[3])
            r = rank ** -b
            docMap[docid] += r
        resF.close()
        result = inlineCalculation.calculateG(docMap)
        if (outFile != ''):
            items = docMap.items()
            df = pd.DataFrame(items,columns='docid r'.split())
            df.to_csv(outFile,index=None)
        return result

class DataframeCalculation ():
    def calculate_res_map(res_file, b, c):
        # Given Res File - C - b : Calculate Retrievability MAP
        # Res Headers
        names = ['qryid', 'dum', 'docid', 'rank', 'score', 'tag']
        # Read Res File
        df = pd.read_csv(res_file, delimiter=' ', names=names)
        # Drop Unnecessary Columns
        df.drop(['dum', 'score', 'tag'], axis=1, inplace=True)
        # Set Max Results in MAP
        df = df.groupby('qryid').head(c)
        # Calculate R and add R Column in Map
        if b == 0:
            df['r'] = 1
        else:
            df['r'] = df['rank'] ** -b
        # Group Resultant Map By Doc ID
        # df = df.groupby('docid').agg({'r': [np.sum,'count']})
        df = df.groupby('docid').agg({'r': ['sum', 'count']})
        df.columns = df.columns.droplevel(0)
        df.rename(columns={'sum':'r','count':'rcount'},inplace=True)
        # Calculate r_sum
        # r_sum = df['r'].sum()
        return df

    def initDocMap(mapFile):
        # Given mapFile path (Simply list of docIds) get DocMap by adding r = 0 to all documents
        df = pd.read_csv(mapFile, names=['docid'])
        # df['r'] = 0
        return df

    def calculateG(df):
        # Given Merged Map and rSum  calculate G
        num_head = 'numerator'
        # Sort and reindex map based on r values
        df = df.sort_values('r')
        df = df.reset_index(drop=True)
        # Add 1 to N to avoid doing that all over the rows in the MAP
        N = len(df) + 1
        # Calculating Numerator Column
        df[num_head] = (2 * (df.index + 1) - N) * df['r']
        # Set Back N Value
        N -= 1
        # Total Numerator
        sumNumerator = df[num_head].sum()
        # Calculate G
        rSum = df['r'].sum()
        G = sumNumerator / (N * rSum)
        return [G,rSum]

    def mergeMaps(docMap, resMap):
        # Given DocMap and ResMap - Merge both based on doc id
        # df = pd.merge(docMap, resMap, how='left', on='docid', suffixes=["_x", ""])
        df = pd.merge(docMap, resMap, how='left', on='docid')
        # Drop Additional DocMap r Column after Merge
        # df.drop('r_x', axis=1, inplace=True)
        # Replace Nan values in Res R Column with Zero
        df.fillna(0, axis=1, inplace=True)
        return df

    def calculate(resFile , b , c , corpus , outFile):
        # resFile = r'C:\Users\kkb19103\Desktop\WA-BM25-BI-300K-C100-b0.4.res'
        mapFile = getMapFile(corpus)
        # Initialize DocMap
        docDf = DataframeCalculation.initDocMap(mapFile)
        # Calculate R MAP
        resDf = DataframeCalculation.calculate_res_map(resFile, float(b), c)
        # Merge Both Maps
        mergeDf = DataframeCalculation.mergeMaps(docDf, resDf)
        # Release Memory
        resDf = None
        docDf = None
        # Calculate G
        [G,rSum] = DataframeCalculation.calculateG(mergeDf)
        # output MAP
        if outFile != '':
            mergeDf.to_csv(outFile, sep='\t', header=False, index=False)
        criteria = mergeDf['r'] == 0
        ctr_zero = len(mergeDf[criteria])

        # mergeDf['r'] = mergeDf['r'] / mergeDf['rcount']
        # [NG,r] = calculateG(mergeDf)
        return [G , ctr_zero , rSum]
