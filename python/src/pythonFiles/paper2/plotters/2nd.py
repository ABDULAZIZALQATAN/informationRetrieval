# This Module is For Plotting Check Bigrams Charts
import pythonFiles.plotters.csvPlotterGen as pltgen
import pandas as pd
import matplotlib.pyplot as plt
import classes.general as gen


inCorpus = "a"  # @param ["a", "c", "w"]
inExp = "ax"  # @param ["AX", "RM3"]
inXAxis = "fbTerms"  # @param [ "fbTerms",'fbDocs']
inYAxis = "TrecMAP"  # @param ["TrecMAP", "TrecBref", "TrecP10", "CWLMAP","CWLRBP0.4","CWLRBP0.6" , "CWLRBP0.8"]

# *** End Colab Form ***

def getvBase (base):
    result = 'fbTerms' if base == 'fbDocs' else 'fbDocs'
    return  result

def showFigure():
    # outputFile
    # Set Ticks

    # if (ticks != None):
    #     plt.xticks(pltgen.getTicks(ticks))
    # ticks = getTicks(inYAxis)
    # if (ticks != None):
    #     plt.yticks(pltgen.getTicks(ticks))

    ticks = '0 55 5'
    plt.xticks(pltgen.getTicks(ticks))
    # ticks = '0.2 0.32 0.01'
    # plt.yticks(pltgen.getTicks(ticks))

    [fFamily, fSize, fWeight] = pltgen.getFont()

    # Set Legend
    legend = getvBase(inXAxis)
    plt.legend(title=legend, ncol=2)
    # Set Title
    line = "%s - %s\nBM25 - b = 0.75" % (inCorpus.upper() , inExp)
    # line+=add
    plt.title(line,size=fSize,family=fFamily,weight=fWeight)
    # Set Axis Labels
    line = pltgen.getAxisLabel(inXAxis)
    plt.xlabel(line,size=fSize,family=fFamily,weight=fWeight)
    line = pltgen.getAxisLabel(inYAxis)
    plt.ylabel(line,size=fSize,family=fFamily,weight=fWeight)

    plt.show()

def getDataFrame(measure,criteria):
    file = pltgen.getFile(measure, 2)
    df = pd.read_csv(file, ',')
    keys = 'corpus model qryExpansion beta fbDocs fbTerms'
    df = pltgen.filterDf(df, criteria)
    df = pltgen.sortDf(df, keys)
    return df

def plot():

    beta = 0.4 if inExp == 'AX' else 0.5
    criteria = {
        'corpus':inCorpus,
        'qryExpansion':inExp,
        'beta': beta,
        'RetrievalCoefficient':0.75
    }
    dfY = getDataFrame(inYAxis , criteria)
    dfX = dfY
    vBase = getvBase(inXAxis)
    vRange = range (5,55,5)
    fig = plt.figure(1)
    for item in vRange:
        criteria = {
            vBase: item,
        }
        xValues = pltgen.filterDf(dfX, criteria)[inXAxis]
        yValues = pltgen.filterDf(dfY, criteria)[inYAxis]
        marker = pltgen.getMarker(item)
        label = str(item)
        plt.plot(xValues, yValues, marker=marker, markersize=8, label= label)

    # pltgen.drawBaseLine(plt, inXAxis, inYAxis, inCorpus, 2)
    showFigure()
    fName = r'C:\Users\kkb19103\Desktop\new\%s-%s.png' % (inCorpus[:2],inExp)
    fig.savefig(fName)

if __name__ == '__main__':
    inExp = inExp.upper()
    for c in 'A C W'.split():
        inCorpus = gen.getCorpus(c)
        plot()

