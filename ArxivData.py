import urllib
import re #for removing namespaces
import sys
from xml.etree import ElementTree as ET




class Paper:
    """ Class to hold paper information.  For now this is blank.  Could be useful later."""

    def __init__(self,xml_data):
        #blank
        self.title = "blah"
        



def SearchPapers(input_str,max_results=5):
    """ Function to search arxiv for papers and print them to the screen.  In the future, will
    use this to collect data into a format we like."""

    url = 'http://export.arxiv.org/api/query?search_query=all:{0}&start=0&max_results={1}'.format(input_str,max_results)

    data = urllib.urlopen(url).read()

    #remove namespaces
    data = re.sub(' xmlns="[^"]+"', '', data, count=1)
    
    root = ET.fromstring(data)
    
    for entry in root.findall('entry'):
        print "--------------------------"
        
        summary = entry.find('summary').text
        title = entry.find('title').text
        print "Title:", title
        print "  "
        print "Authors:"
        authors = entry.findall('author')
        for author in authors:
            name = author.find('name').text
            print name
        print "  "
        print "Abstract:"
        print summary
        print "  "   

    return
        
        
if __name__ == "__main__":

    SearchPapers(sys.argv[1],1)
