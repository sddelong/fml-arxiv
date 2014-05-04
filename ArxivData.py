""" Module to import data from arxiv in real time.  Used to fetch data for online learning of 
    document preferences.  """

import urllib
import re #for removing namespaces, featurizing abstracts
import sys
from xml.etree import ElementTree as ET
from sklearn.feature_extraction.text import TfidfVectorizer
import time

class TextFeatureVector:
    """ feature vector, just a dictionary of words present in an abstract, and for each word
    a counter that keeps track of (# occurences)/(# total "relevant" words), where relevant words
    are everything but stop words. """
    
    def __init__(self):
        
        self.words = dict();
        self.total_words = 0

    def AddWord(self,word):
        """ add word to self.words. """
        if word in iter(self.words):
            self.words[word] = self.words[word] + 1
        else:
            self.words[word] = 1
            
        self.total_words += 1
            
        return

    def _mul_(self,other):
        """ dot product of two feature vectors """

        value = 0
        for word in iter(self.words):
            if word in other.words:
                value += self.words[word]*other.words[word]
                
        value = float(value)/float(self.total_words)/float(other.total_words)
        
        return value

    def dot(self,weights):
        """ dot product with vector of weights, similar to _mul_ above, but 
        weights won't have a total_words, it will be just numeric."""

        value = 0
        for word in iter(self.words):
            if word in weights:
                value += self.words[word]*weights[word]
                
        value = float(value)/float(self.total_words)

        return value

    def __str__(self):
        
        string_rep = "{ "
        for word in iter(self.words):
            string_rep += word + ": " + str(float(self.words[word])/float(self.total_words)) + ", "
        
        return string_rep + "}"

    __repr__ = __str__

    # end of class TextFeatureVector

    

class Paper:
    """ Class to hold paper information.

    member variables:
               title - string, title of the paper
               abstract - string, abstract of the paper
               authors - list of strings, names of authors of the paper.
               published - string, date and time the paper was published.
    """

    def __init__(self,entry,xml_type):
        
        """create a paper object from an XML entry, which could be returned 
        from a query using the arxiv api, in which case specify xml_type == "query", 
        or it could be from an rss feed, in which case specify xml_type == "rss"
        """
        
        if xml_type == "query":
            self.title = entry.find('title').text
            self.abstract = entry.find('summary').text
        
            self.authors = []
            authors = entry.findall('author')
            for author in authors:
                name = author.find('name').text
                self.authors.append(name)

            self.published = entry.find('published').text

        elif xml_type == "rss":
            self.title = entry.find('title').text
            self.abstract = entry.find('description').text
        
            self.authors = []
            authors = entry.find('dc:creator').text
            #TODO: Parse this.

#            for author in authors:
#                name = author.find('name').text
#                self.authors.append(name)

            self.published = None # TODO(delong) Make this todays date.

        else:
            print "Error: xml_type must be one of: query, rss"
            raise NotImplementedError
        


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
        paper_list.append(Paper(entry,"query"))
    
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

def IDFromLink(link):
    """
    quick helper function to get an article id from a string of its link
    
    inputs:
         link - string link to a paper, assumed to be of 
                the form http://arxiv.org/abs/<paper-id>
    outputs:
         paper_id - string with just the id
    """
    paper_id = link[21:]

    return paper_id
    

def GetTodaysPapers():
    """ 
    GetTodaysPapers()
    
    Function to get all arxiv papers published on the current day.
    
    inputs:
            <none>

    return value:
           This function returns a list of Paper objects, populated from the papers on Arxiv
    """

    #list of all subjects to grab papers from
    subject_list = ["cs","math","physics","cond-mat","math-ph","stat"]

    #initialize paper list
    id_list = []
    paper_list = []
    
    #TODO, loop through subjects
    url = "http://export.arxiv.org/rss/math"


    #extract info here.
    data = urllib.urlopen(url).read()
    
    #remove namespaces
    data = re.sub(' xmlns="[^"]+"', '', data, count=1)
    
    root = ET.fromstring(data)

    for item in root.findall('item'):
        id_list.append(IDFromLink(item.find('link').text))

    
    query_str = "id:" + str(id_list[0])
    for k in range(1,len(id_list)):
        query_str = query_str + "+OR+id:" + str(id_list[k])
    
    #now get URL for all papers we want TODO: don't hardcode length, make this work
    url = 'http://export.arxiv.org/api/query?search_query={0}&max_results=300'.format(query_str)
    
    #get xml data
    data = urllib.urlopen(url).read()
    #remove namespace
    data = re.sub(' xmlns="[^"]+"', '', data, count=1)
    # get root
    root = ET.fromstring(data)
    
    #create list of papers
    for entry in root.findall('entry'):
        this_paper = Paper(entry,"query")
        print "this paper published", this_paper.published
        print "todays date", time.strftime("%Y-%m-%d")
        #check that the paper was published today, not just updated.
        if this_paper.published[0:10] == time.strftime("%Y-%m-%d"):
            paper_list.append(this_paper)
            
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


def FeaturizeAbstract(abstract):
    """ Given a string of the abstract, return a TextFeatureVector object: a vector of frequency of the word. 
        Excludes stop words.
    
    inputs:
        abstract - string of abstract text for the paper
        
    outputs:
        abstract_vector  -  feature vector stored as a dictionary of normalized word frequency 
                            (portion of words in the document equal to the given word).

    """
    stop_words = ["is","it","that","the","a","an","of","in","this","and"]

    #initialize feature vector
    text_features = TextFeatureVector()

    bag_of_words = re.findall(r"[\w']+",abstract)
    for word in bag_of_words:
        word = word.lower()
        if word not in stop_words:
            text_features.AddWord(word)
            
    return text_features
            
if __name__ == "__main__":

    paper_list = SearchPapers(sys.argv[1],2)
#    paper_list = GetTodaysPapers()

#    for paper in paper_list:
#        paper.Print()
        
#    vectorizer = TfidfVectorizer()
    abstracts = GetAbstracts(paper_list)

    feature_vector = FeaturizeAbstract(abstracts[0])
    print feature_vector

#    print abstracts
#    abstract_vectors = vectorizer.fit_transform(abstracts)
#    print abstract_vectors.shape
#    print abstract_vectors.nnz/float(abstract_vectors.shape[0])
                          
