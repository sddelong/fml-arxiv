import urllib

url = 'http://export.arxiv.org/api/query?search_query=all:Brownian%20dynamics%20without&start=0&max_results=5'

data = urllib.urlopen(url).read()



class Paper:
    
    def __init__(self,xml_data):
        
        
        






