import numpy as np


def sign(x):
    """ compute sign of x, with convention that 0 is positive """
    if x >= 0:
        return 1
    else:
        return -1



class PerceptronClassifier:
    """ Simple perceptron algorithm for online learning. """
    
    def __init__(self,n,eta):
        """ Constructor for Perceptron. 

           Arguments:
                   eta - learning rate
                   n - length of input data. (We may want to do this differently
                            to be specific to bags of words)
        """
        
        self.eta = eta
        self.weights = np.zeros(n)
        self.n_correct = 0
        self.n_wrong = 0
        
        
    def Update(self,x,y_hat,y):
        """ given that the Perceptron has guessed y_hat for data x, update it 
        using the correct value y.

        Note: must be used after every prediction to obtain a correct accuracy estimate
        """
        
        if y_hat != y:
            #update
            self.n_wrong += 1
            self.weights = self.weights + self.eta*y*x
        else:
            self.n_correct += 1
        
        return
        

    def Predict(self,x):
        """ predict y by using sign of a dot product of x with weights """
        
        return sign(np.dot(self.weights,x))


    def ReportAccuracy(self):
        
        return float(self.n_correct)/float(self.n_wrong + self.n_correct)


if __name__ == "__main__":
    

    x = np.ones(10)
    pclassifier = Perceptron(10,0.3)
    
    y_hat = pclassifier.Predict(x)
    
    assert y_hat == 1, "y_hat should be 1 at initialization, it is not"
    
    pclassifier.Update(x,y_hat,-1)
    y_hat_2 = pclassifier.Predict(x)
    
    assert y_hat_2 == -1, "y_hat should be -1 after update, it is not"
    
    
    print "Completed some basic tests"




        

        
           
        
