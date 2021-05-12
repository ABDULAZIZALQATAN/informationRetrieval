import numpy as np
import pythonFiles.paper2.AdditionalAnalysis.csvPlotterAdditionalAnalysis as analysis
import pandas as pd
import matplotlib.pyplot as plt
import pythonFiles.plotters.csvPlotterGen as pltgen
import classes.general as gen


inDocs = '05'

def formatKickers(kickers):
  i = 0
  for kicker in kickers:
    kicker = kicker.split()
    count = len(kicker)
    if (count == 1):
      kicker = kicker[0]
    elif (count == 2):
      kicker = '%s\n%s' % (kicker[0], kicker[1])
    elif (count == 3):
      kicker = '%s %s\n%s' % (kicker[0], kicker[1], kicker[2])
    else:
      kicker = '%s %s\n%s %s' % (kicker[0], kicker[1], kicker[2], kicker[3])
    kickers[i] = kicker
    i += 1
  return kickers

def getFile (corpus,exp):
  exp = exp[:2].upper()
  path = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\2nd Experiment - RM3 VS AX\DocLength Analysis\DocLength Analysis'
  docs = '0' if exp == 'BA' else inDocs
  file = r'%s\%s-%s-%s-%s.csv' % (path,corpus,exp,docs,docs)
  return file

def readFile (corpus,exp):
  fName = getFile(corpus,exp)
  df = pd.read_csv(fName)
  return df

def compute_percent(v):
  total_v = np.sum(v)
  percent_v = np.divide(v * 100, total_v)

  return percent_v

def compute_fairness_score(a, b):
  c = np.subtract(a,b)  # substract
  c = np.power(c,2) # square
  c = np.sum(c) # sum
  score = np.power(c, 0.5) #square root
  return score

def add_length_bucket(df, num_buckets=100):
  df.sort_values(['length'], inplace=True)
  # 3- work out how many docs per bucket = total_num_docs / num_buckets
  total_num_docs = len(df)
  bucket_size = int(np.ceil(total_num_docs / num_buckets))
  # 4- build a list (bucket_list) that assigns the first n docs to bucket 1, the next n to bucket 2, etc.
  rng = list(range(1,num_buckets + 1)) * bucket_size
  # rng = list(range(1,bucket_size + 1)) * num_buckets

  # 5- add the list to dataframe as a col --> sdf['buckets'] = bucket_list
  df['bucket'] = sorted(rng[:total_num_docs])
  # df['bucket'] = sorted(rng)

  return df

def add_year_src(df):
  # for aquaint
  df['news'] = df['docid'].str[:3]
  df['year'] = df['docid'].str[3:7]
  df['news-year'] = df['news'] + '\n' + df['year']

  return df


def processSupervisor(df):
  rField = 'r0'
  kickers = df.groupby('kicker').agg({rField: ['mean', 'sum' , 'count']})
  # Compute the proportion of exposure to each of the kickers
  percent_rd = compute_percent(kickers[rField]['sum'])

  # Lets assume that for each kicker we should be fair to each group based on group size
  # percent_size = compute_percent(kickers['length']['count'])

  percent_size = compute_percent(kickers[rField]['count'])
  # percent_size = compute_percent(kickers['length']['count'])

  # Lets assume that all kickers we have should be equally treated (regardless of size)
  percent_groups = compute_percent([1] * len(percent_size))
  print(len(percent_size), percent_groups)

  # Lets assume that the proportional of relevant items in each kicker is how we should allocate resources...
  # use the QRELS and count how many rels are associated with each kicker..

  size_v_rd = compute_fairness_score(percent_rd, percent_size)
  groups_v_rd = compute_fairness_score(percent_rd, percent_groups)
  print(size_v_rd)
  print(groups_v_rd)


def plotFigure (exp,x,y):
  color = exp[0].lower()
  label = exp

  if (exp == 'AX'):
    color = 'g'
    marker = '^'
  elif (exp == 'BA'):
    label = 'Baseline'
    marker = 'o'
  else:
    marker = 'x'
  plt.scatter(x, y,marker=marker,color=color,label=label)

def getFigureProperties (type,corpus):

  corpus = gen.getCorpus(corpus[0])

  temp = '%s - BM25 - b = 0.75\nfbDocs=%s - fbTerms=%s' % (corpus,inDocs,inDocs)
  if type == 'bucket':
    title = "%s\nDocument Bucket vs Average (r)" % (temp)
    xLabel = 'Document Bucket'
  elif (type == 'news-year'):
    title = "%s\nNews-Year vs Average (r)" % (temp)
    xLabel = 'News-Year'
  else:
    title = "%s\nKicker vs Average (r)" % (temp)
    xLabel = 'Kicker'
  yLabel = 'Percentage Average (r) %'
  return [title , xLabel,yLabel]



def showFigure(title,xLabel,yLabel):
  legend= 'Query Expansion'
  plt.legend(title=legend, ncol=2)
  # Set Title
  [fFamily, fSize, fWeight] = pltgen.getFont()
  plt.title(title, size=fSize, family=fFamily, weight=fWeight)
  # Set Axis Labels
  plt.xlabel(xLabel, size=fSize, family=fFamily, weight=fWeight)
  plt.ylabel(yLabel, size=fSize, family=fFamily, weight=fWeight)

  if(title.__contains__('Bucket')):
    plt.xticks(range(0,110,10))
    ticks = pltgen.getTicks('0 2 0.2')
    plt.yticks(ticks)
  plt.show()

def plotBuckets(corpus,exp):
  # Avg(R) vs BucketSize
  groupField = 'bucket'
  rField = 'r0'
  corpus = corpus.upper()
  exp = exp.upper()
  df = readFile(corpus,exp)
  df = add_length_bucket(df)
  df = df.groupby(by=groupField,as_index=False).agg({rField:'mean'})
  x = df[groupField]
  y = compute_percent(df[rField])
  plotFigure(exp,x,y)


def plotAQUAINT (exp):
  # AQUAINT Groups
  groupField = 'news-year'
  corpus = 'AQ'
  rField = 'r0'
  exp = exp.upper()
  df = readFile(corpus, exp)
  df= add_year_src(df)
  df = df.groupby(by=groupField,as_index=False).agg({rField:'mean'})
  x= df[groupField]
  y = compute_percent(df[rField])
  # bucket_vs_rd = compute_fairness_score(percent_bucket,percent_avgr)
  plotFigure(exp,x,y)

def plotKickers(exp,dest):
  # WAPO Groups
  groupField = 'kicker'
  corpus = 'WA'
  rField = 'r0'
  exp = exp.upper()
  df = readFile(corpus, exp)
  df = df.groupby(by=groupField, as_index=False).agg({rField: 'mean'})
  df.sort_values(rField,inplace=True)
  y = compute_percent(df[rField])
  x = df[groupField]
  if (dest > 0):
    y = y.head(dest)
    x = x.head(dest)
  else:
    y = y.tail(abs(dest))
    x = x.tail(abs(dest))
  x = formatKickers(list(x))
  plotFigure(exp, x, y)


def plotManyBuckets():
  global inDocs
  groupField = 'bucket'
  inDocs = '05'
  for corpus in 'aq co wa'.split():
    for exp in 'ax ba rm3'.split():
        plotBuckets(corpus,exp)

        print('Finished ', corpus, exp)
    [title, xLabel, yLabel] = getFigureProperties(groupField, corpus)
    showFigure(title, xLabel, yLabel)


def plotManyAQUAINTs():
  global inDocs

  groupField = 'news-year'
  corpus = 'AQ'
  inDocs = '05'
  for exp in 'ax ba rm3'.split():
    plotAQUAINT(exp)
    [title, xLabel, yLabel] = getFigureProperties(groupField, corpus )
    print('Finished ', corpus, exp)
  showFigure(title, xLabel, yLabel)


def plotManyKickers ():
  global inDocs

  groupField = 'kicker'
  corpus = 'WA'
  inDocs = '05'
  dest = -6
  for exp in 'ax ba rm3'.split():
    plotKickers(exp,dest)
    [title, xLabel, yLabel] = getFigureProperties(groupField, corpus )
    print('Finished ', corpus, exp)
    temp = 'Top' if dest < 0 else 'Least'
    switcher = {
      'a':'Axiom',
      'b':'Baseline',
      'r':'RM3'
    }
    exp = switcher.get(exp[0].lower(),' ')
    title = title.replace('\n', ' - %s\n%s %d Values\n' % (exp,temp,abs(dest)))
    showFigure(title, xLabel, yLabel)

def main():
  plotManyBuckets()

if __name__ == '__main__':
    main()