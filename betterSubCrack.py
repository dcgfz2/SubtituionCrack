#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, collections, copy, re

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ .'


def main():
    #Replace spaces with ~ to make parsing easier
    KEY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ~.'
    
    with open (sys.argv[1], 'r') as sinput:
        MESSAGE = sinput.read()
    
    with open ('dictionary.txt','r') as f:
        DICTIONARY = dict()
        for line in f:
            for word in line.split():
                pattern = patternFinder(word)
                if pattern in DICTIONARY:
                    DICTIONARY[pattern].append(word)
                else:
                    DICTIONARY[pattern] = [word]
    
    FixSpacing = swapSingle(MESSAGE, '~', ' ')
    freq = collections.Counter(FixSpacing)

    POSSIBLEMAP = { 'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': [], 'K': [], 'L': [], 'M': [], 'N': [], 'O': [],
            'P': [], 'Q': [], 'R': [], 'S': [],'T': [], 'U': [], 'V' :[], 'W': [], 'X': [], 'Y': [], 'Z': [], '.': [], '~': []}
    ABSOLUTEMAP = copy.deepcopy(POSSIBLEMAP)
    for letter, count in freq.most_common(1):
        symIndex = KEY.find(letter.upper())
    ABSOLUTEMAP[KEY[symIndex]] = '~'
    splitat = KEY[symIndex] + '|' + KEY[symIndex].lower()
    IsSpace = KEY[symIndex]
    del POSSIBLEMAP[KEY[symIndex]]
    for letter, count in freq.most_common(2):
        symIndex = KEY.find(letter.upper())
    ABSOLUTEMAP[KEY[symIndex]] = 'E'
    del POSSIBLEMAP[KEY[symIndex]]
    for letter, count in freq.most_common(3):
        symIndex = KEY.find(letter.upper())
    ABSOLUTEMAP[KEY[symIndex]] = 'T'
    del POSSIBLEMAP[KEY[symIndex]]
    
    newlineCount = ''
    prevChar = ''
    beforeChar = ''
    for line in FixSpacing:
        if '\n' in line:
            if '\n' in prevChar:
                newlineCount += beforeChar
        beforeChar = prevChar
        prevChar = line
        
    freq = collections.Counter(newlineCount)
    theStop = ''
    for letter, count in freq.most_common(2):
        if theStop == '':
            if '\n' not in letter:
                theStop = letter.upper() 
    
    ABSOLUTEMAP[theStop] = '.'
    del POSSIBLEMAP[theStop]

    W_list = []
    tempMAP = newLettermap()
    Timeslooped = 0
    while Timeslooped == 0:
        for line in re.split(splitat, FixSpacing):
            HasKnowns = 0
            skipit = 0
            for letter in line:
                if letter.upper() not in ABSOLUTEMAP:
                    skipit = 1
                else:
                    if len(ABSOLUTEMAP[letter.upper()]) == 1:
                        HasKnowns += 1
            if HasKnowns != 0 and skipit == 0:
                semiconvert = ''
                for letter in line:
                    if ABSOLUTEMAP[letter.upper()] == '.':
                        semiconvert += ''
                    elif len(ABSOLUTEMAP[letter.upper()]) == 1:
                        semiconvert += str(ABSOLUTEMAP[letter.upper()])
                    else:
                        semiconvert += '^'
                removeStop = ''
                for letter in line:
                    if letter.upper() != theStop:
                        removeStop += letter
                word_pattern = patternFinder(removeStop)
                W_list.clear()
                if word_pattern in DICTIONARY:
                    for refrence in DICTIONARY[word_pattern]:
                        LIndex = 0
                        HasKnowns = 0
                        for letters in refrence:
                            if (letters.upper() != semiconvert[LIndex]) and semiconvert[LIndex] != '^':
                                HasKnowns = 1
                            LIndex +=1
                        if HasKnowns == 0:
                            W_list.append(refrence)
                    for item in W_list:
                        LIndex = 0
                        for letter in item:
                            if semiconvert[LIndex] == '^':
                                if letter.upper() not in tempMAP[line[LIndex].upper()]:
                                    tempMAP[line[LIndex].upper()] += letter.upper()
                            LIndex += 1
                POSSIBLEMAP = OverlapMaps(POSSIBLEMAP, tempMAP, KEY)
                tempMAP.clear()
                tempMAP = newLettermap()
                Timeslooped += 1               
                for letter in POSSIBLEMAP:
                    if len(POSSIBLEMAP[letter]) == 1:
                        ABSOLUTEMAP[letter] = POSSIBLEMAP[letter].pop()
                        Timeslooped = 0
                for letter in ABSOLUTEMAP:
                    if len(ABSOLUTEMAP[letter]) == 1:
                        if letter in POSSIBLEMAP:
                            del POSSIBLEMAP[letter]
    NotAvail = []
    for key in ABSOLUTEMAP:
        NotAvail.append(ABSOLUTEMAP[key])
    for letter in POSSIBLEMAP:
        for item in letter:
            if item in NotAvail:
                letter.remove(item)

    StillAvail = []
    for key in KEY:
        if key  not in NotAvail:
            StillAvail.append(key)

    KEY = makeKey(ABSOLUTEMAP, StillAvail)    
    DecryptMESSAGE = decrypt(KEY, MESSAGE)
    
    print(DecryptMESSAGE, file=open(sys.argv[2], 'w'))

def decrypt(key, text):
    message = ''
    for symbol in text:
        if (symbol.upper() in LETTERS):
            symIndex = LETTERS.find(symbol.upper())
            if key[symIndex] == '*':
                message += symbol
            elif symbol.isupper():
                message += key[symIndex].upper()
            else:
                message += key[symIndex].lower()
        else:
            message += symbol
    return message    
def patternFinder(word):
    lettermap = ''
    pattern = ''
    for char in word.upper():
        if char.upper() in lettermap:
            syIndex = lettermap.find(char.upper())
            pattern += str(syIndex)
        else:
            pattern += str(len(lettermap))
            lettermap += char.upper()
    return pattern
def swapSingle(message, char, replace):
    newmessage = ''
    for word in message:
        if word.upper() == replace.upper():
            if word.isupper():
                newmessage += char.upper()
            else:
                newmessage += char.lower()
        else:
            newmessage += word
    return newmessage
def newLettermap():
    MAPPERS = { 'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': [], 'K': [], 'L': [], 'M': [], 'N': [], 'O': [],
             'P': [], 'Q': [], 'R': [], 'S': [],'T': [], 'U': [], 'V' :[], 'W': [], 'X': [], 'Y': [], 'Z': [], '.': [], '~': []}
    return MAPPERS
def OverlapMaps(RMAP, LMAP, key):
    Combined = newLettermap()
    
    for items in key:
        if items not in RMAP:
            del LMAP[items]
            del Combined[items]
        else:
            if not RMAP[items]:
                Combined[items] = copy.deepcopy(LMAP[items])
            elif not LMAP[items]:
                Combined[items] = copy.deepcopy(RMAP[items])
            else:
                for letter in RMAP[items]:
                    if letter in LMAP[items]:
                        Combined[items].append(letter)
    return Combined
def makeKey(diction, remain):
    replaceKey = ''
    for letter in LETTERS:
        converter = letter
        if converter == ' ':
            converter = '~'
        if converter in diction:
            sconverter = diction[converter]
            if sconverter == '~':
                sconverter = ' '
            replaceKey += sconverter
        else:
            replaceKey += remain[0]
    return replaceKey
if __name__=='__main__':
    main()
