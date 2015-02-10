#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Week 2 Assignment"""


from datetime import datetime
import urllib2
import logging
import csv
import argparse
import sys


# 'http://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv'


parser = argparse.ArgumentParser()
parser.add_argument('--url', help='display a url with a csv')
args = parser.parse_args()

logging.basicConfig(filename='errors.log', level=logging.ERROR)
logger = logging.getLogger('assignment2')


def downloadData(url=''):
    '''
    Takes in a string of url and returns info from it.
    '''
    response = urllib2.urlopen(url)
    return response


def processData(info):
    '''
    Takes in CSV and returns dictionary with id as the key and
    name and birthday in a tuple as the value
    '''
    csvFile = csv.reader(open(info))
    dictInfo = {}

    for row in csvFile:
        idnum = row[0]
        name = row[1]
        date = row[2]

        try:
            bday = datetime.strptime(date, '%d/%m/%Y')
            dictInfo[idnum] = (name, bday)
        except ValueError:
            logging.error(
                'Error processing line #{0} for ID #{1}'.format(
                    int(idnum) + 1, idnum))
    return dictInfo


def displayPerson(id, personData):
    '''
    If the ID number is valid, a sentence with information
    is printed out.
    '''
    try:
        bday = datetime.strftime(personData[id][1], '%Y-%m-%d')
        print 'Person #{0} is {1} with a birthday of {2}.'.format(
            id, personData[id][0], bday)
    except:
        print 'No user found with that id'


if not args.url:
    sys.exit()
else:
    try:
        loop = True
        while loop:
            csvData = downloadData(args.url)
            personData = processData(csvData)
            idpick = int(raw_input('Pick an id number: '))
            print idpick

            if idpick > 0:
                displayPerson(idpick, personData)
            else:
                loop = False

    except URLError:
        sys.exit()