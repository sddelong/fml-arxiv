import ArxivSubjects as arxs
from ArxivData import GetPapersOAI
from ArxivData import GetAbstracts

import Perceptron as perc

class Arxiver:
    
    def __init__(self,classifier):

        self.classifier = classifier
        self.subjects = None
        self.subcategories = None
        self.name = ''


    def SetUp(self):
        """ Ask for name, subjects and subcategories"""
        
        #initialize subjects and subcategories
        self.subjects = []
        self.subcategories = dict()

        #gather subjects and subcategories
        go_again = True
        while go_again:
            print 'Please enter an arXiv category from the following list:'
            print arxs.subject_list
    
            while True:
                subject = raw_input()
    
                if subject in arxs.subject_list:
                    break
                else:
                    print 'Invalid subject, please choose from list.'
    
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
    
                self.subjects.append(subject)
                self.subcategories[subject] = subcategories

            else:
                # no subcategories, just subject
                self.subjects.append(subject)

            answered = False
            while answered == False:
                in_str = raw_input("Would you like to look at another subject as well? yes/no.")

                if in_str in ["yes","Yes","y","Y","1"]:
                    go_again = True
                    answered = True
                elif in_str in ["no","No","n","N","0"]:
                    go_again = False
                    answered = True
                else:
                    print "Please input yes or no."
                    answered = False

        return
    
    def CheckTodaysPapers(self):
        """ Use OAI to get today's papers and check them one at a time asking for user input."""

        paper_list = GetPapersOAI()

    def Prompt(self):
        """ Present an abstract to the user 
        """        
        
    def Run(self):
        """ Run the algorithm by presenting abstracts, receiving labels and calling function to
                update weights.
        """

        #filename where data is stored
        data_filename = "./" + user_name + "CustomTestData.pkl"

        data_file = open(data_filename,"rb")


        paper_list = cPickle.load(data_file)

        #print paper_list

        #initialize list of labels
        label_list = []

        #Vectorize abstracts
        vectors = FeaturizeAbstracts(GetAbstracts(paper_list))

        classifier = perc.PerceptronClassifier(1.0)
        for i, x in enumerate(vectors):
            #Predict abstract, make y_hat
            paper = paper_list[i]
            y_hat = classifier.Predict(x)

            if y_hat == 1:
                #Present paper, make update if needed
                y = PromptUser(paper)
                if y == 1:


            elif y_hat == -1:
                #make k

                if k == 1:
                    y = PromptUser(paper)

                else:
                    

            print "-"*80
            #If prediction is 1, present paper, make update
            #Else if predition is -1, make k
            #If k=1 present abstract, make update
            #If k=0 don't
            label = PromptUser(paper)
            label_list.append(label)


        out_file = open(str(user_name) + "customlabels.pkl","wb")
        cPickle.dump(label_list,out_file)



#    def CheckAbstract(x, label)
#        """ Receive data and label for one abstract, make prediction 
#        """













        #for i in range(len(data)):
            x = data[i]
            y_hat = classifier.Predict(x)
            if y == 1 and y_hat == 1:
                if i > threshold:
                    n_pos_right += 1
            elif y == -1 and y_hat == -1:
                #update total_negative_checks count if we had to check, 
                # and for adaptive p, update value of current_p
                if self.p == 'adaptive':
                    #got it correct, reduce p towards 0.01, our minimum
                    #print "current p is", self.current_p
                    if np.random.binomial(1,self.current_p) == 1:
                        self.current_p = 0.9*self.current_p + 0.001
                        total_negative_checks += 1
                        if i  > threshold :
                            total_end_negative_checks += 1
                else:
                    if np.random.binomial(1,self.p) == 1:
                        total_negative_checks += 1
                        if i  > threshold :
                            total_end_negative_checks += 1

            elif y_hat == 1 and y == -1:
                #update on false positive, add one to n_wrong
                if i > threshold:
                    n_precision_wrong += 1
                classifier.Update(x,y_hat,y)
            else:
                #maybe update on false negative, depends on p.
                if i > threshold:
                    n_recall_wrong += 1
                if self.p == 'adaptive':
                    # got it wrong, move current_p toward 1.0
                    # to check more frequently
                    #print "current p is", self.current_p
                    k = np.random.binomial(1,self.current_p)
                    if k == 1:
                        total_negative_checks += 1
                        if i  > threshold :
                            total_end_negative_checks += 1
                        classifier.Update(x,y_hat,y)
                        self.current_p = 0.55*self.current_p + 0.4
                else:
                    k = np.random.binomial(1,self.p)
                    if k == 1:
                        total_negative_checks += 1
                        if i  > threshold :
                            total_end_negative_checks += 1
                        classifier.Update(x,y_hat,y)

