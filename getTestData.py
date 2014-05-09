import ArxivData as ad
from cPickle import dump
import time
from random import shuffle

paper_list = []

if __name__ == '__main__':

    # Note: Modified to be more relevant and increase total number of 
    #       articles for OfficialTestData2.pkl

    #originally was 5-30 - 04-02
    math_list = ad.GetPapersOAI('2014-02-20', '2014-03-08', 'math')

    print "math: ", len(math_list)

    #sleep for 21 , have to do this in order to use OAI MP again
    time.sleep(21)

    cs_list = ad.GetPapersOAI('2014-02-20', '2014-03-08', 'cs')

    print "cs: ", len(cs_list)

    time.sleep(21)

    phys_list = ad.GetPapersOAI('2014-01-20', '2014-03-10', 'physics')

    print 'math:', len(math_list), ', cs: ', len(cs_list), ', physics: ', len(phys_list)

    paper_list = math_list + cs_list  + phys_list#(ad.GetPapersOAI('2014-04-30','2014-05-02','math')
        #+ad.GetPapersOAI('2014-04-30','2014-05-02','cs'))

    #remove duplicates, do this the dumb way for now
    unique_paper_list = []
    for j in range(len(paper_list)):
        unique_flag = True
        for k in range(j+1,len(paper_list)):
            if paper_list[j].id == paper_list[k].id:
                unique_flag = False
                
        if unique_flag:
            unique_paper_list.append(paper_list[j])
                
                
    print "total articles: " , len(unique_paper_list)

    shuffle(unique_paper_list)

    with open('TestData.pkl','wb') as file:
        dump(unique_paper_list,file)



