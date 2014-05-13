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
from WeightedMajority import WeightedMajorityClassifier
from WeightedMajority import MakeWeightedMajorityClassifier
from ClassifierTester import ClassifierTester



def AddBarToPlot(cln, max_recall, max_precision, r_neg_updates, p_neg_updates, k):
    """' helper function to add a bar to barplot 2k and 2k+1 , 
    inputs:
            cln - classifier number, from test script
            max_recall - best recall achieved by classifier
            max_precision - best precision achieved by classifier
            k - user name number.
            """
    
    if p == 1.0:
        offset = 0
        plot_clr = "blue"
    elif p == 0.1:
        offset = 0.2
        plot_clr = "red"
    elif p == 'adaptive':
        offset = 0.4
        plot_clr = "green"

    pyplot.figure(2*k)
    pyplot.subplot(211)
    if cln == 0:
        pyplot.bar(cln + offset,max_recall,label = "p = " + str(p),width=0.2, color=plot_clr)
    else:
        pyplot.bar(cln + offset,max_recall,width=0.2, color=plot_clr)

    pyplot.subplot(212)
    if cln == 0:
        pyplot.bar(cln + offset,r_neg_updates,label = "p = " + str(p),width=0.2, color=plot_clr)
    else:
        pyplot.bar(cln + offset,r_neg_updates,width=0.2, color=plot_clr)

    pyplot.figure(2*k + 1)
    pyplot.subplot(211)
    if cln == 0:                    
        pyplot.bar(cln + offset,max_precision,label="p = " + str(p), width=0.2, color=plot_clr)
    else:
        pyplot.bar(cln + offset,max_precision, width=0.2, color=plot_clr)

    pyplot.subplot(212)
    if cln == 0:
        pyplot.bar(cln + offset,p_neg_updates,label = "p = " + str(p),width=0.2, color=plot_clr)
    else:
        pyplot.bar(cln + offset,p_neg_updates,width=0.2, color=plot_clr)

    return


def BestParams(grid, neg_updates):
    """ find the best values of parameters from the recall on a grid of parameters.  Also report the number of
    negative updates needed for those values of parameters
    inputs:  
            grid - dict of either recall or precision from a single classifier, 1 entry for each set of parameters tested
            neg_updates - dict of negative updates required for each set of parameters.  The keys here match the keys of grid
           
    outputs:
           best_param        - set of parameters that gave the maximum value in grid
           best_value        - maximum value found in grid (recall or precision)
           best_neg_udpdates - number of negative updates needed by 
                               classifier using best_param for parameters
"""
    
    best_value = 0.
    best_param = None
    best_neg_updates = 0
    #go through all parameters tested by this object, and return
    # the parameters that gave the best recall
    for param in grid:
        if grid[param] > best_value:
            best_value = grid[param]
            best_param = param
            best_neg_updates = neg_updates[param]

    return best_param, best_value, best_neg_updates


#Begin Script here:
if __name__ == "__main__":
#names of people who contributed labels
    names = ["steven","joey","sid","iantobasco","manas","travis"]
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
    cs = [0.0, 0.03125, 0.0625]
    ds = [1, 2, 3, 4]
    
    #liss of classifiers and their names
    classifier_list = [MakePerceptronClassifier, MakeMarginPerceptronClassifier,MakeOnlineSVMClassifier,MakeGaussianKernelPerceptronClassifier, MakePolynomialKernelPerceptronClassifier, MakeWeightedMajorityClassifier]
    classifier_names = ["Perceptron","Margin Perceptron","Online SVM","Gaussian Kernel Perceptron","Polynomial Kernel Perceptron", "Weighted Majority Classifier"]

    #set up empty lists for labels on bar graphs
    # add entry for "__everyone__" to aggregate
    classifier_r_labels = dict()
    for name in names:
        classifier_r_labels[name] = range(len(classifier_names))
    classifier_r_labels["__everyone__"] = range(len(classifier_names))
    classifier_p_labels = dict()
    for name in names:
        classifier_p_labels[name] = range(len(classifier_names))
    classifier_p_labels["__everyone__"] = range(len(classifier_names))

    param_r_labels = dict()
    for name in names:
        param_r_labels[name] = range(len(classifier_names))
    param_r_labels["__everyone__"] = range(len(classifier_names))
    param_p_labels = dict()
    for name in names:
        param_p_labels[name] = range(len(classifier_names))
    param_p_labels["__everyone__"] = range(len(classifier_names))


    #set up parameters and their names                                      
    parameters_list = [etas, rhos, Cs, sigmas, [cs, ds], [rhos, Cs]]
    parameter_names = [["eta"],["rho"],["C"],["sigma"],["c","d"], ["rho","C"]]
    nparams_list = [1, 1, 1, 1, 2, 2]
                      
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
                recall_grid, precision_grid, neg_updates = classifier_tester.ReportGrid()
                
                #set up grid from gridsearch that aggregates over all names:
                #if it's the first name, make the grid
                if k == 0:
                    total_recall_grid = recall_grid
                    total_precision_grid = precision_grid
                    total_neg_update_grid = neg_updates
                    total_product_grid = dict()
                    for param in recall_grid:
                        total_product_grid[param] = recall_grid[param]*precision_grid[param]
                else:
                    #add values to grids for aggregating
                    for param in recall_grid:
                        total_recall_grid[param] += recall_grid[param]
                        total_precision_grid[param] += precision_grid[param]
                        total_neg_update_grid[param] += neg_updates[param]
                        total_product_grid[param] += recall_grid[param]*precision_grid[param]
                        
                best_r_params, max_recall, r_neg_updates = classifier_tester.ReportBestRecall()

                best_p_params, max_precision, p_neg_updates = classifier_tester.ReportBestPrecision()
                
                AddBarToPlot(cln, max_recall, max_precision, r_neg_updates, p_neg_updates, k)

                if p == 1.0:
                    classifier_r_labels[name][cln] = classifier_names[cln]# + "\n Neg updates: " + str(r_neg_updates)
                    param_r_labels[name][cln] = "\n params: " + str(best_r_params)
                    classifier_p_labels[name][cln] = classifier_names[cln]# + "\n Neg updates: " + str(p_neg_updates)
                    param_p_labels[name][cln] = "\n params: " + str(best_p_params)
                else:
#                    classifier_r_labels[name][cln] += ", " + str(r_neg_updates)
                    param_r_labels[name][cln] += ", " + str(best_r_params)
#                    classifier_p_labels[name][cln] += ", " + str(p_neg_updates)
                    param_p_labels[name][cln] += ", " + str(best_p_params)
    
            
            #normalize total grids
            for param in total_recall_grid:
                total_recall_grid[param] = total_recall_grid[param]/len(names)
                total_precision_grid[param] = total_precision_grid[param]/len(names)
                total_neg_update_grid[param] = total_neg_update_grid[param]/len(names)
                    
            #find best parameters, and corresponding neg updates
            best_r_params, max_recall, r_neg_updates = BestParams(total_recall_grid, total_neg_update_grid)
            best_p_params, max_precision, p_neg_updates = BestParams(total_precision_grid, total_neg_update_grid)

            #add to bar plot
            AddBarToPlot(cln, max_recall, max_precision, r_neg_updates, p_neg_updates, len(names))

    #title, label, and save plots
    for k in range(len(names)):
        pyplot.figure(2*k)
        pyplot.subplot(211)
        pyplot.title("Recall for " + names[k])
        #append information about parameters to labels
        for l in range(len(classifier_names)):
            classifier_r_labels[names[k]][l] = classifier_r_labels[names[k]][l] + param_r_labels[names[k]][l]
#        pyplot.xticks(range(len(classifier_names)),classifier_r_labels[names[k]],rotation=35,fontsize=8)
        pyplot.xticks([],[])
        pyplot.gcf().subplots_adjust(bottom=0.20)
        pyplot.ylim([0,0.6])
        pyplot.legend(loc="best",prop={"size":10})
        pyplot.subplot(212)
        pyplot.title("Number of Negative Updates")
        pyplot.xticks(range(len(classifier_names)),classifier_names, rotation = 35, fontsize=9)
        pyplot.savefig("./" + names[k] + "Recall.pdf")

        pyplot.figure(2*k + 1)
        pyplot.subplot(211)
        pyplot.title("Precision for " + names[k])
        #append information about parameters to labels
        for l in range(len(classifier_names)):
            classifier_p_labels[names[k]][l] = classifier_p_labels[names[k]][l] + param_p_labels[names[k]][l]
#        pyplot.xticks(range(len(classifier_names)),classifier_p_labels[names[k]], rotation = 35, fontsize=9)
#        pyplot.xticks(range(len(classifier_names)),classifier_names, rotation = 35, fontsize=9)
        pyplot.xticks([],[])
        pyplot.gcf().subplots_adjust(bottom=0.20)
        pyplot.ylim([0,0.6])
        pyplot.legend(loc="best",prop={"size":10})
        pyplot.subplot(212)
        pyplot.title("Number of Negative Updates")
        pyplot.xticks(range(len(classifier_names)),classifier_names, rotation = 35, fontsize=9)
        pyplot.savefig("./" + names[k] + "Precision.pdf")



#title, label, and save plots
pyplot.figure(2*len(names))
pyplot.subplot(211)
pyplot.title("Recall Aggregated over Users")
#append information about parameters to labels
#for l in range(len(classifier_names)):
#    classifier_r_labels[names[k]][l] = classifier_r_labels[names[k]][l] + param_r_labels[names[k]][l]
#pyplot.xticks(range(len(classifier_names)),classifier_names, rotation = 35, fontsize=9)
pyplot.xticks([],[])
pyplot.gcf().subplots_adjust(bottom=0.20)
pyplot.ylim([0,0.6])
pyplot.legend(loc="best",prop={"size":10})
pyplot.subplot(212)
pyplot.title("Number of Negative Updates")
pyplot.xticks(range(len(classifier_names)),classifier_names, rotation = 35, fontsize=9)
pyplot.savefig("./EveryoneRecall.pdf")

pyplot.figure(2*len(names) + 1)
pyplot.subplot(211)
pyplot.title("Precision Aggregated over Users")
#append information about parameters to labels
#for l in range(len(classifier_names)):
#    classifier_p_labels[names[k]][l] = classifier_p_labels[names[k]][l] + param_p_labels[names[k]][l]
#pyplot.xticks(range(len(classifier_names)),classifier_names, rotation = 35, fontsize=9)
pyplot.xticks([],[])
pyplot.gcf().subplots_adjust(bottom=0.20)
pyplot.ylim([0,0.6])
pyplot.legend(loc="best",prop={"size":10})
pyplot.subplot(212)
pyplot.title("Number of Negative Updates")
pyplot.xticks(range(len(classifier_names)),classifier_names, rotation = 35, fontsize=9)
pyplot.savefig("./EveryonePrecision.pdf")


    
    


    
                    
