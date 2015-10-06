"""Markov Chain for generating lists of any immutable objects. Typical use case is text,
but it is not limited to this. The supplied main() example reads a text file containing
an excerpt from The Canterbury Tales (chaucer.txt) and generates a Markov Chain based on
it. The Markov Chain is of order 6 and the basic unit is a character. It is possible to
use the supplied class for creating Markov chains with words as the basic unit as well.
Any choice of order is supported so feel free to play around.

The order defines how many previous characters should be looked at when deciding which
one should follow. Higher order gives more coherent text, but make the order too high
and you will just copy large swaths of the original. You can try with other sources as
well and see what works well. It is really the quality of the source material that
defines the quality of the output. Generally, the source should be as large as possible,
but since my code keeps the generated model in memory it can't handle too large datasets.
This could be improved by storing the model in a database."""
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
                the learned model. Note that a string is a sequence of characters
                and can be used for this argument. A list may also be given. If a
                string is given, the resulting Markov Chain will use characters as
                the basic unit. If a list is given, the elements of the list (e.g. words)'
                will be the basic unit.
            order (int): Defines the order of the markov chain. Defaults to 1.
        """
        
        self.order = order
        self._state_trans_dict = {}
        
        if training_list != None:
            self._train(training_list)
            self.trained = True
        else:
            self.trained = False
            
    def train(self,training_list=None):
        """Train the markov chain using a sequence. The train function can be called
        multiple times if necessary. The learned data will be retained. This way multiple
        samples can be used.
    
        Args:
            training_list: See __init__. If training_is not supplied or None
                this method does nothing.
        """
        if training_list != None:
            self._train(training_list)
            self.trained = True
    
    def _train(self,training_list):
        """Non-public helper function for training."""
        
        order = self.order
        for i in range(order,len(training_list)):
            key = tuple(training_list[i-order:i])
            if key in self._state_trans_dict:
                self._state_trans_dict[key].append(training_list[i])
            else:
                self._state_trans_dict[key] = [training_list[i]]
    
    def generate(self,seed=None,length=24):
        """Generate a list of length elements based on the markov chain model.
        
        Args:
            seed: An iterable that supplies the starting sequence. Needs to be
                at least as long as the order of the chain. Can be a string. If
                seed is None or not supplied than a random key of self._state_trans_dict
                will be used as seed.
            length: The desired length of the list to generate
        
        Returns:
            list: Genrated sequence of length 'length'.
        """
        order = self.order
        
        if seed == None or len(seed) < order:
            seed = random.choice(list(self._state_trans_dict.keys()))
        elif not tuple(seed[-order:]) in self._state_trans_dict:
            seed = random.choice(list(self._state_trans_dict.keys()))
        
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
    for char in mc.generate(length=140):
        output_text = output_text + char
    print(output_text)
    
if __name__ == '__main__': #This snippet lets you import without executing
    main()