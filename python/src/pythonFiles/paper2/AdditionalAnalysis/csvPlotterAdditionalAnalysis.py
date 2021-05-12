import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import classes.general as gen

def getFileName (corpus,exp):
    mainFolder = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\2nd Experiment - RM3 VS AX\DocLength Analysis\DocLength Analysis'
    exp = exp[:2].upper()
    corpus = corpus[:2].upper()
    docs = 0 if (exp == 'BA') else 30
    path = mainFolder + '\%s-%s-%d-%d.csv' % (corpus, exp,docs,docs)
    return path

def readDf(corpus,exp):
    # Read input Df File Given Corpus and Expansion
    path = getFileName(corpus,exp)
    df = pd.read_csv(path)
    return df

def showFigure(title , type):
   # General plot properties
  if (type == 'dl'):
    [xLabel,yLabel] = [  'Bucket' , 'r']
    # plt.xticks(range(0,11000,1000) )
  elif (type == 'aq'):
    [xLabel,yLabel] = [  'Newswire-Year' , 'Average r']
  else:
      [xLabel, yLabel] = ['Kicker' , 'rAverage']
  [fSize, fWeight] = [17,500]
  plt.title(title,size=fSize,weight=fWeight)
  # Set Axis Labels
  plt.xlabel(xLabel,size=fSize,weight=fWeight)
  plt.ylabel(yLabel,size=fSize,weight=fWeight)
  plt.show()

def plotDocumentBucket (corpus, exp , num_buckets):
  # Plot
  # 1- read in file that contains (docid, len, etc..) to a dataframe df
  # temp = exp[:2].upper()
  # fName = '%s-%s' % (corpus[:2] ,temp)
  df = readDf(corpus,exp)
  # 2- sort dataframe by len --> sdf
  df.sort_values(['length'], inplace=True)
  # 3- work out how many docs per bucket = total_num_docs / num_buckets
  total_num_docs = len(df)
  bucket_size = int(np.ceil(total_num_docs / num_buckets))
  print(bucket_size)
  # 4- build a list (bucket_list) that assigns the first n docs to bucket 1, the next n to bucket 2, etc.
  rng = list(range(1,num_buckets + 1)) * bucket_size
  # 5- add the list to dataframe as a col --> sdf['buckets'] = bucket_list
  df['bucket'] = sorted(rng[:total_num_docs])
  # 6- sdf.groupby(by='bucket_list').mean()
  df = df.groupby('bucket').agg({'r':'mean'}).reset_index()
  # df.groupby('bucket').agg({'r':['mean', 'std','count']})
  plt.plot (df['bucket'],df['r'])
  showFigure('%s-%s\nDocument Length Buckets - Count = %d' % (corpus,exp, num_buckets) ,'dl')

def plotAquaintCategories(exp):
  # fName = 'AQ-' + exp[:2].upper()
  df = readDf('AQ',exp)
  df['news'] = df['docid'].str[:3]
  df['year'] = df['docid'].str[3:7]
  df = df.groupby(['news','year']).sum()
  # print('The rSum of Expansion %s \n' % exp, df)
  df['r'] =  df['r'] / df['r'].sum() * 100
  df.reset_index(inplace=True)
  df['x'] = df[['news', 'year']].agg('\n'.join, axis=1)
  df = df[['x','r','length']]
  print('The rAverage of Expansion %s \n' % exp, df)
  plt.plot(df['x'],df['r'])
  showFigure('AQUAINT Categories - ' + exp , 'aq')

def plotWAPOKickers(exp,limit):

  df = readDf('WA',exp)
  df = df.groupby('kicker',as_index=False).sum('r')
  df['r'] = df['r'] / df['r'].sum() * 100
  df.sort_values('r',ascending=False, inplace=True)
  dfTop = df.head(limit)
  dfBottom = df.tail(limit)
  print('Top Values : \n',dfTop)
  print('Bottom Values : \n', dfBottom)
  plt.plot(dfTop['kicker'],dfTop['r'])
  showFigure('WAPO Categories - Top %d Values' % limit ,'WA')
  plt.plot(dfTop['kicker'], dfBottom['r'])
  showFigure('WAPO Categories - Bottom %d Values' % limit, 'WA')

def addRelevance (corpus,exp):
    df = readDf(corpus,exp)
    qrel = gen.getGainFile(corpus)
    dfQrel = pd.read_csv(qrel,sep=' ',header=None,names=['qryid','dum1','docid','dum2'])
    df['rel'] = df["docid"].isin(dfQrel["docid"])
    # df.drop('rcount',axis=1,inplace=True)
    path = getFileName(corpus,exp)
    df.to_csv(path,index=False)

def main():
    for exp in 'ax rm ba'.split():
        addRelevance('aq',exp)
    # df = readDf('co','ax')
    # criteria = df['rel'] == 1
    # df = df[criteria]
    # print(df , len(df))


if __name__ == '__main__':
    main()