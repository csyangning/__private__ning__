#!/usr/bin/env python3
import argparse
import os

def ProcessCSVFile(folderName):
    resultFolder = os.path.join(folderName, "Result")
    print("Result will be saved in {}".format(resultFolder))

    if(not os.path.exists(resultFolder)):
        os.makedirs(resultFolder)

    for file in os.listdir(folderName):
        if file.lower().endswith(".csv"):
            fullPath = os.path.join(folderName, file)
            nameCol = []
            resultDictionary = {}
            headerMode = False
            resultMode = False

            print("Processing file {}...".format(fullPath))
            with open(fullPath, mode='rt', encoding='utf-8') as csvFile:
                lines = csvFile.readlines()
                for i in range(0, len(lines)):
                    if not lines[i]:
                        continue

                    if "Header" in lines[i]:
                        nameCol.append(lines[i + 3].strip('\n,'))
                        i = i + 3
                        headerMode = True
                        resultMode = False
                        continue

                    if "Result" in lines[i]:
                        headerMode = False
                        if resultMode:
                            nameCol.append(" ")
                        else:
                            resultMode = True
                        continue

                    if not headerMode:
                        result = lines[i].split(',')
                        if not result[0] in resultDictionary:
                            resultDictionary[result[0]] = []

                        resultDictionary[result[0]].append(result[1])


                processResult = ["{0},{1}\n".format(key, ','.join(resultDictionary[key])) for key in resultDictionary]
                resultFileFullName = os.path.join(resultFolder, file)
                with open(resultFileFullName, mode='wt', encoding='utf-8') as resultFile:
                    resultFile.write("{}\n".format(",".join(nameCol)))
                    resultFile.writelines(processResult)

    print("Process Complete")
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process fyf lab csv data.')
    parser.add_argument('-f','--folder', dest='folderName', required=True,
                        type=str,help='The folder contains the csv files')

    args = parser.parse_args()
    if(os.path.isdir(args.folderName) and os.path.exists(args.folderName)):
        print("Trying to process files under {}".format(args.folderName))
        ProcessCSVFile(args.folderName)
    else:
        print("{} doesn't exit".format(args.folderName))
