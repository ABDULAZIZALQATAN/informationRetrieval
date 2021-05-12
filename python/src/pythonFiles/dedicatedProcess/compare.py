
def getFeature (ln):
    # Get specific feature to use for comparison
   parts = str(ln).split(" ",3)
   return parts[2]
   #return ln

def compareFiles(path1, path2):
    # Compare between two input files line by line and print the differences between them
    f1 = open(path1,'r')
    f2 = open(path2,'r')
    i = 1
    ctr = 0
    for ln1 in f1:
       ln2 = f2.readline()
       if (ln1 != ln2):
            print ("Line Differ " + str(i))
            print('Line 1 : ' + ln1)
            print('Line 2 : ' + ln2)
            ctr += 1
       i += 1
    print ('Done with ' + str(ctr) + " Differences")


def similarWordCount (path,baseWords,version):
    f = open(path, 'r')
    ctr = 0
    print (version + ' Version: \n')
    wordsSet = []
    for line in f:
        words = line.split(maxsplit=1)[1].replace('\n','')
        for word in words.split():
            if baseWords.count(word) > 0:
                wordsSet.append(word)
                ctr += 1
                if (len(wordsSet) == 15):
                    print(' '.join(wordsSet))
                    wordsSet.clear()
    f.close()
    print('\n')
    return ctr

def compareWords(path1,path2):
    baseFile = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\LUCENE\anserini\revertedIndex\prior\Old\WA-Df-500K.sts'
    f = open(baseFile,'r' , encoding='utf-8')
    baseWords = []

    for line in f:
        baseWords.append(line.split()[0])
    f.close()
    c1 = similarWordCount(path1,baseWords , 'Original')
    c2 = similarWordCount(path2,baseWords , 'Analyzed')

    print('The similarity between terms count in main DF file ( DF >= 2 )  And : \n' + \
          'Original Standard Query File 50 topics  : %d\n' % c1 + \
          'Analyzed Version Of Same Query File: %d ' % c2)

if __name__ == '__main__':
    mainPath = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\LUCENE\anserini\revertedIndex\prior\DFBigger02'
    # mainPath = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\Resources\WAPO'
    path2 = mainPath + '\BaseScore.res'
    path1 = mainPath + '\BaseScore500K.res'
    # compareWords(path1, path2)
    # compareFiles(path1,path2)
    compareFiles(path2,path1)