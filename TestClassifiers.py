from ArxivData import FeaturizeAbstracts
from ArxivData import GetAbstracts
import random
import numpy as np
import cPickle
from ArxivData import Paper
from ArxivData import PromptUser
from OnlineSVM import OnlineSVMClassifier
from OnlineSVM import MakeOnlineSVMClassifier
from Perceptron import PerceptronClassifier
from Perceptron import MakePerceptronClassifier
from Perceptron import MarginPerceptronClassifier
from Perceptron import MakeMarginPerceptronClassifier
from ClassifierTester import ClassifierTester



#Begin Script here:
if __name__ == "__main__":
#names of people who contributed labels
    names = ["steven","sid","iantobasco","joey","manas","travis"]
    custom_data_dict = {'steven' : 'stevenCustomTestData.pkl', 'joey' : 'joeynewCustomTestData.pkl'}
    custom_label_dict = {'steven' : 'stevencustomlabels.pkl', 'joey' : 'joeynewcustomlabels.pkl'}
    
#get data
    data_filename = "./OfficialTestData.pkl"
    data_file = open(data_filename,"rb")
    paper_list = cPickle.load(data_file)
    abstracts = GetAbstracts(paper_list)
    abstract_vectors = FeaturizeAbstracts(abstracts)
    
    etas = [1.0]
    rhos = [2**(-7),2**(-6),2**(-5),2**(-4),2**(-3),2**(-2)]
    Cs = [2**(-6),2**(-5),2**(-4),2**(-3),2**(-2), 2**(-1), 1.0, 2.0, 4.0, 8.0, 16.0, 32.0]
    classifier_list = [MakePerceptronClassifier, MakeMarginPerceptronClassifier,MakeOnlineSVMClassifier]
    parameters_list = [etas, [etas,rhos], [etas,Cs]]
    nparams_list = [1, 2, 2, 2]
                      
    
#go through all classifiers to test
    for cln in range(len(classifier_list)):
        
        for p in [1.0, 0.1, 'adaptive']:
            print "P value is: ", p
        #go through labeled data a few times, 
            for name in names:
                print "User: ", name
                #create classifier tester
                classifier_tester = ClassifierTester(classifier_list[cln],parameters_list[cln],nparams_list[cln],p)

            #get labels
                label_filename = name + "labels.pkl"
                label_file = open(label_filename,"rb")
                labels = cPickle.load(label_file)
                
            #get extra data and labels
                if name in custom_data_dict:
                    custom_data_file_name = custom_data_dict[name]
                    custom_label_file_name = custom_label_dict[name]
                    
                    with open(custom_data_file_name,"rb") as custom_data_file:
                        custom_paper_list = cPickle.load(custom_data_file)
                        custom_abstracts = GetAbstracts(custom_paper_list)
                        custom_abstract_vectors = FeaturizeAbstracts(custom_abstracts)
                        current_data = abstract_vectors + custom_abstract_vectors
                        
                    with open(custom_label_file_name,"rb") as custom_label_file:
                        custom_labels = cPickle.load(custom_label_file)
                        current_labels = labels + custom_labels
                            
                else:
                    current_data = abstract_vectors
                    current_labels = labels
                    
            #shuffle custom and regular data together
                packaged_data = [(current_data[i],current_labels[i]) for i in range(len(current_data))]
                random.seed(1)
                random.shuffle(packaged_data)
                    
                for i in range(len(packaged_data)):
                    current_data[i] = packaged_data[i][0]
                    current_labels[i] = packaged_data[i][1]


                classifier_tester.Test(current_data,current_labels)
                classifier_tester.ReportGrid()
                        
                #initialize counts for accuracy
#                n_pos_right = 0
#                n_precision_wrong = 0
#                n_recall_wrong = 0
#                for i in range(len(current_data)):
#            
#                    x = current_data[i]
#                    y_hat = classifier.Predict(x)
#                    y = current_labels[i]
#                    if y == 1 and y_hat == 1:
#                        n_pos_right += 1
#                    elif y == -1 and y_hat == -1:
#                    #do nothing, doesn't count as positive correct
#                        pass
#                    elif y_hat == 1:
#                        #update on false positive, add one to n_wrong
#                        n_precision_wrong += 1
#                        classifier.Update(x,y_hat,y)
#                    else:
#                    #maybe update on false negative, depends on p.
#                        n_recall_wrong += 1
#                        k = np.random.binomial(1,p)
#                        if k == 1:
#                            classifier.Update(x,y_hat,y)
#                        
#
#                print "User: ", name
#                print "Total preferred papers: ", n_pos_right + n_recall_wrong
#                if n_pos_right != 0:
#                    print "Recall: ", float(n_pos_right)/float(n_pos_right + n_recall_wrong)
#                    print "Precision: ", float(n_pos_right)/float(n_pos_right + n_precision_wrong)
#                else:
#                    print "Recall: ", 0.0
#                    print "Precision: ", 0.0
#                
#                print "-"*80
                                
                    
                
        
        
    
        
    
    




    
