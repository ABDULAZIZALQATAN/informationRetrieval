import json

def filterTerm (term):
    if (term == '' or term == None):
        term = 'None'
    else:
        term = str(term)
        for i in '; , "'.split() :
            term = term.replace(i, '')
        term = term.replace('\n','').replace('\r','')
    return term

def extractWAPOFields(path,outFile):
    # path = r'C:\Users\kkb19103\Desktop\TempFiles\WashingtonPost.v2\data'
    # inFile = path + '\dum.txt'
    # outFile = path + r'\kickerList.txt'
    f = open(path, 'r', encoding='utf8')
    outf = open(outFile, 'w')
    # outFile = path + r'\newDum.txt'
    # lines = []
    # Header
    line = 'docid,author,pubDate,kicker,byLine\n'
    outf.write(line)
    i = 1
    n = 0
    for line in f:
        if (line != ''):
            # outf2.write(line)
            line = json.loads(line)
            docid = line['id']
            author = line['author']
            pubDate = line['published_date']
            kicker = ''
            byLine = ''
            for item in line['contents']:
                if (item == None):
                    continue
                elif (item['type'] == 'kicker'):
                    kicker = item['content']
                elif (item['type'] == 'byline'):
                    byLine = item['content']
                    break
            if (kicker == ''):
                n += 1
            #    line = 'docid,author,pubDate,kicker,byLine\n'
            # if (i>=240707):
            #     print('None')
            line = docid
            for term in [author , pubDate , kicker , byLine]:
                line += ',' + filterTerm(term)
            line += '\n'
            # line = '%s,' * 5
            # line = line[:-1] + '\n'
            # line = line % (docid, author , pubDate , kicker , byLine)
            outf.write(line)
            print(i,line)
            i += 1
    print('Unfound Kickers : ', str(n))
    f.close()
    outf.close()

def pyseriniFormat(path):
    f = open(path,'r')
    newF = open(path.replace('.jl','collection.jl'),'w')
    ctr = 0
    for line in f:
        jsonLine = json.loads(line)
        id = jsonLine['id']
        contents = ''
        for item in  jsonLine['contents']:
            if item == None:
                continue
            val = ''
            if 'content' in item.keys():
                val = item['content']
            elif 'fullcaption' in item.keys():
                val = item['fullcaption']
            if val != '':
                contents += str(val) + ' '

        if contents != '':
            #  {"id": "doc1", "contents": "contents of doc one."}
            contents = contents.replace("\"","'")
            contents = contents.replace("\n",'').replace("\t",'').replace("\\",'/')
            newLine =  '{"id": "%s", "contents": "%s"}' % (id,contents)
            newF.write(newLine + '\n')
            ctr += 1
            print (ctr , '- Line Done : ' , newLine)

    f.close()
    newF.close()

if __name__ == '__main__':
    folder = r'C:\Users\kkb19103\Desktop\new\data'
    path = folder + r'\TREC_Washington_Post_collection.v2_Modified.jl'
    outFile = folder + r'\WAPOFields.csv'
    # pyseriniFormat(path)
    extractWAPOFields(path,outFile)
