import ArxivData as ad
from cPickle import dump

paper_list = []

if __name__ == '__main__':
    paper_list = (ad.GetPapersOAI('2014-04-30','2014-05-02','math')
        +ad.GetPapersOAI('2014-04-30','2014-05-02','cs'))

with open('TestData.pkl','w') as file:
    dump(paper_list,file)



