"""Markov Chain"""
import random

class Markov():
    """Class for a markov chain model of arbitrary order
    
    Attributes:
        trained (Read-only[bool]): True if the model has been trained.
            training can be done on construction or later using the train method
        order (Read-only[int]): The order of the markov chain. A positive integer.
    """
    def __init__(self,training_list=None,order=1):
        """
        
        Args:
            training_list: must be a sequence containing only immutable objects
                e.g. a list of strings, a list of numbers etc. The objects need to
                be immutable because they are used as keys in the dict that stores
                the learned model. Note that a string is a sequence of characters and can be used for
                this argument.
            order (int): Defines the order of the markov chain. Defaults to 1.
        """
        
        self.order = order
        
        if training_list != None:
            self._train(training_list)
            self.trained = True
        else:
            self.trained = False
            
    def train(self,training_list=None):
        """Train the markov chain using a sequence.
    
        Args:
            training_list: See __init__. If training_is not supplied or None
                this method does nothing.
        """
        if training_list != None:
            self._train(training_list)
            self.trained = True
    
    def _train(self,training_list):
        """Non-public helper function for training."""
        self._state_trans_dict = {}
        order = self.order
        for i in range(order,len(training_list)):
            key = tuple(training_list[i-order:i])
            if key in self._state_trans_dict:
                self._state_trans_dict[key].append(training_list[i])
            else:
                self._state_trans_dict[key] = [training_list[i]]
    
    def generate(self,seed,length=24):
        """Generate a list of length elements based on the markov chain model.
        
        Args:
            seed: An iterable that supplies the starting sequence. Needs to be
                at least as long as the order of the chain. Can be a string.
            length: The desired length of the list to generate
        """
        order = self.order
        
        output_list = list(seed)
        for i in range(len(seed),length):
            key = tuple(output_list[i-order:i])
            output_list.append(random.choice(self._state_trans_dict[key]))
        return output_list
            
def main():
    file = open('chaucer.txt', 'r')
    text = file.read()
    file.close()
    
    mc = Markov(text,6)

    output_text = ''
    for char in mc.generate('For though',140):
        output_text = output_text + char
    print(output_text)
    
if __name__ == '__main__': #This snippet lets you import without executing
    main()