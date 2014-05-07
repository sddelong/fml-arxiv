import ArxivData as ad
from cPickle import dump
import time

paper_list = []

if __name__ == '__main__':
    
    math_list = ad.GetPapersOAI('2014-04-29', '2014-05-02', 'math')

    #sleep for 21 , have to do this in order to use OAI MP again
    time.sleep(21)

    cs_list = ad.GetPapersOAI('2014-04-29', '2014-05-02', 'cs')

    print 'math:', len(math_list), ', cs: ', len(cs_list)

    paper_list = math_list + cs_list #(ad.GetPapersOAI('2014-04-30','2014-05-02','math')
        #+ad.GetPapersOAI('2014-04-30','2014-05-02','cs'))

    #remove duplicates, do this the dumb way for now
    remove_list = []
    for j in range(len(paper_list)):
        for k in range(j,len(paper_list)):
            if paper_list[j].id == paper_list[k].id:
                remove_list.append(paper_list[k])
                
    for r in remove_list:
        paper_list.remove(r)

    print "total articles: " , len(paper_list)

    with open('TestData.pkl','wb') as file:
        dump(paper_list,file)



