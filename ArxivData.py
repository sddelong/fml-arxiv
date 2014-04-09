""" Module to import data from arxiv in real time.  Used to fetch data for online learning of 
    document preferences.  """

import urllib
import re #for removing namespaces
import sys
from xml.etree import ElementTree as ET


class Paper:
    """ Class to hold paper information.

    member variables:
               title - string, title of the paper
               abstract - string, abstract of the paper
               authors - list of strings, names of authors of the paper.
    """

    def __init__(self,xml_entry):
        #blank
        self.title =entry.find('title').text
        self.abstract = entry.find('summary').text
        
        self.authors = []
        authors = entry.findall('author')
        for author in authors:
            name = author.find('name').text
            self.authors.append(name)
        
        


def SearchPapers(input_str,max_results=5):
    """ Function to search arxiv for papers and print them to the screen.  In the future, will
    use something like this to collect data into a format we like."""

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


def GetDatedPapers(date,max_results = None):
    """ 
    GetDatedPapers(date,max_results)
    
    Function to get all arxiv papers published on a given date.  
    
    inputs:
          date - this function will return all papers on arxiv uploaded on this specified date
          max_results - optional upper limit on number of papers returned.

    return value:
           This function returns a list of Paper objects, populated from the papers on Arxiv
    """

    #initialize paper list
    paper_list = []
    
    if(max_results):
        url = 'http://export.arxiv.org/api/query?search_query=published:&start=0&max_results={1}'.format(date,max_results)
    else:
        url = 'http://export.arxiv.org/api/query?search_query=published:{0}&start=0'.format(date)

    #extract info here.

    return paper_list

    


        
if __name__ == "__main__":

    SearchPapers(sys.argv[1],4)
