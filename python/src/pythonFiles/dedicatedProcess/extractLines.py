import os
def extract(file,num):
    aFile = open(file, 'r')
    newFile = open(file.replace('.jl','-extracted.jl'),'w')

    i = 0
    for line in aFile:
        i+=1
        if (i >= num):
            break
        else:
            newFile.write(line)
    newFile.close()
    aFile.close()

if __name__ == '__main__':
    num = 20
    file = r'/mnt/c/Users/kkb19103/Desktop/new/data/WAPO.jl'
    extract(file,num)
    print('Done')