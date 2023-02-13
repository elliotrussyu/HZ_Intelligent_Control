# Author: Hanshu Yu
# Last update: 04-02-2023
# All rights reserved.

import string
import sys

ENG_CHR_RANK = 'etaoinsrhdlucmfywgpbvkxqjz'
FREQ_RANK = [12.02,9.10,8.12,7.68,7.31,6.95,
            6.28,6.02,5.92,4.32,3.98,2.88,
            2.71,2.61,2.30,2.11,2.09,2.03,
            1.82,1.49,1.11,0.69,0.17,0.11,
            0.10,0.07]
TOT_STAT = zip(ENG_CHR_RANK,FREQ_RANK)
ENG_FREQ = {i:j/100 for i,j in TOT_STAT}

def clean(rawtxt):
    """
    This function picks all alphabet characters of the input string and transfer them to all lower case
    """
    return "".join([c for c in rawtxt.lower() if c.isalpha()])

class ShiftCrypto: 
    
    alphabet = string.ascii_lowercase
    alphanum = len(alphabet)
    
    def encdec(self, intxt, key, mode):
        """
        This function performs the enc/dec for the shift cipher.
        mode could be either 'enc' or 'dec'
        """
        if mode not in ('enc','dec'):
            raise SyntaxError('Wrong mode!')
        if mode == 'dec':
            key *= -1 #Shift left when dec
        outtxt = ''
        mapping = {c:self.alphabet[(i+key)%self.alphanum] 
                   for i,c in enumerate(self.alphabet)} #generates an alphabet map between ciphertxt and plaintxt, 
                                                        #such that later we can just look up the map when we process our input str
        for char in intxt.lower(): 
            if char not in mapping.keys(): #If the character is not supposed to be altered by enc/dec then we keep it as it is in the mapping
                mapping[char] = char #Mapping itself to itself, no change at all
            outtxt += mapping[char]
        return outtxt
    
    def keyfinder(self,rawtxt):
        """
        This function finds the key from the inputted shifted ciphertext, outputs the most likely key
        """
        loweralphatxt = clean(rawtxt)
        tot_char = len(loweralphatxt)
        freq_alpha_seq = [num/100 for num in list(zip(*sorted(list(zip(ENG_CHR_RANK,FREQ_RANK)))))[1]]
        OUR_FREQ = [loweralphatxt.count(c)/tot_char for c in self.alphabet]
        tot_rec = [ # tot_rec records the statistical difference in the format of a list with tuples 
                    ( 
                    sum([abs(freq_alpha_seq[j] - OUR_FREQ[(i+j)%self.alphanum])
                         for j in range(self.alphanum)]) #The statistical difference for each shift i
                    ,i                             #Recording the potential key i
                    ) #Construct tuples with 2 elements (statistical difference, corresponding shift)
                    for i in range(self.alphanum)]
        return sorted(tot_rec)[0][1] # Sort by statistical difference, 
                                    # get the second element (the most likely shift key) 
                                    # of the first tuple (the tuple with smallest statistical difference) in the list tot_rec

if __name__ == '__main__':
    tool = ShiftCrypto()
    while 1:
        selection = input('Select mode: \n1: encrypt\n2: decrypt\n3: hack\n0: exit\n')

        if not int(selection):
            break
        if selection not in ('1','2','3'):
            print('Faulty input')
            continue

        # rawtxt = input('Input text:\n')
        print('Input text: Indicate the end of your input by pressing ctrl+Z then press enter to confirm\n(If ctrl+Z and enter does not work, try ctrl+D and enter)\nInput text:')
        rawtxt = sys.stdin.read()
        if selection == '1':
            key = int(input('Input key:  '))
            print('ciphertxt:\n',tool.encdec(rawtxt,key,'enc'))
        if selection == '2':
            key = int(input('Input key:  '))
            print('plaintxt:\n',tool.encdec(rawtxt,key,'dec'))
        if selection == '3':
            key = tool.keyfinder(rawtxt)
            print('key:  ', key)
            print('ciphertxt:\n',tool.encdec(rawtxt,key,'dec'))

    print('Program exit according to user input')