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
    unique_paper_list = []
    for j in range(len(paper_list)):
        unique_flag = True
        for k in range(j+1,len(paper_list)):
            if paper_list[j].id == paper_list[k].id:
                unique_flag = False
                print paper_list[j].title
                
        if unique_flag:
            unique_paper_list.append(paper_list[j])
                
                
    print "total articles: " , len(unique_paper_list)

    with open('TestData.pkl','wb') as file:
        dump(unique_paper_list,file)



