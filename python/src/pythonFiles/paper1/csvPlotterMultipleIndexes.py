# This Module is For Plotting Check Bigrams Charts
import python.src.pythonFiles.plotters.csvPlotterGen as gen
import pandas as pd
import matplotlib.pyplot as plt

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
#@markdown Check Bigrams Plot - Multiple Indexes

inCorpus = "Aquaint"  # @param ["Aquaint", "Core17", "WAPO",'All']
inModel = "BM25"  # @param ["BM25", "LMD", "PL2", 'All']
# @markdown The Number of values to plot - 0 for all
# PLotValuesCount = 0  # @param {type:"slider", min:0, max:16, step:1}
# @markdown Use Predefined ticks from ticks.csv files

inXAxis = "rSum0"  # @param ["RetrievalCoefficient", "TrecMAP" , "CWLMAP","rSum0", "rSum0.5"]
inYAxis = "G0"  # @param ["G0", "G0.5", "TrecMAP", "TrecBref", "TrecP10", "CWLMAP","CWLRBP0.6" , "CWLRBP0.8"]

# *** End Colab Form ***

GLegend = 'indexType'

def showFigure():
    # outputFile

    # Set Ticks
    # xTicks = gen.getTicks('5 55 5')
    # plt.xticks(xTicks)

    # Set Legend
    line = GLegend
    plt.legend(title=line, ncol=2)

    [fFamily, fSize, fWeight] = gen.getFont()
    # Set Title
    line = "%s - %s" % (inCorpus, inModel)
    plt.title(line.upper() ,size=fSize,family=fFamily,weight=fWeight)
    # Set Axis Labels
    line = gen.getAxisLabel(inXAxis)
    plt.xlabel(line,size=fSize,family=fFamily,weight=fWeight)
    line = gen.getAxisLabel(inYAxis)
    plt.ylabel(line,size=fSize,family=fFamily,weight=fWeight)

    plt.show()

def getDataFrame(measure):
    file = gen.getFile(measure,1)
    df = pd.read_csv(file, ',')
    criteria = {
        'corpus': inCorpus,
        'model': inModel
    }
    temp = None
    if (measure.startswith('rSum')):
        temp = float(measure.replace('rSum',''))
    elif (measure.startswith('G0')):
        temp = float(measure.replace('G',''))

    if (temp == None):
        keys = 'corpus indexType model RetrievalCoefficient'
    else:
        criteria['RetrievabilityB'] = temp
        keys = 'corpus indexType model RetrievabilityB RetrievalCoefficient'

    df = gen.filterDf(df, criteria)
    df = gen.sortDf(df,keys)
    return df



def plot():
    global inXAxis , inYAxis
    dfY = getDataFrame(inYAxis)
    if (gen.isKeyLabel(inXAxis) or gen.getGroup(inXAxis) == gen.getGroup(inYAxis)):
        dfX = dfY
    else:
        dfX = getDataFrame(inXAxis)
    legendRange = 'Unigram Bigram Combined Fielded'

    for item in legendRange.split():
        criteria = {GLegend: item + 'Index'}
        xValues = gen.filterDf(dfX, criteria)[inXAxis.replace('0.5','').replace('0','')]
        if (inXAxis.startswith('rSum')):
            xValues = gen.convertRSum(xValues)
        yValues = gen.filterDf(dfY, criteria)[inYAxis.replace('0.5','').replace('0','')]
        marker = gen.getMarker(item[0])
        plt.plot(xValues, yValues, marker=marker, markersize=8, label=item + 'Index')
    showFigure()
    print('Done')
if __name__ == '__main__':
    plot()