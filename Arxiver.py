import ArxivSubjects as arxs
from Perceptron import PerceptronClassifier, MarginPerceptronClassifier, VotedPerceptronClassifier
from Perceptron import KernelPerceptronClassifier
from OnlineSVM import OnlineSVMClassifier
from WeightedMajority import WeightedMajorityClassifier
from ArxivData import GetPapersOAI
from ArxivData import GetAbstracts
from ArxivData import FeaturizeAbstracts
from datetime import datetime
import errno, urllib, os, cPickle, time
import numpy as np
import Perceptron as perc


def mkdir_p(path):
    #helper function for making directories
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


#define kernel functions locally so we can pickle them
def GaussianKernel(x,y):

    return np.exp(x.Distance2(y)/(2.))

def PolynomialKernel(x,y):
        
    return (x*y)**3

def MakeWeightedMajorityClassifier():
    """ wrapper to make weighted majority classifier from
    Perceptron, Margin perceptron, SVM, Gaussian kernel Perceptron Classifier, Polynomial Kernel Perceptron Classifier 
    For use directly with Arxiver, all parameters hard coded for now"""


    pclassifier = PerceptronClassifier(1.0)
    v_pclassifier = VotedPerceptronClassifier(1.0)
    margin_pclassifier = MarginPerceptronClassifier(1.0, 0.03125)
    svmclassifier = OnlineSVMClassifier(0.25, 1.0)
    gk_pclassifier = KernelPerceptronClassifier(1.0,GaussianKernel)
    pk_pclassifier = KernelPerceptronClassifier(1.0,PolynomialKernel)    

    classifier_list = [pclassifier, v_pclassifier, margin_pclassifier, svmclassifier, gk_pclassifier, pk_pclassifier]
    
    wm_classifier = WeightedMajorityClassifier(classifier_list)
    
    return wm_classifier
    

class Arxiver:
    
    def __init__(self,classifier,p):

        self.classifier = classifier
        self.subjects = None
        self.subcategories = None
        self.name = ''
        self.p = p
        self.current_p = 1.0 #only used if p = 'adaptive'
        self.p_min = 0.01
        self.gamma_1 = 0.55
        self.gamma_2 = 0.1
        

    def SetUp(self):
        """ Ask for name, subjects and subcategories"""
        
        print "Please enter a name for new Arxiver."
        self.name = raw_input()
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
    
    def CheckDaysPapers(self,date):
        """ Use OAI to get today's papers and check them one at a time asking for user input."""

        mkdir_p("./" + self.name + "/" + date)
        paper_list = []
        for subject in self.subjects:
            print "Gathering ", subject, " papers."
            if subject != self.subjects[0]:
                #sleep for 20 if we just asked for papers from OAI. 
                time.sleep(20)
            paper_list += GetPapersOAI(day=date,until='',subject=subject, subcategories=self.subcategories[subject])
            print "total papers published on relevant dates:", len(paper_list)


        abstract_vectors = FeaturizeAbstracts(GetAbstracts(paper_list))

        #shuffle data so there is no pattern from getting one subject at a time.
        
        np.random.shuffle(abstract_vectors)

        for i, x in enumerate(abstract_vectors):
            y_hat = self.classifier.Predict(x)
            paper = paper_list[i]
            if y_hat == 1:
                #Present paper, make update if needed
                print "-"*60
                y = self.Prompt(paper,y_hat)
                if y == 1:
                    self.SavePaper(paper,date)
                else:
                    self.classifier.Update(x,y_hat,y)
            elif y_hat == -1:
                #make k #update total_negative_checks count if we had to check, 
                # and for adaptive p, update value of current_p
                if self.p == 'adaptive':
                    if np.random.binomial(1,self.current_p) == 1:
                        print "-"*60
                        y = self.Prompt(paper,y_hat)
                        #check if correct, if so reduce p towards .01
                        if y == 1: #incorrect
                            self.current_p = self.current_p + self.gamma_1*(1. - self.current_p)
                            self.SavePaper(paper_list[i],date)
                            self.classifier.Update(x,y_hat,y)
                        elif y == -1:
                            #correct negative prediction, leave classifier alone and decrease p
                            self.current_p = self.current_p - self.gamma_2*(self.current_p - self.p_min)
                else:
                    #check with fixed probability p
                    if np.random.binomial(1,self.p) == 1:
                        y = self.Prompt(paper,y_hat)
                        if y != y_hat:
                            # wrong, the paper is good, save it and upate
                            self.SavePaper(paper_list[i],date)
                            self.classifier.Update(x,y_hat,y)

        print "-"*60
        print "-"*60
        print "Done classifying papers."
        return
            

    def Prompt(self, paper,y_hat):
        """ Present an abstract to the user and ask for a label
        """        

        if y_hat == 1:
            print "Arxiver thinks you will like this paper: "
            paper.Print()
            answered = False
            ans = raw_input("Do you like this paper?")
            while not answered:
                if ans in ['Yes', 'yes', 'y', '1']:
                    y = 1
                    answered = True
                elif ans in ['No', 'no', 'n', '0']:
                    y = -1
                    answered = True
        # use quit to leave
                elif ans == 'quit':
                    raise SystemExit('Exiting.')
                else:
                    ans = raw_input('Invalid response. Yes/No? Use "quit" to leave.')
        elif y_hat == -1:
            print "Arxiver thinks you do NOT like this paper.  Please confirm."
            paper.Print()

            answered = False
            ans = raw_input( "Do you like this paper?")
            while not answered:
                if ans in ['Yes', 'yes', 'y', '1']:
                    y = 1
                    answered = True
                elif ans in ['No', 'no', 'n', '0']:
                    y = -1
                    answered = True
        # use quit to leave
                elif ans == 'quit':
                    raise SystemExit('Exiting.')
                else:
                    ans = raw_input('Invalid response. Yes/No? Use "quit" to leave.')
            
        return y
        
#    def Run(self):
#       """ Run the algorithm by presenting abstracts, receiving labels and calling function to
#                update weights.
#        """
#        pass
        #filename where data is stored
#        data_filename = "./" + user_name + "CustomTestData.pkl"
#
#        data_file = open(data_filename,"rb")
#
#        paper_list = cPickle.load(data_file)
#        chosen_papers = []
#
#        #initialize list of labels
#        label_list = []
#
#        #Vectorize abstracts
#        vectors = FeaturizeAbstracts(GetAbstracts(paper_list))
#
#        classifier = perc.PerceptronClassifier(1.0)
#        for i, x in enumerate(vectors):
#            #Predict abstract, make y_hat
#            paper = paper_list[i]
#            y_hat = classifier.Predict(x)
#
#
#            if y_hat == 1:
#                #Present paper, make update if needed
#                print "-"*80
#                y = PromptUser(paper)
#                if y == 1:
#                    chosen_papers.append(paper)
#                    if i > threshold:
#                        n_pos_right += 1
#                else:
#                #update on false positive, add one to n_wrong
#                    classifier.Update(x,y_hat,y)
#                    if i > threshold:
#                        n_precision_wrong += 1
#
#            #y_hat == -1:        
#            else: 
#                #update total_negative_checks count if we had to check, 
#                # and for adaptive p, update value of current_p
#                if self.p == 'adaptive':
#                    #got it correct, reduce p towards 0.01, our minimum
#                    if np.random.binomial(1,self.current_p) == 1:
#                        print "-"*80
#                        y = PromptUser(paper)
#                        #check if correct, if so reduce p towards .01
#                        if y == 1:
#                            self.current_p = 0.9*self.current_p + 0.001 #TODO: This was a wrong negative, increase p
#                            total_negative_checks += 1
#                            if i  > threshold :
#                                total_end_negative_checks += 1
#
#                            self.current_p = 0.9*self.current_p + 0.001
#                            total_negative_checks += 1
#                            chosen_papers.append(paper)
#                            classifier.Update(x,y_hat,y)
#                            self.current_p = 0.55*self.current_p + 0.4
#                            if i  > threshold :
#                                total_end_negative_checks += 1
#
#
#                        elif y == -1:
#                            #correct negative prediction, leave classifier alone and decrease p
#                            self.current_p = 0.9*self.current_p + 0.001
#
#                else:
#                    if np.random.binomial(1,self.p) == 1:
#                        y = PromptUser(paper)
#                        total_negative_checks += 1
#                        if i  > threshold :
#                            total_end_negative_checks += 1
#
#        for paper in chosen_papers:
#            print paper.id
#
#            #If prediction is 1, present paper, make update
#            #Else if predition is -1, make k
#            #If k=1 present abstract, make update
#            #If k=0 don't
#
#
#        out_file = open(str(user_name) + "customlabels.pkl","wb")
#        cPickle.dump(label_list,out_file)
#
#
#    def CheckAbstract(x, label)
#        """ Receive data and label for one abstract, make prediction 
#        """
#
#
#        #for i in range(len(data)):
#            x = data[i]
#            y_hat = classifier.Predict(x)
#            if y == 1 and y_hat == 1:
#                if i > threshold:
#                    n_pos_right += 1
#            elif y == -1 and y_hat == -1:
#                #update total_negative_checks count if we had to check, 
#                # and for adaptive p, update value of current_p
#                if self.p == 'adaptive':
#                    #got it correct, reduce p towards 0.01, our minimum
#                    #print "current p is", self.current_p
#                    if np.random.binomial(1,self.current_p) == 1:
#                        self.current_p = 0.9*self.current_p + 0.001
#                        total_negative_checks += 1
#                        if i  > threshold :
#                            total_end_negative_checks += 1
#                else:
#                    if np.random.binomial(1,self.p) == 1:
#                        total_negative_checks += 1
#                        if i  > threshold :
#                            total_end_negative_checks += 1
#
#            elif y_hat == 1 and y == -1:
#                #update on false positive, add one to n_wrong
#                if i > threshold:
#                    n_precision_wrong += 1
#                classifier.Update(x,y_hat,y)
#            else:
#                #maybe update on false negative, depends on p.
#                if i > threshold:
#                    n_recall_wrong += 1
#                if self.p == 'adaptive':
#                    # got it wrong, move current_p toward 1.0
#                    # to check more frequently
#                    #print "current p is", self.current_p
#                    k = np.random.binomial(1,self.current_p)
#                    if k == 1:
#                        total_negative_checks += 1
#                        if i  > threshold :
#                            total_end_negative_checks += 1
#                        classifier.Update(x,y_hat,y)
#                        self.current_p = 0.55*self.current_p + 0.4
#                else:
#                    k = np.random.binomial(1,self.p)
#                    if k == 1:
#                        total_negative_checks += 1
#                        if i  > threshold :
#                            total_end_negative_checks += 1
#                        classifier.Update(x,y_hat,y)
    def SavePaper(self,paper,date):
        """ Save paper to folder"""

        urllib.urlretrieve("https://www.arxiv.org/pdf/" + paper.id + ".pdf","./"+ self.name + "/" + date + "/" + paper.title + ".pdf")
        
        return
        

def UpdateArxivers(arxiver_dict):
    """ function to prompt the user to update Arxivers from the dictionary of arxivers created. """
    
    keep_updating = True
    while keep_updating:
        print "Please Select an Arxiver to update."
        for name in arxiver_dict:
            print name
        ans = raw_input("")
        if ans in arxiver_dict:
            arxiver_dict[ans].CheckDaysPapers('2014-05-15')
    
        again = raw_input( "Would you like to update another Arxiver?(y/n)")
        if again in ["no","No","NO","n","0"]:
            keep_updating = False
        

    return


if __name__ == "__main__":
    #script to use arxiver 

    #load arxiver dict if it's been created
    if os.path.exists("./arxiver_dict.pkl"):
        with open("./arxiver_dict.pkl","rb") as in_file:
            arxiver_dict = cPickle.load(in_file)
        ans = raw_input('Do you want to create a new Arxiver or update a current one? Please enter "update" or "new"')

    else:
        print "No Arxivers found."
        arxiver_dict = dict()
        ans = "new"

    answered = False
    while not answered:
        if ans == "update":
            UpdateArxivers(arviver_dict)
            answered = True
        elif ans == "new":
            # create a new arxiver then update it.  Use majority vote classifier and adaptive p hardcoded for now.
            answered = True
            classifier = MakeWeightedMajorityClassifier()
            new_arxiver = Arxiver(classifier,'adaptive')
            
            new_arxiver.SetUp()
            new_arxiver.CheckDaysPapers('2014-05-15')
            print "Saving Arxiver."
            print new_arxiver.name
            arxiver_dict[new_arxiver.name] = new_arxiver

        else:
            ans = raw_input('Please enter either "update" or "new"')

    with open("./arxiver_dict.pkl","wb") as out_file:
        cPickle.dump(arxiver_dict,out_file)
        
            
    
            
            

    
