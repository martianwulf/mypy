import re, csv, sys

def genUserName(fname, lname, address):
    #creates a username from the first name, last name and address
    mo = re.search(r'\d{5}$', address)
    if mo is None:
        return None
    else:
        user = '{}{}{}'.format(fname[0],lname[:5],mo.group()[1:])
        return user.lower()

def emailFromUser(user, domain):
    return '{}@{}'.format(user,domain)

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

if __name__ == '__main__':
    if len(sys.argv)>1:
        rmap = parseCommandMap(sys.argv)
    else:
        data = input('Enter map text: ')
        rmap = parseCommandMap(data)
    print(rmap)
