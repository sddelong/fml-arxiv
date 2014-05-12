import random
import numpy as np


class ClassifierTester:
    """ Used to test any of the classifiers we use for abstract classification. """
    
    def __init__(self,classifier_creator,gridsearch_parameters,n_params,p):
        
        self.n_params = n_params
        if self.n_params not in [1, 2]:
            print "number of parameters must be 1 or 2"
            raise NotImplementedError
        self.classifier_creator = classifier_creator
        self.p = p
        if self.p == 'adaptive':
            self.current_p = 1.0

        self.gridsearch_parameters = gridsearch_parameters

        self.recall_grid = dict()
        self.precision_grid = dict()

        
    def Test(self,data,labels):
        
        #setup parameters for gridsearch
        if self.n_params == 1:
            parameters_list = [[p] for p in self.gridsearch_parameters]
        elif self.n_params == 2:
            parameters_list = [[x,y] for x in self.gridsearch_parameters[0] for y in self.gridsearch_parameters[1]]

        for params in parameters_list:
            
            #create classifier
            classifier = self.classifier_creator(params)
            
            #initialize counts for accuracy
            n_pos_right = 0
            n_precision_wrong = 0
            n_recall_wrong = 0
            total_negative_checks = 0
            for i in range(len(data)):
            
                x = data[i]
                y_hat = classifier.Predict(x)
                y = labels[i]
                if y == 1 and y_hat == 1:
                    n_pos_right += 1
                elif y == -1 and y_hat == -1:
                    #update total_negative_checks count if we had to check, 
                    # and for adaptive p, update value of current_p
                    if self.p == 'adaptive':
                        #got it correct, reduce p towards 0.01, our minimum
                        if np.random.binomial(1,self.current_p) == 1:
                            self.current_p = 0.9*self.current_p + 0.001
                            total_negative_checks += 1
                    else:
                        if np.random.binomial(1,self.p) == 1:
                            total_negative_checks += 1

                elif y_hat == 1:
                    #update on false positive, add one to n_wrong
                    n_precision_wrong += 1
                    classifier.Update(x,y_hat,y)
                else:
                    #maybe update on false negative, depends on p.
                    n_recall_wrong += 1
                    if self.p == 'adaptive':
                        # got it wrong, move current_p toward 1.0
                        # to check more frequently
                        k = np.random.binomial(1,self.current_p)
                        if k == 1:
                            total_negative_checks += 1
                            classifier.Update(x,y_hat,y)
                            self.current_p = 0.4*self.current_p + 0.6
                    else:
                        k = np.random.binomial(1,self.p)
                        if k == 1:
                            total_negative_checks += 1
                            classifier.Update(x,y_hat,y)

                    
            print "Total Negative Checks: ", total_negative_checks
            if n_pos_right != 0:
                self.recall_grid[self._ParamsToString(params)] = float(n_pos_right)/float(n_pos_right + n_recall_wrong)
                self.precision_grid[self._ParamsToString(params)] = float(n_pos_right)/float(n_pos_right + n_precision_wrong)
            else:
                self.recall_grid[self._ParamsToString(params)] = 0.0
                self.precision_grid[self._ParamsToString(params)] = 0.0

    def ReportGrid(self):
        
        if self.n_params == 1:
            classifier = self.classifier_creator([0.0])
            print classifier.name
            parameters_list = [[p] for p in self.gridsearch_parameters]
            print "        Recall Grid:            "
            print "-"*60
            print_str = ""
            for p in self.gridsearch_parameters:
                print_str +=  str(p) +  "    | "
            print print_str
            print_str = ""
            for param in parameters_list:
                print_str += "%1.4f" % (self.recall_grid[self._ParamsToString(param)]) + " | "
            print print_str
            print "-"*60
            print "\n"

            print "        Precision Grid:            "
            print "-"*60
            print_str = ""
            for p in self.gridsearch_parameters:
                print_str += str(p) +  "    | "
            print print_str
            print_str = ""
            for param in parameters_list:
                print_str += "%1.4f" % (self.precision_grid[self._ParamsToString(param)]) + " | "
            print print_str
            print "-"*60
            print "\n"
            
        elif self.n_params == 2:
            classifier = self.classifier_creator([0.0, 0.0])
            print classifier.name
            print "        Recall Grid         "
            print "-"*60
            print_str = "       | "
            for p in self.gridsearch_parameters[0]:
                print_str += str(p) + "    | "
            print print_str
            print_str = ""
            print "-"*50
            for p2 in self.gridsearch_parameters[1]:
                print_str +=  "%1.3f" % p2 +  "  || "
                for p1 in self.gridsearch_parameters[0]:
                    print_str += "%1.4f" % (self.recall_grid[self._ParamsToString([p1,p2])]) + " | "
                print print_str
                print_str = ""
            print "-"*60


            print "        Precision Grid         "
            print "-"*60
            print_str = "       | "
            for p in self.gridsearch_parameters[0]:
                print_str += str(p) + "    | "
            print print_str
            print_str = ""
            print "-"*50
            for p2 in self.gridsearch_parameters[1]:
                print_str +=  "%1.3f" % p2 +  "  || "
                for p1 in self.gridsearch_parameters[0]:
                    print_str += "%1.4f" % (self.precision_grid[self._ParamsToString([p1,p2])]) + " | "
                print print_str
                print_str = ""
            print "-"*60

                
            return


    def ReportBest(self):
        """ Report best classifier """
    

    def _ParamsToString(self,params):
        """ helper function to turn params into a 
        string for use as a dict key
        """

        p_str = ""
        for p in params:
            p_str += str(p) + ", "
                
        return p_str
                
            
                  