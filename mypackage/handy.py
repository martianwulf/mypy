#handy module
import re, os.path
from configparser import ConfigParser

class QuitException(Exception):
    pass

def testQuit(choice):
    '''returns True if choice == "quit" and False otherwise'''
    quitRegex = re.compile(r'^quit$',re.I)
    qmo = quitRegex.search(choice)
    if qmo == None:
        return False
    else:
        return True

def testQuit2(choice):
    '''Raises QuitException when choice == "quit"'''
    qmo = re.search(r'^quit$', choice, re.I)
    if qmo:
        raise QuitException("QUIT")

def testQuit3(statment):
    '''Raises QuitException when input == "quit"'''
    temp = input(statment)
    qmo = re.search(r'^quit$', temp, re.I)
    if qmo:
        raise QuitException("QUIT")
    else:
        return temp    

def parseConfigFile(filename, section):
    '''returns a dictionary of items in a config file'''
    parser = ConfigParser()
    configDict = {}
    try:
        parser.read(filename)
        if parser.has_section(section):
            items = parser.items(section)
            for item in items:
                configDict[item[0]] = item[1]
    except Exception as e:
        pass
    finally:
        return configDict

def dictWordCount(s):
    #returns a dictionary of all the word and their number of occurence in the argument 's'
    d = {}
    a = 0
    i = 0
    count = len(s)
    foundWord = False
    for char in s:
        if char.isalnum():
            #current char is alphanumeric
            #if this is the first before a whitespace, start of a word
            if foundWord == False:
                foundWord = True
                a = i
            if (foundWord and (count-1)==i ):
                sub = s[a:i]
                if sub in d.keys():
                    d[sub] += 1
                else:
                    d[sub] = 1
                    break
        else:
            if foundWord ==  True:
                sub = s[a:i]
                if sub in d.keys():
                    d[sub] += 1
                else:
                    #add sub and set initial value of 1
                    d[sub] = 1
                foundWord = False
        i+=1
    return d

def parseMapString(args):
    #accepts a string structured like a map as a command line
    #argument or as keyboard input
    data = None
    if type(args) is str:
        data = args
    elif type(args) is list:
        data = ' '.join(args[1:])
    else:
        return {}
    regex = re.compile(r'\'[\w]+\':\s\'.{,}?\'')
    keyvalreg =re.compile(r'\'([\w]+)\':\s\'(.{,})\'')
    outmap = {}
    
    #print(data)
    tupall = regex.findall(data)
    for pairs in tupall:
        m = keyvalreg.findall(pairs)
        #print(m)
        outmap[m[0][0]] = m[0][1]
        #print('m {0}'.format(str(m)))
        #for piece in m:
    return outmap

def mapFolder(location):
    m = []
    for dir, subs, files in os.walk(location):
        #if not len(m):
        #    root = location
        #    m[root] = []
        for sub in subs:
            m.append({os.path.join(dir, sub):False})
        for file in files:
            m.append({os.path.join(dir, file):False})
    return m
