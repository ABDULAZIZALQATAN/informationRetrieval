import classes.clsRetrievabilityCalculator as ret
import pandas as pd
import classes.general as gen

def getRelevantDf (corpus):
    folder = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\Resources'
    corpus = gen.getCorpus(corpus[0])
    file = folder + r'\%s\%s.qrel' % (corpus,corpus)
    df = pd.read_csv(file,sep=' ',names='d1 d2 docid d3'.split())
    df = df['docid']
    return df


def getDocLength (corpus):
    folder = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\2nd Experiment - RM3 VS AX\DocLength Analysis\DocLength Analysis\Anserini-DocLength'
    file = folder + r'\%s-Doclengths.csv' % corpus
    sep = ','
    df = pd.read_csv(file,sep=sep)
# external_docid
#     fldDocid = 'internal_docid' if corpus == 'CO' else 'external_docid'
    fldDocid = 'external_docid'
    extract = [fldDocid , 'doc_length']
    if corpus == 'WA':
        extract.append('kicker')
    df = df[extract]
    df.rename(columns={fldDocid:'docid','doc_length':'length'},inplace=True)
    return df

def getRetrievabilityResults (corpus,exp ,b , docs , terms):
    # folder = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\2nd Experiment - RM3 VS AX\DocLength Analysis\DocLength Analysis\ResFiles'
    folder = r'D:\Backup 29-04-2021\2nd Experiment - RM3\AllRes\Bias Measurement'
    # AQ-BM25-UI-300K-C100-Baseline-b0.75.res
    if (exp == 'BA'):
        # AQ-BM25-UI-300K-C100-Baseline-b0.75
        resFile = '\%s-BM25-UI-300K-C100-Baseline-b0.75.res'
    # elif (exp == 'RM'):
    #     resFile = '\%s-BM25-UI-300K-C100-RM3-fbdocs%s-fbterms%s-b0.75.res'
    else:
        resFile = '\%s-BM25-UI-300K-C100-' + exp + '-fbdocs%s-fbterms%s-b0.75.res'
    resFile = resFile % (corpus,docs,terms)

    resFile = folder + resFile
    c = 100
    df = ret.getRetDf(resFile,b,c,corpus)
    df.rename(columns={'r':'r'+ str(b)},inplace=True)
    if (corpus == 'CO'):
        df['docid'] = df['docid'].astype(int)
    return df

def mergeDf (df1 , df2):
    df = None
    if (len(df1) == len(df2)):
        df = df1.merge(df2, 'inner', 'docid')
    return df

def process(corpus,exp):
    corpus = corpus[:2].upper()
    exp = exp.upper()
    docs = '05'
    # Add doc Length Field
    df = getDocLength(corpus)
    # Add r0 wirh retrievability values b = 0
    dfr = getRetrievabilityResults(corpus , exp , 0 ,docs)
    # df1 = df.head(10)
    # df2 = dfr.head(10)
    # df2['docid'] = df2['docid'].astype(int)
    df = mergeDf(df,dfr)
    # Add r0.5 wirh retrievability values b = 0.5
    dfr = getRetrievabilityResults(corpus, exp, 0.5 , docs)
    df = mergeDf(df, dfr)
    # Add rel field with relevance based on standard query
    dfr = getRelevantDf(corpus)
    df['rel'] = df['docid'].isin(dfr)
    # outfput the final version of the csv file
    folder = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\2nd Experiment - RM3 VS AX\DocLength Analysis\DocLength Analysis'
    outFile = r'\%s-BA-0-0.csv' % corpus if (exp == 'BA') else r'\%s-%s-%s-%s.csv' % (corpus, exp[:2],docs,docs)
    outFile = folder + outFile
    df.to_csv(outFile,index=None)

    print('Done',corpus,exp)
def main():
    for corpus in 'aq co wa'.split():
        for exp in 'ax rm3'.split():
            process(corpus,exp)
if __name__ == '__main__':
    main()