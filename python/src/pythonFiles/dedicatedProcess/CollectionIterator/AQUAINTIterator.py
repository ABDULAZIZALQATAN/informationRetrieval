import os
import pythonFiles.dedicatedProcess.CollectionIterator.WAPOIterator as wa
import pandas as pd

def extractValue (line,tag):
    line = line.replace(tag,'')
    tag = tag.replace('<','</',1)
    line = line.replace(tag,'').strip()

    # Filter Value
    line = wa.filterTerm(line)
    return line

def extractFields(xml):
    mainTags = '<DOCNO> <DOCTYPE> <DATE_TIME> <SLUG>'.split()
    result = ['None'] * 4
    tags = mainTags.copy()
    for line in xml.split('\n') :
        # ctr = 0
        if (len(tags) < 1):
            break
        for i in range(len(tags)):
            if line.startswith(tags[i]):
                value = extractValue(line , tags[i])
                temp = mainTags.index(tags[i])
                result[temp] = value
                tags.remove(tags[i])
                break
    return ','.join(result)

def processFile (file):
    f = open(file, 'r')
    files = ''.join(f.readlines())
    files = files.split('</DOC>\n')
    lines = []
    for xml in files:
      if (xml != ''):
        line =  extractFields(xml)
        lines.append(line)
        print('Added ',line)
    f.close()
    return '\n'.join(lines) + '\n'


def iterateGroup (groupPath,yearRange,outFile):
    f = open(outFile, 'a')
    for year in yearRange:
        folder = '%s\%d' % (groupPath, year)
        files = os.listdir(folder)
        for file in files:
            file = '%s\%s' % (folder,file)
            lines = processFile(file)
            f.write(lines)
    f.close()

def iterateFiles(outFile):
    # NYT Path
    f = open(outFile,'w')
    line = 'DOCNO,DOCTYPE,DATE_TIME,SLUG\n'
    f.write(line)
    f.close()
    groupPath = r'C:\Users\kkb19103\Desktop\new\data\TREC-Aquaint\aquaint_disk_1\nyt'
    yearRange = range(1998,2001)
    iterateGroup(groupPath,yearRange,outFile)
    folder = r'C:\Users\kkb19103\Desktop\new\data\TREC-Aquaint\aqauint_disk_2'
    groupPath = folder + r'\apw'
    yearRange = range(1998, 2001)
    iterateGroup(groupPath,yearRange,outFile)
    groupPath = folder + r'\xie'
    yearRange = range(1996, 2001)
    iterateGroup(groupPath, yearRange, outFile)
    print('All Done')

def removeDuplicates (file):
    df = pd.read_csv(file)
    df = df.drop_duplicates()
    df.to_csv(file)

def main():
    outFile = r'C:\Users\kkb19103\Desktop\new\data\AQUAINTFields.csv'
    # iterateFiles(outFile)
    # removeDuplicates(outFile)
    print('Done')
if __name__ == '__main__':
    main()