import pythonFiles.paper2.AdditionalAnalysis.plotRelevanceExposure as relexp
import pythonFiles.paper2.AdditionalAnalysis.generateCSV as gencsv
# import pythonFiles.paper2.AdditionalAnalysis.generateRetFile as genret
import pandas as pd


def getTwoNumbers (num):
    return '{:02d}'.format(int(num))

def getRetDf (corpus,exp , docs , terms):
    # WA-AX-0.4-30-15.csv
    path = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\2nd Experiment - RM3 VS AX\DocLength Analysis\DocLength Analysis\RetFiles'
    beta = '0.4' if exp == 'AX' else '0.5'
    fName = path + '\%s-%s-%s-%s-%s.csv' % (corpus,exp,beta,docs,terms)
    df = pd.read_csv(fName)
    return df

def getFullDf (corpus,exp , docs , terms):
    docs = getTwoNumbers(docs)
    terms = getTwoNumbers(terms)

    file = gencsv.getMainFile(corpus)
    df = pd.read_csv(file,low_memory=False)
    dfr = getRetDf(corpus,exp , docs , terms)
    df = df.merge(dfr, 'left', 'docid')

    # for b in [0]:
    #     dfr = genret.getRetrievabilityResults(corpus, exp, b, docs, terms)
    #     df = df.merge(dfr, 'left', 'docid')

    return df


def process(group,corpus,exp , docs , terms , b):
    # Get The Full Df including r Values
    df = getFullDf(corpus,exp , docs , terms)

    '''
    Calculate Exposure_g
    	For each group calculate the sum of the r(d) values 
        Then workout the proportion of r(d) for each group g.  = Exposure_g
    '''
    fld = 'r' + str(b)
    dfTemp = df.groupby(group,as_index=False).agg({fld:'sum'})
    Exposure_g = relexp.compute_percent(dfTemp[fld])
    '''
    Calculate Rel_g
    	For each group, calculate the sum of the #rels for each 
    	group g, = Rel_g    = sum of rels for group / total rels over the collection
    '''
    fld = 'rel'
    dfTemp = df.groupby(group, as_index=False).agg({fld: 'sum'})
    Rel_g = relexp.compute_percent(dfTemp[fld])
    '''
    Calculate Size_g 
        For each group, calculate the total group member - 
        i.e. the number of documents in the group = Size_g
    '''
    fld = 'docid'
    dfTemp = df.groupby(group, as_index=False).agg({fld: 'count'})
    Size_g = relexp.compute_percent(dfTemp[fld])
    '''
    Calculate Group_g
    - [GROUPs] ALL GROUPS ARE EQUAL
        For each group, Group_g = 1/(Number of groups). 
    '''
    fld = 'group'
    dfTemp[fld] = 1
    Group_g = relexp.compute_percent(dfTemp[fld])

    # Calculate Fairness
    rel_exposure = relexp.compute_fairness_score(Rel_g,Exposure_g)
    size_exposure = relexp.compute_fairness_score(Size_g,Exposure_g)
    Grp_exposure = relexp.compute_fairness_score(Group_g,Exposure_g)
    result = [ str(x) for x in [rel_exposure,size_exposure,Grp_exposure]]
    return result

def main():
    corpus = 'wa'
    exp = 'AX'
    docs = 5
    terms = 5
    group = 'author'
    result = process(group , corpus,exp , docs , terms)
    result = ','.join(result)
    print(result)

if __name__ == '__main__':
    main()