import random
import numpy as np
import cPickle
from matplotlib import pyplot
from ArxivData import FeaturizeAbstracts
from ArxivData import GetAbstracts
from ArxivData import Paper
from ArxivData import PromptUser
from OnlineSVM import OnlineSVMClassifier
from OnlineSVM import MakeOnlineSVMClassifier
from Perceptron import PerceptronClassifier
from Perceptron import MakePerceptronClassifier
from Perceptron import MarginPerceptronClassifier
from Perceptron import MakeMarginPerceptronClassifier
from Perceptron import MakeGaussianKernelPerceptronClassifier
from Perceptron import MakePolynomialKernelPerceptronClassifier
from Perceptron import KernelPerceptronClassifier
from ClassifierTester import ClassifierTester



#Begin Script here:
if __name__ == "__main__":
#names of people who contributed labels
    names = ["steven","sid","iantobasco","joey","manas","travis"]
    custom_data_dict = {'steven' : 'stevenCustomTestData.pkl', 'joey' : 'joeynewCustomTestData.pkl','travis' : 'travisCustomTestData.pkl', }
    custom_label_dict = {'steven' : 'stevencustomlabels.pkl', 'joey' : 'joeynewcustomlabels.pkl', 'travis' : 'traviscustomlabels.pkl'}
    
#get data
    data_filename = "./OfficialTestData.pkl"
    data_file = open(data_filename,"rb")
    paper_list = cPickle.load(data_file)
    abstracts = GetAbstracts(paper_list)
    abstract_vectors = FeaturizeAbstracts(abstracts)
    
    #set up lists of parameters and classifiers for grid searches
    etas = [1.0]
    rhos = [2**(-8), 2**(-7),2**(-6),2**(-5)]
    Cs = [2**(-6),2**(-5),2**(-4),2**(-3),2**(-2), 2**(-1), 1.0, 2.0]
    sigmas = [0.01, 0.02, 0.04,0.2, 1.0]
    cs = [-0.0625, -0.03125, 0.0, 0.03125, 0.0625]
    ds = [1, 2, 3, 4]
    
    #liss of classifiers and their names
    classifier_list = [MakePerceptronClassifier, MakeMarginPerceptronClassifier,MakeOnlineSVMClassifier,MakeGaussianKernelPerceptronClassifier, MakePolynomialKernelPerceptronClassifier]
    classifier_names = ["Perceptron","Margin Perceptron","Online SVM","Gaussian Kernel Perceptron","Polynomial Kernel Perceptron"]


    #set up empty lists for labels on bar graphs
    classifier_r_labels = dict()
    for name in names:
        classifier_r_labels[name] = range(len(classifier_names))
    classifier_p_labels = dict()
    for name in names:
        classifier_p_labels[name] = range(len(classifier_names))

    param_r_labels = dict()
    for name in names:
        param_r_labels[name] = range(len(classifier_names))
    param_p_labels = dict()
    for name in names:
        param_p_labels[name] = range(len(classifier_names))


    #set up parameters and their names                                      
    parameters_list = [etas, rhos, Cs, sigmas, [cs, ds]]
    parameter_names = [["eta"],["rho"],["C"],["sigma"],["c","d"]]
    nparams_list = [1, 1, 1, 1, 2]
    
                      
#go through all classifiers to test
    for cln in range(len(classifier_list)):

        #go through values for p
        for p in [1.0, 0.1, 'adaptive']:
            print "P value is: ", p
            #go through users
            
            for k in range(len(names)):
                #use k to determine plots
                name = names[k]
                print "User: ", name

                #create classifier tester
                classifier_tester = ClassifierTester(classifier_list[cln],parameters_list[cln],nparams_list[cln],p,classifier_names[cln])

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

                print "total positives: ", sum(np.array(current_labels) == 1)
                print "total papers: ", len(current_data)

                classifier_tester.Test(current_data,current_labels)
                classifier_tester.ReportGrid()
                
                best_r_params, max_recall, r_neg_updates = classifier_tester.ReportBestRecall()

                best_p_params, max_precision, p_neg_updates = classifier_tester.ReportBestPrecision()
                
                
                
                
                if p == 1.0:
                    pyplot.figure(2*k)
                    if cln == 0:
                        pyplot.bar(cln,max_recall,label="p = 1.0",width=0.2, color="blue")
                    else:
                        pyplot.bar(cln,max_recall,width=0.2, color="blue")
                        
                    classifier_r_labels[name][cln] = classifier_names[cln] + "\n Neg updates: " + str(r_neg_updates)

                    param_r_labels[name][cln] = "\n params: " + str(best_r_params)

                    pyplot.figure(2*k + 1)
                    if classifier_names[cln] == "Perceptron":
                        pyplot.bar(cln,max_precision,label="p = 1.0",width=0.2, color="blue")
                    else:
                        pyplot.bar(cln,max_precision,width=0.2, color="blue")
                    classifier_p_labels[name][cln] = classifier_names[cln] + "\n Neg updates: " + str(p_neg_updates)
                    param_p_labels[name][cln] = "\n params: " + str(best_p_params)


                elif p == 0.1: 
                    # plot offset bars for p = 0.1
                    pyplot.figure(2*k)
                    if classifier_names[cln] == "Perceptron":
                        pyplot.bar(cln + 0.2,max_recall,label = "p = 0.1",width=0.2, color="red")
                    else:
                        pyplot.bar(cln + 0.2,max_recall,width=0.2, color="red")
                    classifier_r_labels[name][cln] += ", " + str(r_neg_updates)
                    param_r_labels[name][cln] += ", " + str(best_r_params)

                    pyplot.figure(2*k + 1)
                    if classifier_names[cln] == "Perceptron":                    
                        pyplot.bar(cln + 0.2,max_precision,label="p = 0.1", width=0.2, color="red")
                    else:
                        pyplot.bar(cln + 0.2,max_precision, width=0.2, color="red")
                    classifier_p_labels[name][cln] += ", " + str(p_neg_updates)
                    param_p_labels[name][cln] += ", " + str(best_p_params)



                elif p == 'adaptive':
                    pyplot.figure(2*k)
                    if classifier_names[cln] == "Perceptron":
                        pyplot.bar(cln + 0.4,max_recall,label = "p = adaptive",width=0.2, color="green")
                    else:
                        pyplot.bar(cln + 0.4,max_recall,width=0.2, color="green")
                    classifier_r_labels[name][cln] += ", " + str(r_neg_updates)
                    param_r_labels[name][cln] += ", " + str(best_r_params)

                    pyplot.figure(2*k + 1)
                    if classifier_names[cln] == "Perceptron":
                        pyplot.bar(cln + 0.4,max_precision,label = "p = adaptive",width=0.2, color="green")
                    else:
                        pyplot.bar(cln + 0.4,max_precision,width=0.2, color="green")
                    classifier_p_labels[name][cln] += ", " + str(p_neg_updates)
                    param_p_labels[name][cln] += ", " + str(best_p_params)

                    
    for k in range(len(names)):
        pyplot.figure(2*k)
        pyplot.title("Recall for " + names[k])

        #append information about parameters to labels
        for l in range(len(classifier_names)):
            classifier_r_labels[names[k]][l] = classifier_r_labels[names[k]][l] + param_r_labels[names[k]][l]
        pyplot.xticks(range(len(classifier_names)),classifier_r_labels[names[k]],rotation=35,fontsize=8)
        pyplot.gcf().subplots_adjust(bottom=0.20)
        pyplot.ylim([0,1])
        pyplot.legend(loc="best",prop={"size":10})
        pyplot.savefig("./" + names[k] + "Recall.pdf")

        pyplot.figure(2*k + 1)
        pyplot.title("Precision for " + names[k])
        #append information about parameters to labels
        for l in range(len(classifier_names)):
            classifier_p_labels[names[k]][l] = classifier_p_labels[names[k]][l] + param_p_labels[names[k]][l]
        pyplot.xticks(range(len(classifier_names)),classifier_p_labels[names[k]], rotation = 35, fontsize=9)
        pyplot.gcf().subplots_adjust(bottom=0.20)
        pyplot.ylim([0,1])
        pyplot.legend(loc="best",prop={"size":10})
        pyplot.savefig("./" + names[k] + "Precision.pdf")
            
                    
                    
                               
                

                
                
                        
                    
