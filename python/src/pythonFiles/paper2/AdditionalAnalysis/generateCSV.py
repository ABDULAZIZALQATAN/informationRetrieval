import pandas as pd
import classes.general as gen

def getDocLength (corpus):
    folder = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\2nd Experiment - RM3 VS AX\DocLength Analysis\DocLength Analysis\Anserini-DocLength'
    file = folder + r'\%s-Doclengths.csv' % corpus
    sep = ','
    df = pd.read_csv(file,sep=sep)
# external_docid
#     fldDocid = 'internal_docid' if corpus == 'CO' else 'external_docid'
    fldDocid = 'external_docid'
    extract = [fldDocid , 'doc_length']
    df = df[extract]
    df.rename(columns={fldDocid:'docid','doc_length':'length'},inplace=True)
    return df

def getRelevantDf (corpus):
    folder = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\Resources'
    corpus = gen.getCorpus(corpus[0])
    file = folder + r'\%s\%s.qrel' % (corpus,corpus)
    df = pd.read_csv(file,sep=' ',names='d1 d2 docid rel'.split())
    df = df.groupby('docid',as_index=False).sum('rel')
    df = df['docid rel'.split()]
    return df

def mergeDf (df1 , df2):
    df = df1.merge(df2, 'left', 'docid')
    return df

def getMainFile (corpus):
    corpus = gen.getCorpus(corpus[0])
    file = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\2nd Experiment - RM3 VS AX\Faieness Measurement\%sFields.csv' % corpus
    return file

def process(corpus):
    key = 'docid'
    file = getMainFile(corpus)
    df = pd.read_csv(file, low_memory=False)
    dfTemp = getRelevantDf(corpus)
    df = df.merge(dfTemp, 'left', key)
    df['rel'].fillna(0, inplace=True)
    dfTemp = getDocLength(corpus)
    df = df.merge(dfTemp, 'left', key)
    df['length'].fillna(0, inplace=True)
    df.to_csv(file, index=None)
    print('Done')

def main():
    for c in 'co wa'.split():
        process(c)

if __name__ == '__main__':
    main()