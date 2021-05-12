import matplotlib.font_manager as fm
import numpy as nm
import pandas as pd

# Get Value Lists
def getAxisLabel(axis):
    switcher = {
        'G0': "G - Cumulative - B = 0 - C = 100",
        'G0.5': "G - Gravity - B = 0.5 - C = 100",
        'TrecMAP': "MAP",
        'TrecP10': "P10",
        'TrecNDCG':"Trec NDCG",
        'CWLMAP': "CWL MAP",
        'CWLP10': "CWL P10",
        'CWLNDCG': 'CWL NDCG10',
        'TrecBref': "Binary Preference",
        'rSum0': "Total Retrievability Mass",
        'rSum0.5': "Total Retrievability Mass",
        'CWLRBP0.4' : 'Rank Biased Precision 0.4',
        'CWLRBP0.6': 'Rank Biased Precision 0.6',
        'CWLRBP0.8': 'Rank Biased Precision 0.8',
        'fbTerms': 'FbTerms',
        'fbDocs': 'FbDocs'
    }
    return switcher.get(axis)

def getMarker(i):
    switcher = {
        # Multiple  Indexes
        'U': "^",  # Upper Triangle
        'B': "o",  # Circle
        'C': "X",  # X Filled
        'F': "*",  # Star
        # RM3
        '5': "^",  # Upper Triangle
        '10': "o",  # Circle
        '15': "X",  # X Filled
        '20': "*",  # Star
        '25': "v",  # Upper Triangle
        '30': "s",  # Circle
        '35': "8",  # X Filled
        '40': "p",  # Star
        '45': "P",  # Upper Triangle
        '50': "H"
    }
    return switcher.get(str(i), "nothing")

def getChosenCoefficient(model):
    switcher = {
        'B': 0.75,
        'L': 310,
        'P': 5.1
    }
    return switcher.get(model[0].upper())

def getTicks(ticks):
    ticks = ticks.split()
    return nm.arange(float(ticks[0]), float(ticks[1]), float(ticks[2]))

def isKeyLabel(lbl):
    return lbl in ['fbTerms','fbDocs','beta','RetrievalCoefficient','Time']

def getFont():
    # Get Libertine Font From its File
    # Specify The Location of the File in Path Variable
    # Matplotlib cache should be deleted
    # ( The Contents of .matplotlib Folder should be deleted )
    path = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\My Work\libertine\opentype\LinLibertine_R.otf'
    prop = fm.FontProperties(fname=path)
    # [fFamily, fSize, fWeight]
    return [prop.get_name(),17,900]

def getExFolder (exNum):
    mainFolder = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\%s\CSV'
    switcher = {
        1: '1st Experiment - Bigrams Influence',
        2: '2nd Experiment - RM3 VS AX',
        3: '3rd Experiment - Reverted Index'
    }
    exFolder  = mainFolder % switcher.get(exNum)
    return exFolder

def filterDf (df, dictCriteria):
    '''
    First Criteria should be Equal criteria
    Operators might be inserted at the end of the key in input dictionary
    -< for <
    -> for >
    -! for !=
    -isin for isin
    '''
    if (len(dictCriteria) > 0):
        criteria = ''
        for item in dictCriteria:
          if (item.__contains__('-')):
              parts = item.split('-')
              key = parts[0]
              operator = parts[1]
              value = dictCriteria[item]
              if (operator == '<'):
                  criteria &= df[key] < value
              elif (operator == '>'):
                  criteria &= df[key] > value
              elif (operator == '!'):
                  criteria &= df[key] != value
              elif (operator == 'isin'):
                  criteria &= df[key].isin(value)
          else:
              # First Criteria should be Equal
              value = dictCriteria[item]
              if (len(criteria) == 0):
                criteria = df[item] == value
              else:
                  criteria &= df[item] == value
        df = df[criteria]
    return df

def getGroup (measure):
    group = 'ret' if (measure in ['G0', 'G0.5' , 'rSum0' , 'rSum0.5']) else 'per'
    return group

def convertRSum(series):
    tempXValues = []
    for i in range(series.size):
        temp = '{:.2f} M'.format(series.iat[i] / 1000000)
        tempXValues.append(temp)
    return tempXValues

def getFile (measure , exNum):
    exFolder = getExFolder(exNum)
    group = getGroup(measure)
    fName = '\Ex%d%s.csv' % (exNum,group)
    file = exFolder + fName
    # file = gen.getLinuxPath(file)
    return file

def sortDf(df , keys):

    keys = 'corpus model beta fbDocs fbTerms'.split() if keys == 3 else keys.split()
    df.sort_values(by=keys, inplace=True)
    return df

def getColumnIndex (df,hdr):
    return df.columns.get_loc(hdr)

def updateGiniCriteria (criteria , axis):
    if (axis.startswith('G')):
        b = float(axis.replace('G',''))
        criteria['RetrievabilityB'] = b
    return criteria

def getDfBaselineValue (axis,corpus,exnum):
    file = getFile(axis,exnum)
    switcher = {
        2:'qryExpansion',
        3:'type'
    }
    fldBaseLine = switcher.get(exnum,'')
    criteria = {
        fldBaseLine: 'Baseline',
        'corpus':corpus
    }
    df = pd.read_csv(file)
    criteria = updateGiniCriteria(criteria,axis)
    df = filterDf(df,criteria)
    if (axis.startswith('G')):
        axis = 'G'
    result = df[axis]
    return result

def drawBaseLine(plotter , xAxis,yAxis,corpus,exnum):
    x = getDfBaselineValue(xAxis,corpus,exnum)
    y = getDfBaselineValue(yAxis,corpus,exnum)

    plotter.plot(x, y,
             # marker='$B$',
             marker='o',
             markersize=12,
             color='r'
             )

