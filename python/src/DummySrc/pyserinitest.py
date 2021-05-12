

# import jnius_config as jc
# # jc.add_options('-Xrs', '-Xmx4096')
# # path = \  # '/mnt/c/Users/kkb19103/.m2/repository/*:' + \
# # path = '~/.local/lib/python3.9/site-packages/anserini/target/anserini-0.10.1-SNAPSHOT.jar'
# # jc.set_classpath('', path)
# # jc.set_classpath()
from pyserini.index import IndexReader as ir
from pyserini.search import SimpleSearcher as ss
from pyserini.search import querybuilder as qb
import jnius as js

def getQuery (qryDict):
    should = qb.JBooleanClauseOccur['should'].value
    booleanBuilder = qb.get_boolean_query_builder()
    i = 0
    for key , val in qryDict.items():
        term = qb.get_term_query(key)
        boost = qb.get_boost_query(term,val)
        booleanBuilder.add(boost,should)

    result = booleanBuilder.build()
    return result

def searcher ():
    # os.environ["JAVA_HOME"] = "/mnt/c/Program Files/Java/jdk-15.0.2/bin"
    # import itertools
    path = r'/mnt/c/Users/kkb19103/Desktop/new/data/WAPOIndex'
    searcher = ss(path)
    searcher.set_qld(100)
    boosts = [0.2,0.5,0.75,1.5,1,2,4]
    for bst in boosts:
        qryDict = {
            'women':bst
        }
        print('Percentage ' , bst)
        qry = getQuery(qryDict)
        hits = searcher.search(qry)
        for i in range(1):
            print(f'{i + 1:2} {hits[i].docid:7} {hits[i].score:.5f}')
    print('Done')

def tryjnius():
    Stack = js.autoclass('java.util.Stack')
    stack = Stack()
    stack.push('hello')
    stack.push('world')

    print (stack.pop())  # --> 'world'
    print (stack.pop())  # --> 'hello'
if __name__ == '__main__':

    searcher()
    # tryjnius()

