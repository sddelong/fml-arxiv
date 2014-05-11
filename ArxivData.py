""" Module to import data from arxiv in real time.  Used to fetch data for online learning of 
    document preferences.  """

import urllib
import re #for removing namespaces, featurizing abstracts
import sys
from xml.etree import ElementTree as ET
#from sklearn.feature_extraction.text import TfidfVectorizer
#import time
from datetime import datetime
import cPickle
import ArxivSubjects as arxs
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

    def GetWord(self,word):
        """ return value for a given word"""
        if word in iter(self.words):
            return float(self.words[word])/float(self.total_words)
        else:
            return 0.0
        
        
    def __mul__(self,other):
        """ dot product of two feature vectors """

        value = 0
        for word in iter(self.words):
            if word in other.words:
                value += self.words[word]*other.words[word]
                
        value = float(value)/float(self.total_words)/float(other.total_words)
        
        return value

    def Dot(self,weights):
        """ dot product with vector of weights, similar to _mul_ above, but 
        weights won't have a total_words, it will be just numeric."""

        value = 0
        for word in iter(self.words):
            if word in weights:
                value += self.words[word]*weights[word]
                
        value = float(value)/float(self.total_words)

        return value

    def UpdateWeights(self,weights,y,eta):
        """ update weights according to the rule weigts = weights + eta*x*y """
        for word in iter(self.words):
            if word in weights:
                weights[word] = weights[word] + eta*y*self.words[word]/self.total_words
            else:
                weights[word] = eta*y*self.words[word]/self.total_words
                
        return weights

    def UpdateWeightsSVM(self,weights,y,eta,C):
        """ update weights according to the rule 
        weights = weights - eta(w_t - C*x*y) 
        for online SVM"""
        
        for word in iter(self.words):
            if word in weights:
                weights[word] = weights[word] - eta*(weights[word] - C*y*self.words[word]/self.total_words)
            else:
                weights[word] = C*eta*y*self.words[word]/self.total_words
                
        return weights

    def Distance2(self,y):
        """ Calculate distance squared from self to y. 
            Used for Gaussian Kernel """
        distance = 0.
        for word in self.words:
            if word in y.words:
                distance += (self.words[word]/self.total_words - y.words[word]/y.total_words)**2
            else:
                distance += (self.words[word]/self.total_words)**2

        for word in y.words:
            if word not in self.words:
                distance += (y.words[word]/y.total_words)**2

        return distance
                
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
                id - string, arXiv identifier
    """

    def __init__(self, entry, xml_type):
        
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

        elif xml_type == "OAI":
            ns = {'ns':'http://www.openarchives.org/OAI/2.0/', 
                'dc':'http://purl.org/dc/elements/1.1/'}
            self.title = entry.find('.//{http://purl.org/dc/elements/1.1/}title').text #, namespaces=ns).text
            self.abstract = entry.find('.//{http://purl.org/dc/elements/1.1/}description').text #, namespaces=ns).text

            self.authors = []
            for author in entry.findall('.//{http://purl.org/dc/elements/1.1/}creator'): #, namespaces=ns):
                name = author.text
                self.authors.append(name)

            self.published = entry.find('.//{http://purl.org/dc/elements/1.1/}date').text #, namespaces=ns).text
            self.id = entry.find('.//{http://www.openarchives.org/OAI/2.0/}identifier').text #, namespaces=ns).text
        else:
            print "Error: xml_type must be one of: query, rss, OAI"
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
    data = re.sub(' xmlns:="[^"]+"', '', data, count=1)
    
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
    

def GetTodaysPapers(subject=''):
    """ 
    GetTodaysPapers()
    
    Function to get all arxiv papers published on the current day, using RSS feed
    
    inputs:
            <none>

    return value:
           This function returns a list of Paper objects, populated from the papers on Arxiv
    """
    

    #list of all subjects to grab papers from, check if optional argument set is in list
    subject_list = ['physics:astro-ph','physics:cond-mat','physics:gr-qc',
        'physics:hep-ex','physics:hep-lat','physics:hep-ph','physics:hep-th',
        'physics:math-ph','physics:nlin','physics:nucl-ex','physics:nucl-th',
        'physics','physics:quant-ph','math','cs','q-bio','q-fin','stat']

    if subject in subject_list:
        subject_string = '&set='+subject
    elif subject:
    #RAISE ERROR since subject doesn't match a set name TODO
        return
    else:
        subject_string = ''

    #set the URL using API, loop through subjects TODO
    url = "http://export.arxiv.org/rss/math"

    #extract info here.
    data = urllib.urlopen(url).read()
    
    #remove namespaces
    data = re.sub(' xmlns="[^"]+"', '', data, count=1)    
    root = ET.fromstring(data)

    #initialize paper list
    id_list = []
    paper_list = []    

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
        print "today's date", str(datetime.today())
        #check that the paper was published today, not just updated.
        if this_paper.published[0:10] == str(datetime.today()):
            paper_list.append(this_paper)
            
    return paper_list

def OAIWrapper():
    print 'Please enter an arXiv category from the following list:'
    print arxs.subject_list

    while True:
        subject = raw_input()
        
        if subject in arxs.subject_list:
            break
        else:
            print 'Invalid subject, please choose from list.'

    day = raw_input('Enter a start date in form YYYY-MM-DD:')
    print day
    until = raw_input('Enter an end date in form YYYY-MM-DD:')
    print until
    
    subcategories = []
    if arxs.subject_dict[subject]:
        print ('Enter all preferred subcategories from subject as listed below (capitalization). Enter "done" when finished.')
        print arxs.subject_dict[subject]
        
        while True:
            subcategory = raw_input()
            if subcategory in arxs.subject_dict[subject]:
                subcategories.append(subcategory)
                print "Please pick another subcategory or enter 'done'"
            elif subcategory == 'done':
                break
            else:
                print 'Must choose valid subcategory or enter "done" and continue.'

    paper_list = GetPapersOAI(day=day, until=until, subject=subject, subcategories=subcategories)

    return paper_list

def GetPapersOAI(day='', until='', subject='', subcategories=None):
    """ 
    Function to get all arxiv papers updated on the specific day within subject using OAI-PMH protocol,
        for harvesting large batches of papers.
    
    inputs:
            day
            until
            subject
            subcategories
            
    return value:
            This function returns a list of Paper objects, populated from Arxiv papers updated on given
            range of days within given subject set
    """
    
    if arxs.subject_dict[subject]:   
        subcategory_list = [arxs.subject_name[subject]+' - '+subcategory for subcategory in subcategories]
    else:
        subcategory_list = [arxs.subject_name[subject]]

    # if day not specified, get today's date as a string 'YYYY-MM-DD'; if until specified, create string
    # if until not specified, papers range through current day
    if not day:
        day = str(datetime.today())
    if until:
        until_string = '&until='+until

    #check for valid optional subject, create string
    if subject in arxs.subject_list:
        subject_string = '&set='+subject
    elif subject:
    #RAISE ERROR since subject doesn't match a set name TODO
        print "ERROR: Subject you specified does not exist on Arxiv."
        raise NameError
    else:
        subject_string = ''

    #set the URL using OAI-PMH standard, choosing from today's records with chosen subject, loop through subjects TODO
    url = 'http://export.arxiv.org/oai2?verb=ListRecords&from='+day+until_string+subject_string+'&metadataPrefix=oai_dc'

    #extract info here.
    data = urllib.urlopen(url).read()

    # declare namespaces
    ns = {'ns':'http://www.openarchives.org/OAI/2.0/',
        'dc':'http://purl.org/dc/elements/1.1/'}
    root = ET.fromstring(data)

    #initialize paper list
    paper_list = []    

    # create list of papers

    print len(root.findall('.//{http://www.openarchives.org/OAI/2.0/}record')), 'papers harvested.'
    if len(root.findall('.//{http://www.openarchives.org/OAI/2.0/}record')) == 1000:
        print 'Choose smaller date range to receive newer papers.'

    start = time.clock()
    for entry in root.findall('.//{http://www.openarchives.org/OAI/2.0/}record'): #, namespaces=ns):
        this_paper = Paper(entry, 'OAI')

        if IsPaperInSubcategories(entry, subcategory_list, ns):
            # check that the paper was published today, not just updated.
            if day and until:
                if (datetime.fromordinal(datetime.strptime(day, '%Y-%m-%d').toordinal()-5)
                    <= datetime.strptime(this_paper.published, '%Y-%m-%d')
                    <= datetime.strptime(until, '%Y-%m-%d')):
                    paper_list.append(this_paper)
            elif day:
                if (datetime.strptime(day, '%Y-%m-%d')
                    <= datetime.strptime(this_paper.published, '%Y-%m-%d')):
                    paper_list.append(this_paper)
              
    return paper_list

def IsPaperInSubcategories(entry,subcategories,ns):
    """
    Checks to see if any of the subjects of entry match any of the given subcategories. 
    
    inputs:
         entry - OAI format entry for paper (record)
         subcategories - list of strings given subcategories to check against
         ns - namespaces, dictionary of namespaces for OAI format, this doesn't work for old versions of python, so it is hardcoded for now
         
    outputs:
        is_in_sub - boolean, is this paper in any of the given subcategories or not.
    """
    
    paper_subcategories = [a.text for a in entry.findall('.//{http://purl.org/dc/elements/1.1/}subject')]

    for cat in paper_subcategories:
        if cat in subcategories:
            return True
        
    return False

def GetAbstracts(paper_list):
    """ 
    Given a list of papers, return a list containing the abstracts 

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


def PromptUser(entry):
    """ 
    For a given entry/record in arXiv, prompts user and receives
        a label from input

    inputs:
        entry - Paper object

    return value:
        label - paper label indicating like (1) or dislike (-1)

    """
    print 'Do you like this abstract?'
    entry.Print()
    input = raw_input('Yes/No?')
    
    answered = False
    while not answered:
        if input in ['Yes', 'yes', 'y', '1']:
            label = 1
            answered = True
        elif input in ['No', 'no', 'n', '0']:
            label = -1
            answered = True
        # use quit to leave
        elif input == 'quit':
            raise SystemExit('Exiting.')
        else:
            input = raw_input('Invalid response. Yes/No? Use "quit" to leave.')
    
#    if label == 1:
#        print entry.id

    return label


def FeaturizeAbstracts(abstracts):
    """ Given a list of abstracts, each a string, return a TextFeatureVector object: a vector of frequency of the word. 
        Excludes stop words.
    
    inputs:
        abstracts - list of strings of abstract text for the papers
        
    outputs:
        abstract_vectors  -  list of TextFeatureVectors, one for each abstract.

    """
    stop_words = ["is","it","that","the","a","an","of","in","this","and"]

    feature_list = []
    #initialize feature vector
    for abstract in abstracts:
        text_features = TextFeatureVector()
    
        bag_of_words = re.findall(r"[\w']+",abstract)
        for word in bag_of_words:
            word = word.lower()
            if word not in stop_words:
                text_features.AddWord(word)

        feature_list.append(text_features)

    return feature_list

 
if __name__ == "__main__":

    paper_list = GetPapersOAI('2014-05-02', '2014-05-03','math')
    print len(paper_list)
    print paper_list
#    rec_list = []
#    for paper in paper_list:
#        label = PromptUser(paper)

#        if label == 1:
#            rec_list.append(paper.id)
    
    
    #test Feature Vector stuff
    feature_vector = FeaturizeAbstracts(["This is a physics abstract.  Physics is presumably the topic."])

    #de-reference to get first (and only) feature vector
    feature_vector = feature_vector[0]    

    #stop words, this is a stop word
    assert 'this' not in feature_vector.words, "this shouldn't appear in feature vector, it is a stop word."
    
    assert feature_vector.GetWord('physics') == 2./5. , "physics should be 2/5 of the relevant words in this example."
    assert feature_vector.GetWord('presumably') == 1./5., "presumably should be 2/5 of the relevant words in this example."

    #test fetching and printing some machine learning abstracts. 
    # this is a "soft" test, no assertions.

    paper_list = SearchPapers("Machine Learning.")
    abstract_list = GetAbstracts(paper_list)
    
    outfile = open("./machinelearningtestpapers.pkl","wb")
    cPickle.dump(paper_list,outfile)

    print abstract_list

    
                          
