# Author: Hanshu Yu (original), GUI enhancement
# Last update: Enhanced with GUI interface
# All rights reserved.

import string
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

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
        if tot_char == 0:
            return 0
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

class ShiftCipherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Shift Cipher Tool")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        self.cipher_tool = ShiftCrypto()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Shift Cipher Tool", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input text area
        ttk.Label(main_frame, text="Input Text:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.NW, pady=(0, 5))
        self.input_text = scrolledtext.ScrolledText(main_frame, width=60, height=8, wrap=tk.WORD)
        self.input_text.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Key input frame
        key_frame = ttk.Frame(main_frame)
        key_frame.grid(row=2, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        key_frame.columnconfigure(2, weight=1)
        
        ttk.Label(key_frame, text="Key:", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=(0, 10))
        self.key_var = tk.StringVar(value="3")
        self.key_entry = ttk.Entry(key_frame, textvariable=self.key_var, width=10)
        self.key_entry.grid(row=0, column=1, padx=(0, 20))
        
        # Auto-detected key display
        ttk.Label(key_frame, text="Auto-detected key:", font=('Arial', 10)).grid(row=0, column=2, padx=(20, 10), sticky=tk.E)
        self.detected_key_var = tk.StringVar(value="None")
        ttk.Label(key_frame, textvariable=self.detected_key_var, font=('Arial', 10, 'bold'), foreground='blue').grid(row=0, column=3, sticky=tk.W)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=20)
        
        # Style for buttons
        style = ttk.Style()
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))
        
        self.encrypt_btn = ttk.Button(button_frame, text="Encrypt", command=self.encrypt_text, style='Action.TButton')
        self.encrypt_btn.grid(row=0, column=0, padx=5)
        
        self.decrypt_btn = ttk.Button(button_frame, text="Decrypt", command=self.decrypt_text, style='Action.TButton')
        self.decrypt_btn.grid(row=0, column=1, padx=5)
        
        self.hack_btn = ttk.Button(button_frame, text="Auto-Crack", command=self.crack_cipher, style='Action.TButton')
        self.hack_btn.grid(row=0, column=2, padx=5)
        
        self.clear_btn = ttk.Button(button_frame, text="Clear All", command=self.clear_all)
        self.clear_btn.grid(row=0, column=3, padx=5)
        
        # Output text area
        ttk.Label(main_frame, text="Output:", font=('Arial', 10, 'bold')).grid(row=4, column=0, sticky=tk.NW, pady=(20, 5))
        self.output_text = scrolledtext.ScrolledText(main_frame, width=60, height=8, wrap=tk.WORD, state=tk.DISABLED)
        self.output_text.grid(row=4, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(20, 0))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def get_input_text(self):
        return self.input_text.get("1.0", tk.END).strip()
    
    def set_output_text(self, text):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", text)
        self.output_text.config(state=tk.DISABLED)
    
    def get_key(self):
        try:
            return int(self.key_var.get())
        except ValueError:
            raise ValueError("Key must be a valid integer")
    
    def encrypt_text(self):
        try:
            input_text = self.get_input_text()
            if not input_text:
                messagebox.showwarning("Warning", "Please enter text to encrypt")
                return
            
            key = self.get_key()
            result = self.cipher_tool.encdec(input_text, key, 'enc')
            self.set_output_text(result)
            self.status_var.set(f"Text encrypted with key {key}")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {str(e)}")
    
    def decrypt_text(self):
        try:
            input_text = self.get_input_text()
            if not input_text:
                messagebox.showwarning("Warning", "Please enter text to decrypt")
                return
            
            key = self.get_key()
            result = self.cipher_tool.encdec(input_text, key, 'dec')
            self.set_output_text(result)
            self.status_var.set(f"Text decrypted with key {key}")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {str(e)}")
    
    def crack_cipher(self):
        try:
            input_text = self.get_input_text()
            if not input_text:
                messagebox.showwarning("Warning", "Please enter ciphertext to crack")
                return
            
            # Find the most likely key
            detected_key = self.cipher_tool.keyfinder(input_text)
            self.detected_key_var.set(str(detected_key))
            
            # Decrypt with the detected key
            result = self.cipher_tool.encdec(input_text, detected_key, 'dec')
            self.set_output_text(result)
            
            # Update the key field with detected key
            self.key_var.set(str(detected_key))
            
            self.status_var.set(f"Cipher cracked! Most likely key: {detected_key}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Auto-crack failed: {str(e)}")
    
    def clear_all(self):
        self.input_text.delete("1.0", tk.END)
        self.set_output_text("")
        self.key_var.set("3")
        self.detected_key_var.set("None")
        self.status_var.set("Ready")

def main():
    root = tk.Tk()
    app = ShiftCipherGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()