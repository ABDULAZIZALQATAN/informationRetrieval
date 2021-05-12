# This Module is For Plotting Check Bigrams Charts
import pythonFiles.plotters.csvPlotterGen as pltgen
import pandas as pd
import matplotlib.pyplot as plt
import classes.general as gen

# Import Module in G Drive

# drivePath = '/content/gdrive'
# modPath = '/My Drive/Colab Notebooks'
# from google.colab import drive
# drive.mount (drivePath )
# import sys
# sys.path.append(drivePath + modPath)
# import csvPlotterGeneral as gen

"""
 *** Start Colab Form ***
 Input Data
 @title Plot Bias & Performance Experiments
"""
inCorpus = "a"  # @param ["a", "c", "w"]
inModel = "BM25"  # @param ["BM25", "LMD", "PL2"]
# inExp = "RM3"  # @param ["AX", "RM3"]
##PredefinedTicks = "No"  # @param ["Yes", "No"]
inBase = "fbTerms" # @param ["fbDocs", "fbTerms",'beta']
inXAxis = "TrecNDCG"  # @param ['RetrievalCoefficient', "fbTerms",'fbDocs',"TrecMAP", "TrecBref", "TrecP10", "CWLMAP","CWLRBP0.4","CWLRBP0.6" , "CWLRBP0.8"]
inYAxis = "G0"  # @param ["G0", "G0.5", "TrecMAP", "TrecBref", "TrecP10", "CWLMAP","CWLRBP0.4","CWLRBP0.6" , "CWLRBP0.8"]

# *** End Colab Form ***

def getTicks (axis):
    result = None
    if (inBase == 'beta'):
        switcher = {
            # AQUAINT
            'A-TrecMAP': '0.18 0.27 0.01' ,
            'A-TrecP10': '0.37 0.46 0.01',
            'A-G0': '0.41 0.54 0.01',
            # CORE 17
            'C-TrecMAP': '0.2 0.33 0.01',
            'C-TrecP10': '0.46 0.6 0.01',
            'C-G0': '0.48 0.62 0.01',
            # WAPO
            'W-TrecMAP': '0.23 0.34 0.01',
            'W-TrecP10': '0.44 0.52 0.01',
            'W-G0': '0.37 0.52 0.01'
        }
        val = '%s-%s' % (inCorpus[0], axis)
    else:
        switcher = {
            # AQUAINT
            # fbDocs
            'A-fbDocs-TrecMAP':'0.18 0.26 0.01' ,
            'A-fbDocs-TrecP10': '0.37 0.46 0.01',
            'A-fbDocs-G0': '0.41 0.51 0.01',
            # fbTerms
            'A-fbTerms-TrecMAP': '0.18 0.25 0.01',
            'A-fbTerms-TrecP10': '0.35 0.47 0.01',
            'A-fbTerms-G0': '0.41 0.51 0.01',
            # CORE 17
            # fbDocs
            'C-fbDocs-TrecMAP': '0.2 0.31 0.01',
            'C-fbDocs-TrecP10': '0.46 0.59 0.01',
            'C-fbDocs-G0': '0.48 0.6 0.01',
            # fbTerms
            'C-fbTerms-TrecMAP': '0.2 0.31 0.01',
            'C-fbTerms-TrecP10': '0.46 0.59 0.01',
            'C-fbTerms-G0': '0.48 0.6 0.01',
            # WAPO
            # fbDocs
            'W-fbDocs-TrecMAP': '0.23 0.33 0.01',
            'W-fbDocs-TrecP10': '0.44 0.53 0.01',
            'W-fbDocs-G0': '0.37 0.49 0.01',
            # fbTerms
            'W-fbTerms-TrecMAP': '0.23 0.33 0.01',
            'W-fbTerms-TrecP10': '0.42 0.52 0.01',
            'W-fbTerms-G0': '0.37 0.49 0.01'
        }
        val = '%s-%s-%s' % (inCorpus[0],inBase,axis)
    result = switcher.get(val,None)
    return result

def getPlotValues(exp,item):
    colors = 'orange green blue'.split()
    if (exp == 'RM3'):
        line = '--'
        markers = '^ X v'
    else:
        line = '-'
        markers = '8 * s'
    markers = markers.split()
    iItem = int(item / 10 - 1)
    color = colors[iItem]
    marker = markers[iItem]
    label = '%s-%d' % (exp, item)
    return [label,color , marker , line]

def getvBase ():
    result = 'fbTerms' if inBase == 'fbDocs' else 'fbDocs'
    return  result

def getFirstCriteria ():
    retrievalCoefficient = pltgen.getChosenCoefficient(inModel)
    criteria = {
         'corpus': inCorpus,
         'model': inModel,
         'RetrievalCoefficient': retrievalCoefficient,
         inBase + '-<':35
            }

    if inBase == 'beta':
        add = {
            'beta-isin': [0.25, 0.5 , 0.75],
            'fbDocs':20,
            'fbTerms-isin':[10,20,30]
        }
    else:
        add = {
            'beta-isin': [0.4, 0.5]
        }

    criteria.update(add)
    return criteria

def showFigure():
    # outputFile
    # Set Ticks
    ticksCriteria = '-'.join([inBase,inXAxis])
    switcher = {
        'fbTerms-MAP'
    }

    ticks = getTicks(inXAxis)
    if (ticks != None):
        plt.xticks(pltgen.getTicks(ticks))
    ticks = getTicks(inYAxis)
    if (ticks != None):
        plt.yticks(pltgen.getTicks(ticks))

    [fFamily, fSize, fWeight] = pltgen.getFont()

    if (inBase == 'beta'):
        legend = 'Expansion-fbTerms'
        add = 'xAxis Over beta - [0.25,0.5,0.75] fbDocs = 20'
    else:
        legend = 'Expansion-' + getvBase()
        add = 'xAxis Over %s - [5:5:30]' % inBase
    # Set Legend
    plt.legend(title=legend, ncol=2)
    # Set Title
    line = "%s - %s - b = 0.75\n" % (inCorpus.upper() ,  inModel.upper())
    line+=add
    plt.title(line,size=fSize,family=fFamily,weight=fWeight)
    # Set Axis Labels
    line = pltgen.getAxisLabel(inXAxis)
    plt.xlabel(line,size=fSize,family=fFamily,weight=fWeight)
    line = pltgen.getAxisLabel(inYAxis)
    plt.ylabel(line,size=fSize,family=fFamily,weight=fWeight)

    plt.show()

def getDataFrame(measure):
    file = pltgen.getFile(measure, 2)
    df = pd.read_csv(file, ',')
    criteria = getFirstCriteria()

    keys = 'corpus model qryExpansion beta fbDocs fbTerms'
    # if (inStageNumber == 1):
    #     keys += ' RetrievalCoefficient'

    df = pltgen.filterDf(df, criteria)
    df = pltgen.sortDf(df, keys)
    return df

def plot(outPath):
    dfY = getDataFrame(inYAxis)
    if (pltgen.isKeyLabel(inXAxis) or pltgen.getGroup(inXAxis) == pltgen.getGroup(inYAxis)):
        dfX = dfY
    else:
        dfX = getDataFrame(inXAxis)
    vBase = getvBase()
    if (inBase == 'beta'):
        vBase = 'fbTerms'

    vRange = [10, 20, 30]

    if inYAxis.startswith('G'):
        yCriteria = {'RetrievabilityB': int(inYAxis.replace('G', ''))}
        yCaption = 'G'
    else:
        yCriteria = {}
        yCaption = inYAxis
    fig = plt.figure(inCorpus)
    for exp in ['AX','RM3']:
        beta = 0.4 if exp == 'AX' else 0.5
        for item in vRange:
            criteria = {
                vBase: item,
                'qryExpansion':exp,
            }
            if (inBase != 'beta'):
               criteria['beta'] = beta
            xValues = pltgen.filterDf(dfX, criteria)[inXAxis]
            criteria.update(yCriteria)
            yValues = pltgen.filterDf(dfY, criteria)[yCaption]
            # marker = gen.getMarker(str(item))
            [label , color , marker , line] = getPlotValues(exp,item)
            plt.plot(xValues, yValues,color=color , ls=line, marker=marker, markersize=8, label= label)
    pltgen.drawBaseLine(plt, inXAxis, inYAxis, inCorpus, 2)
    showFigure()
    if (outPath != ''):
        fName = '\%s-%s-%s-%s.png' % (inCorpus, inBase, inXAxis, inYAxis)
        fig.savefig(outPath + fName)
if __name__ == '__main__':
    path = r'C:\Users\kkb19103\Desktop\new'
    # path = ''
    for c in 'A C W'.split():
        inCorpus = gen.getCorpus(c)
        plot(path)

