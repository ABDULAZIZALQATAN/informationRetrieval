import json

def filterContents (contents):
    filterDict = {
        "\"":"'" ,
        '\n':'',
        '\t': '',
        '\r':'',
        chr(28):'',
        '\\': '/'
    }
    for key , val in filterDict.items():
        contents = contents.replace(key, val)
    return contents.strip()

def parseWAPO(path,outpath):
    f = open(path,'r')
    newF = open(outpath,'w')
    ctr = 0
    for line in f:
        jsonLine = json.loads(line)
        id = jsonLine['id']
        title = jsonLine['title']
        author = jsonLine['author']
        pubdate = jsonLine['published_date']
        article_url = jsonLine['article_url']
        contents = ' '.join([id,str(title),author,str(pubdate),article_url])
        for item in  jsonLine['contents']:
            if item == None:
                continue
            if 'content' in item.keys():
                val = item['content']
                contents += str(val) + ' '
            elif 'fullcaption' in item.keys():
                val = item['fullcaption']
                contents += str(val) + ' '

        if contents != '':
            #  {"id": "doc1", "contents": "contents of doc one."}
            contents = filterContents(contents)
            newLine = '{"id": "%s", "contents": "%s"}' % (id, contents)
            newF.write(newLine + '\n')
            ctr += 1
            print (ctr , '- Line Done : ' , newLine)

    f.close()
    newF.close()

def removeNonIDs(path):
    f = open(path,'r')
    newf = open(path.replace('.jsonl', 'new.jsonl'), 'w')
    prevLine = ''
    ctr = 1
    for line in f:
        line = line.replace('\n','')
        if (line.startswith('{"id"')):
           newf.write(prevLine + '\n')
           print (ctr , 'Line is Done :' , prevLine)
           ctr += 1
           prevLine = line
        else:
          prevLine += line + ' '
    newf.write(prevLine + '\n')
    print(ctr, 'Line is Done :', prevLine)
    f.close()
    newf.close()

if __name__ == '__main__':
    path = r'/mnt/c/Users/kkb19103/Desktop/new/data/TREC_Washington_Post_collection.v2_Modified.jl'
    outpath = path.replace('.jl','collection.jsonl')
    parseWAPO(path,outpath)
    # path = r'/mnt/c/Users/kkb19103/Desktop/new/data/data/TREC_Washington_Post_collection.v2_Modifiedcollection.jsonl'
    # removeNonIDs(path)
