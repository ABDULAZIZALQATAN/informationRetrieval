'''
Sort Csv File By

'''

import pandas as pd
import  pythonFiles.plotters.csvPlotterGen as pltgen
import classes.general as gen

# Import PyDrive and associated libraries.
# This only needs to be done once per notebook.
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# from google.colab import auth
# from oauth2client.client import GoogleCredentials

# Import General
# drivePath = '/content/gdrive'
# modPath = '/My Drive/Colab Notebooks'
# from google.colab import drive
# drive.mount (drivePath )
# import sys
# sys.path.append(drivePath + modPath)
# import csvPlotterGeneral as gen

# *** Start Colab Form ***
# @title Best Performance
#@markdown Get The Best 5 Trec_Eval Values based on input criteria
Corpus = "Aquaint"  # @param ["Aquaint", "Core17", "WAPO" , "All"]
Model = "BM25"  # @param ["BM25", "LMD", "PL2"]
QryExpansion = "RM3"  # @param ["AX","RM3"]
best = "5"  # @param ["5", "6", "7" , "8"]

# *** End Colab Form ***

def grouping(df,by):
  df = df.groupby(by).count()[df.columns[0:1]]
  df.reset_index(level=0, inplace=True)
  df.rename(columns={df.columns[1]: 'count'}, inplace=True)
  df.sort_values('count',ascending=False,inplace=True)
  return df

def sort(exnum,head):
  c = 'a'
  c = gen.getCorpus(c)
  switcher = {
    2: { 'qryExpansion': 'AX',
          'beta-isin': [0.4, 0.5],
          'RetrievalCoefficient': 0.75,
         'corpus':c
        },
    3: {  'Df>': 10,
          'beta': 0.25
        }
  }

  criteria = switcher.get(exnum,{})

  file = pltgen.getFile(6, exnum)
  df = pd.read_csv(file, ',')
  df = pltgen.filterDf(df, criteria)
  # keys = ['TrecMAP']
  keys = list(df.columns)[8]
  df.sort_values(by=keys, ascending=False, inplace=True)
  df = df['corpus model beta fbDocs fbTerms TrecMAP'.split()]
  df = df.head(head)
  dfTerm =grouping(df,'fbTerms')
  dfDocs = grouping(df,'fbDocs')
  print('Original DataFrame \n' , df,'\nTop %d\n FeedBack Terms Count\n' % head, dfTerm, '\nFeedBack Documents Count \n',dfDocs)

if __name__ == '__main__':
  sort(2,15)
  print('Done')