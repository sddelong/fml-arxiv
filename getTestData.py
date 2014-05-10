import ArxivData as ad
from cPickle import dump
import time
from random import shuffle

paper_list = []

if __name__ == '__main__':
    
    #get name
    name = raw_input("Please enter your name (no spaces.)")

    # Fetch articles from different subjects.
    go_again = True
    while go_again:
        this_paper_list = ad.OAIWrapper()
        print "Number of Articles found: ", len(this_paper_list)
        paper_list.extend(this_paper_list)


        answered = False
        while answered == False:
            in_str = raw_input("Would you like to look at another subject as well? yes/no.")

            if in_str in ["yes","Yes","y","Y","1"]:
                go_again = True
                answered = True
                print "Waiting for 20 seconds before retrieving data again from arxiv."
                time.sleep(20)
            elif in_str in ["no","No","n","N","0"]:
                go_again = False
                answered = True
            else:
                print "Please input yes or no."
                answered = False
            


    #remove duplicates, do this the dumb way for now
    unique_paper_list = []
    for j in range(len(paper_list)):
        unique_flag = True
        for k in range(j+1,len(paper_list)):
            if paper_list[j].id == paper_list[k].id:
                unique_flag = False
                
        if unique_flag:
            unique_paper_list.append(paper_list[j])
                
                
    print "total articles after removing duplicates: " , len(unique_paper_list)

    shuffle(unique_paper_list)

    with open(name + 'CustomTestData.pkl','wb') as file:
        dump(unique_paper_list,file)

