""" Module to import data from arxiv in real time.  Used to fetch data for online learning of 
    document preferences.  """

import urllib
import re #for removing namespaces
import sys
from xml.etree import ElementTree as ET
from sklearn.feature_extraction.text import TfidfVectorizer

class Paper:
    """ Class to hold paper information.

    member variables:
               title - string, title of the paper
               abstract - string, abstract of the paper
               authors - list of strings, names of authors of the paper.
               published - string, date and time the paper was published.
    """

    def __init__(self,entry):
        #blank
        self.title = entry.find('title').text
        self.abstract = entry.find('summary').text
        
        self.authors = []
        authors = entry.findall('author')
        for author in authors:
            name = author.find('name').text
            self.authors.append(name)

        self.published = entry.find('published').text

    def Print(self):
        print "--------------------------"
        print "Title:", self.title
        print "  "
        print "Authors:"
        for author in self.authors:
            print author
        print "  "
        print "Published: ", self.published
        print "Abstract:"
        print self.abstract
        print "  "   

        return
        
def SearchPapers(input_str,max_results=5):
    """ Function to search arxiv for papers and return a list of paper objects
     a format we like.

     inputs:
           input_str - string to search arxiv for
           max_results - maximum number of papers to return, default 5

     return value:
           paper_list - list of paper objects containing the returned data.

     """

    paper_list = []

    url = 'http://export.arxiv.org/api/query?search_query=all:{0}&start=0&max_results={1}'.format(input_str,max_results)

    data = urllib.urlopen(url).read()

    #remove namespaces
    data = re.sub(' xmlns="[^"]+"', '', data, count=1)
    
    root = ET.fromstring(data)
    
    for entry in root.findall('entry'):
        paper_list.append(Paper(entry))
    
    return paper_list


def PrintEntry(entry):
    """ Given an entry from an xml tree, print information about the paper

    inputs:
          entry - xml tree entry from arxiv
    return:
          <No Return Value>
          
    """

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
    print "Published: ", entry.find('published').text                      
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

    data = urllib.urlopen(url).read()

    #remove namespaces
    data = re.sub(' xmlns="[^"]+"', '', data, count=1)
    
    root = ET.fromstring(data)

    for entry in root.findall('entry'):
        paper_list.append(Paper(entry))

    return paper_list


def GetAbstracts(paper_list):
    """ Given a list of papers, return a list containing the abstracts 

    inputs: 
         paper_list - list of papers
    
    return value:
         abstract_list - list of strings, each string is the abstract of 
                         the corresponding paper.
         
   """
    abstract_list = []
    for paper in paper_list:
        abstract_list.append(paper.abstract)
        
    return abstract_list
            

if __name__ == "__main__":

    paper_list = SearchPapers(sys.argv[1],20)

#    for paper in paper_list:
#        paper.Print()
        
    vectorizer = TfidfVectorizer()
    abstracts = GetAbstracts(paper_list)

#    print abstracts
    abstract_vectors = vectorizer.fit_transform(abstracts)
    print abstract_vectors.shape
    print abstract_vectors.nnz/float(abstract_vectors.shape[0])
                          
