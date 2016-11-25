#currently holds functions for use with ftplib objects

def getText(ftp,filename, outfile=None):
    '''Fetches filename in formated text form from the current ftp directory and saves it to outfile'''
    if outfile is None:
        outfile = sys.stdout
    try:
        ftp.retrlines('RETR '+filename,lambda x, w = outfile.write: w(x+'\r\n'))
    except Exception as e:
        print(e)

def getBinary(ftp,filename, outfile):
    '''Fetches filename in binary from the current ftp directory and saves it to outfile'''
    ftp.retrbinary('RETR '+filename,outfile.write,8192)

def upload(ftp, filename):
    '''Uploads filename to the current ftp directory'''
    ext = os.path.splitext(filename)[1]
    try:
        with open(filename,'rb') as upfile:
            if ext in ('.php','.txt','.html','.htm','.css','.js'):
                fname = os.path.split(filename)[1]
                ftp.storlines('STOR '+fname,upfile)
            else:
                fname = os.path.split(filename)[1]
                ftp.storbinary('STOR '+fname,upfile,8192)
    except Exception as e:
        print(e)
