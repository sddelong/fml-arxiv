import ArxivData as ad
from cPickle import dump

paper_list = []

if __name__ == '__main__':
    
    math_list = ad.GetPapersOAI('2014-04-30', '2014-05-02', 'math')
    #cs_list = ad.GetPapersOAI('2014-04-30', '2014-05-02', 'cs')
    print 'math:', len(math_list)#, ', cs:', len(cs_list)

    #maybe narrow a bit, just pick a handful of different subcategories:
    # 'math-ph','math.NA','math.FA','

    paper_list = math_list #+cs_list #(ad.GetPapersOAI('2014-04-30','2014-05-02','math')
        #+ad.GetPapersOAI('2014-04-30','2014-05-02','cs'))

    with open('TestData.pkl','wb') as file:
        dump(paper_list,file)



