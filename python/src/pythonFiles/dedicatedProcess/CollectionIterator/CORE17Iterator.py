import xml.dom.minidom as dm
import os
import pythonFiles.dedicatedProcess.CollectionIterator.WAPOIterator as wa
import pandas as pd

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def getByTag_Attribute(xml , tagName,attribute):
    tag = xml.getElementsByTagName(tagName)
    return '' if (len(tag) < 1) else getByAttribute(tag[0], attribute)

def getByAttribute (tag, attribute):
    return tag.attributes[attribute].value


def getTitle(xml):
    # Retrieved Fields - title
    tagName = 'title'

    tag = xml.getElementsByTagName(tagName)
    if (len(tag) < 1):
        result = 'None'
    else:
        result = getText(tag[0].childNodes)
    return [result]

def getMeta (xml):
    '''
    Retrieved Fields
    slug publication_day_of_month - publication_month
    publication_year - publication_day_of_week
    dsk - online_sections
    '''
    tagName = 'meta'
    tags = xml.getElementsByTagName(tagName)
    targetTagNames = 'slug publication_day_of_month publication_month publication_year publication_day_of_week dsk online_sections'.split()
    result = {}
    # Initialize Names
    for name in targetTagNames :
        result[name] = 'None'

    for item in tags:
        name = getByAttribute(item, 'name')
        if (result.__contains__(name)):
            value = getByAttribute(item, 'content')
            result[name] = value
    result = list(result.values())
    return result

def getDocdata (xml):
    '''
    Retrieved Fields :
    doc-id - doc.copyright-holder - doc.copyright-year -
    descriptor - types_of_material - date_publication
    '''
    tagName = 'doc-id'
    docid = getByTag_Attribute(xml,tagName,'id-string')
    tagName = 'doc.copyright'
    copyrightHolder = getByTag_Attribute(xml,tagName,'holder')
    copyrightYear = getByTag_Attribute(xml,tagName,'year')
    # descriptor - types_of_material
    classifiers = xml.getElementsByTagName('classifier')
    [descriptor,material] = ['None','None']
    for item in classifiers:
        aType = getByAttribute(item,'type')
        if (aType == 'descriptor'):
            descriptor =  getText(item.childNodes)
        elif (aType == 'types_of_material'):
            material = getText(item.childNodes)
    date_publication = getByTag_Attribute(xml,'pubdata','date.publication')

    result = [docid,copyrightHolder,copyrightYear,descriptor,material,date_publication]
    return result

def processFile (file):
    print('Processing ' , file)
    xml = dm.parse(file)
    result = getDocdata(xml)
    result += getTitle(xml)
    result += getMeta(xml)
    xml = None
    for i in range (len(result)):
        result[i] = wa.filterTerm(result[i])
    return  [','.join(result) + '\n']

def iterateFiles (folder):
    items = os.listdir(folder)
    result = []
    for item in items:
        fullItem = folder + '/' + item
        if os.path.isdir(fullItem):
            result += iterateFiles(fullItem)
        else:
            result +=  processFile(fullItem)
    return result

def unionDf ():
    outFile = r'C:\Users\kkb19103\Desktop\new\data\years\CORE17FieldAlls.csv'
    outf = open(outFile,'w',encoding='utf-8')
    line = 'doc-id,doc.copyright-holder,doc.copyright-year,descriptor,types_of_material,date_publication,title,'
    # MetaData
    line += 'publication_day_of_month,publication_month,publication_year,publication_day_of_week,dsk,online_sections\n'
    outf.write(line)

    # df = pd.DataFrame()
    for i in range(1987,2007):
        file = r'C:\Users\kkb19103\Desktop\new\data\years\CORE17Fields%s.csv' % i
        f = open(file,'r',encoding='utf-8')
        f.readline()
        for line in f:
            outf.write(line)
            print('Moved: ' , line)
        f.close()
        # dfTemp = pd.read_csv(file)
        # df = pd.concat([df,dfTemp],ignore_index=True)
    # df.to_csv(outFile)

def main():
    # for year in range(1991,2008):
    #     processYear(year)
    # file = r'C:\Users\kkb19103\Desktop\new\data\CORE17\data\1991/01/21/0416845.xml'
    # x = processFile(file)
    # print(x)
    # unionDf()
    print('Done')


def processYear(year):
        year = str(year)
        print('Processing Year : %s\n' % year)
        path = r'C:\Users\kkb19103\Desktop\new\data\CORE17\data\%s' % year
        outFile = r'C:\Users\kkb19103\Desktop\new\data\years\CORE17Fields%s.csv' % year
        lines = iterateFiles(path)
        f = open(outFile,'w',encoding='utf-8')
        # Header Line
        # DocData + Title
        line = 'doc-id,doc.copyright-holder,doc.copyright-year,descriptor,types_of_material,date_publication,title,'
        # MetaData
        line += 'publication_day_of_month,publication_month,publication_year,publication_day_of_week,dsk,online_sections\n'
        f.write(line)
        for line in lines:
            f.write(line)
        f.close()
        print('Done Year : %s\n' % year)

if __name__ == '__main__':
    main()