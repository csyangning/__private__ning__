#!/usr/bin/env python3
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process fyf lab csv data.')
    parser.add_argument('-f','--folder', dest='folderName', required=True,
                        type=str,help='The folder contains the csv files')

    args = parser.parse_args()
    print("folder name ={}".format(folderName))
