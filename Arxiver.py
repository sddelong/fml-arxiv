import ArxivSubjects as arxs
from ArxivData import GetPapersOAI


class Arxiver:
    
    def __init__(self,classifier):

        self.classifier = classifier
        self.subjects = None
        self.subcategories = None
        
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

        paper_list = getPapersOAI()
        
        
        
        
    
    

                    

                
