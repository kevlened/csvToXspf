import xspf
import csv
import sys, os

usagerules = 'usage: python csvToXspf.py [csv location] [xspf destination]'

def csv_to_xspf(csvloc, xspfloc):
    if not os.path.exists(csvloc):
        print usagerules
        print "csv location doesn't exist"
        return

    playlist = xspf.Xspf(title='GrooveShark Playlist')

    csvreader = unicode_csv_reader(open(csvloc))
    csvreader.next()
    for row in csvreader:
        name, artist, album = row[0], row[1], row[2]
        # album is least likely to be clean or accurate - not included
        playlist.add_track(title=name, creator=artist)

    playlistxspf = playlist.toXml()

    with open(xspfloc, 'w') as xspffile:
        try:
            xspffile.write(playlistxspf)
            print "xspf saved at: " + str(xspfloc)
        except:
            print "unable to save xspf"

##http://stackoverflow.com/questions/904041/reading-a-utf8-csv-file-with-python
def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]

def main(args):
    try:
        inputcsv = args[0]
        outputxspf = args[1]
    except:
        print "needs two arguments - " + usagerules
        return

    csv_to_xspf(inputcsv,outputxspf)

if __name__ == '__main__':
    main(sys.argv[1:])
