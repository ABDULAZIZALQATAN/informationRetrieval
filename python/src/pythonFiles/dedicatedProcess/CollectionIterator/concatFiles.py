import os
import pandas as pd
def main():
    folder  = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\2nd Experiment - RM3 VS AX\Faieness Measurement\concat'
    outFile = folder + '\\out.csv'
    df = pd.DataFrame()
    for file in os.listdir(folder):
        fName = folder + '\\' + file
        if os.path.isfile(fName):
            dfTemp = pd.read_csv(fName)
            df = pd.concat([df,dfTemp])
            print('Added:' , file)
    df.to_csv(outFile,index=None)

if __name__ == '__main__':
    main()