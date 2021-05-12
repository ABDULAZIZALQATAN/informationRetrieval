# Begin Core17 Statistics
def countFiles (folder):
    ctr = 0
    for base , dirs , files in os.walk(folder):
        for file in files:
            ctr += 1
    return ctr

def findMissingCore17IDs(file):
    seq = 0
    f = open(file,'r',encoding='utf-8')
    f.readline()
    ctr = 0
    lineCtr = 0
    for line in f:
        docid = line.split(',',1)[0]
        docid = int(docid)
        if (seq == 0):
            seq = docid
        while (docid > seq):
            # print('Missing Line ' , '{:07d}.xml'.format(seq))
            seq += 1
            ctr += 1
        seq += 1
        lineCtr += 1
    # print ('Total Missing IDs:',ctr)
    result = [lineCtr , ctr]
    return result

def Core17Statistics (year):
    path = r'C:\Users\kkb19103\Desktop\new\data\CORE17\data\%d' % year
    filesCount = countFiles(path)
    path = r'C:\Users\kkb19103\Desktop\new\data\years\CORE17Fields%d.csv' % year
    result = findMissingCore17IDs(path)
    line = [str(x) for x in [year] + result + [filesCount]]
    line = ','.join(line)
    print(line)

# End Core-17 Statistics

if __name__ == '__main__':
    Core17Statistics(1987)