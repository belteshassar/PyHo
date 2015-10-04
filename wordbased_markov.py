"""This file contains an example for how to use the Markov class for
creating a word-based Markov chain instead of character-based as you
get if you feed a string as the training set to the Markov class.
The Markov class can take a list as the training set and uses the
elements of the list as the basic unit. By splitting the Chaucer text
to a list of words using the string.split() function we can achieve this.
"""

from markov import Markov
import string

def main():
    file = open('chaucer.txt', 'r')
    text = file.read()
    file.close()
    
    words = string.split(text)
    
    mc = Markov(words,3)

    output_text = ''
    for word in mc.generate(length=140):
        output_text = output_text + ' ' + word
    print(output_text)
    
if __name__ == '__main__': #This snippet lets you import without executing
    main()