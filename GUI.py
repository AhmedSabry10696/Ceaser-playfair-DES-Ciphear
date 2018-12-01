from tkinter import *
import string

PI = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

#Initial permut made on the key
CP_1 = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]

#Permut applied on shifted key to get Ki+1
CP_2 = [14, 17, 11, 24, 1, 5, 3, 28,
        15, 6, 21, 10, 23, 19, 12, 4,
        26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40,
        51, 45, 33, 48, 44, 49, 39, 56,
        34, 53, 46, 42, 50, 36, 29, 32]

#Expand matrix to get a 48bits matrix of datas to apply the xor with Ki
E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

#SBOX
S_BOX = [
         
[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
 [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
 [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
 [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
],

[[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
 [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
 [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
 [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
],

[[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
 [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
 [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
 [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
],

[[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
 [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
 [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
 [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
],  

[[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
 [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
 [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
 [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
], 

[[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
 [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
 [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
 [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
], 

[[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
 [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
 [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
 [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
],
   
[[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
 [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
 [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
 [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
]
]

#Permut made after each SBox substitution for each round
P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

#Final permut for datas after the 16 rounds
PI_1 = [40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25]

#Matrix that determine the shift for each round of keys
SHIFT = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

def string_to_bit_array(text):#Convert a string into a list of bits
    array = list()
    for char in text:
        binval = binvalue(char, 8)#Get the char value on one byte
        array.extend([int(x) for x in list(binval)]) #Add the bits to the final list
    return array

def bit_array_to_string(array): #Recreate the string from the bit array
    res = ''.join([chr(int(y,2)) for y in [''.join([str(x) for x in bytes]) for bytes in  nsplit(array,8)]])   
    return res

def binvalue(val, bitsize): #Return the binary value as a string of the given size 
    binval = bin(val)[2:] if isinstance(val, int) else bin(ord(val))[2:]
    if len(binval) > bitsize:
        raise "binary value larger than the expected size"
    while len(binval) < bitsize:
        binval = "0"+binval #Add as many 0 as needed to get the wanted size
    return binval

def nsplit(s, n):#Split a list into sublists of size "n"
    return [s[k:k+n] for k in range(0, len(s), n)]

ENCRYPT=1
DECRYPT=0

class des():
    def __init__(self):
        self.password = None
        self.text = None
        self.keys = list()
        
    def run(self, key, text, action):
    
        self.password = key
        self.text = text
        
        self.generatekeys() #Generate all the keys
        text_block = self.text
        result = list()
        
        text_block = string_to_bit_array(text_block)#Convert the block in bit array
        text_block = self.permut(text_block,PI)#Apply the initial permutation
        L, R = nsplit(text_block, 32) #L(LEFT), R(RIGHT)
        tmp = None
        for i in range(16): #Do the 16 rounds
            r_e = self.expand(R, E) #Expand R to match Ki size (48bits)
            if action == ENCRYPT:
                tmp = self.xor(self.keys[i], r_e)#If encrypt use Ki
            else:
                tmp = self.xor(self.keys[15-i], r_e)#If decrypt start by the last key
            tmp = self.substitute(tmp) #Method that will apply the SBOXes
            tmp = self.permut(tmp, P)
            tmp = self.xor(L, tmp)
            L = R
            R = tmp
            
        result += self.permut(R+L, PI_1) #Do the last permut and append the result to result
        final_res = bit_array_to_string(result)
        return final_res #Return the final string of data ciphered/deciphered
    
    def substitute(self, r_e):#Substitute bytes using SBOX
        subblocks = nsplit(r_e, 6)#Split bit array into sublist of 6 bits
        result = list()
        for i in range(len(subblocks)): #For all the sublists
            block = subblocks[i]
            row = int(str(block[0])+str(block[5]),2)#Get the row with the first and last bit
            column = int(''.join([str(x) for x in block[1:][:-1]]),2) #Column is the 2,3,4,5th bits
            val = S_BOX[i][row][column] #Take the value in the SBOX appropriated for the round (i)
            bin = binvalue(val, 4)#Convert the value to binary
            result += [int(x) for x in bin]#And append it to the resulting list
        return result
        
    def permut(self, block, table):#Permut the given block using the given table (so generic method)
        return [block[x-1] for x in table]
    
    def expand(self, block, table):#Do the exact same thing than permut but for more clarity has been renamed
        return [block[x-1] for x in table]
    
    def xor(self, t1, t2):#Apply a xor and return the resulting list
        return [x^y for x,y in zip(t1,t2)]
    
    def generatekeys(self):#Algorithm that generates all the keys
        self.keys = []
        key = string_to_bit_array(self.password)
        key = self.permut(key, CP_1) #Apply the initial permut on the key
        g, d = nsplit(key, 28) #Split it in to (g->LEFT),(d->RIGHT)
        for i in range(16):#Apply the 16 rounds
            g, d = self.shift(g, d, SHIFT[i]) #Apply the shift associated with the round (not always 1)
            tmp = g + d #Merge them
            self.keys.append(self.permut(tmp, CP_2)) #Apply the permut to get the Ki

    def shift(self, g, d, n): #Shift a list of the given value
        return g[n:] + g[:n], d[n:] + d[:n]
    
    def encrypt(self, key, text):
        return self.run(key, text, ENCRYPT)
    
    def decrypt(self, key, text):
        return self.run(key, text, DECRYPT)

d = des()

def Choose_Algorthim_E():
    if var.get() == 1:
        Caesar_Cipher_E()
    elif var.get() == 2:
        Playfair_Cipher_E()
    elif var.get() == 3:
        DES_Cipher_E()
    else:
        print("error")

def Choose_Algorthim_D():
    if var.get() == 1:
        Caesar_Cipher_D()
    elif var.get() == 2:
        Playfair_Cipher_D()
    elif var.get() == 3:
        DES_Cipher_D()
    else:
        print("error")

def Reset():
    var1.set('0')
    var2.set('')
    var3.set('')

def Caesar_Cipher_E():
    key =int(var1.get())
    input1 =list(var2.get())
    output1 =''
    
    for char in input1:
        if char.isupper():
            output1 += chr((ord(char) + key -65) % 26 + 65)
        elif char.islower():
            output1 += chr((ord(char) + key -97) % 26 + 97)
        else:
            output1 += char
    var3.set(output1)

def Caesar_Cipher_D():
    key =int(var1.get())
    input1 =list(var3.get())
    output1 =''
    
    for char in input1:
        if char.isupper():
            output1 += chr((ord(char) - key -65) % 26 + 65)
        elif char.islower():
            output1 += chr((ord(char) - key -97) % 26 + 97)
        else:
            output1 += char    
    var2.set(output1)

def Generate_Table(key):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    table = []
    for char in key.upper():
        if char not in table and char in alphabet:
            table.append(char)

    for char in alphabet:
        if char not in table:
            table.append(char)

    return table

def Playfair_Cipher_E():
    key =str(var1.get())
    table = Generate_Table(key)
    input1 = list(var2.get())
    for char in range(len(input1)):
        if (input1[char] == 'j') or (input1[char] == 'J'):
            input1[char] = 'i'
    input1 = ''.join(input1).upper()
    input1 = list(input1)
    
    output1 = ''
    x=0
    while x<len(input1)-1:
        if input1[x] == input1[x+1]:
            input1.insert(x+1,'X')
        x = x+2

    if len(input1)%2 == 1:
        input1.append('X')


    l2 = []
    x = 0
    while x < len(input1):
        index1 = table.index(input1[x])
        index2 = table.index(input1[x+1])


        if abs(index1 - index2) == abs(index1%5 - index2%5):
            if index1%5 == 4:
                l2.append(table[index1 - 4])
            else:
                l2.append(table[index1 + 1])
            if index2%5 == 4:
                l2.append(table[index2 - 4])
            else:
                l2.append(table[index2 + 1])

        elif index1%5 == index2%5:
            if index1 + 5 > 24:
                l2.append(table[index1%5])
            else:
                l2.append(table[index1 + 5])
            if index2 + 5 > 24:
                l2.append(table[index2%5])
            else:
                l2.append(table[index2 + 5])
        else:
            if index2%5 > index1%5:
                shift = index2%5 - index1%5
                l2.append(table[index1 + shift])
                l2.append(table[index2 - shift])
            else:
                shift = index1%5 - index2%5
                l2.append(table[index1 - shift])
                l2.append(table[index2 + shift])       
        x = x+2
    output1 = ''.join(l2)
    var3.set(output1)


def Playfair_Cipher_D():
    key =str(var1.get())
    table = Generate_Table(key)
    input1 =list(var3.get())
    output = []
    x = 0
    
    while x < len(input1):
        index1 = table.index(input1[x])
        index2 = table.index(input1[x+1])

        if abs(index1 - index2) == abs(index1%5 - index2%5):
            if index1%5 == 0:
                output.append(table[index1 + 4])
            else:
                output.append(table[index1 - 1])
            if index2%5 == 0:
                output.append(table[index2 + 4])
            else:
                output.append(table[index2 - 1])

                

        elif index1%5 == index2%5:
            if index1 - 5 < 0:
                output.append(table[index1 + 20])
            else:
                output.append(table[index1 - 5])
            if index2 - 5 < 0:
                output.append(table[index2 + 20])
            else:
                output.append(table[index2 - 5])
                
        else:
            if index2%5 > index1%5:
                shift = index2%5 - index1%5
                output.append(table[index1 + shift])
                output.append(table[index2 - shift])
            else:
                shift = index1%5 - index2%5
                output.append(table[index1 - shift])
                output.append(table[index2 + shift])       
        x = x+2
    output = ''.join(output)
    print(output)
    var2.set(output)

def DES_Cipher_E():
    key =str(var1.get())
    input1 = list(var2.get())
    var3.set(d.encrypt(key,input1))

def DES_Cipher_D():
    key =str(var1.get())
    input1 =list(var3.get())
    var2.set(d.decrypt(key,input1))



window =Tk()
window.geometry('320x450+250+250')  # size & apear place
window.title('Encyrption & Decyrption Algorthims')    # title
Label(text ="Encyrption & Decyrption Algorthims",fg ='black',bg ='white').place(x =60,y =0) 

var =IntVar()   # Algorthim identifier 1:Caesar Cipher   2:Play Fair 
var.set(1)      # default Caesar Cipher 
Label(text ="Choose Your Algorthim :",fg ='black',bg ='white').place(x =0,y =30)
Radiobutton(window,text ="Caesar Cipher",variable =var,value =1).place(x =0,y =55)
Radiobutton(window,text ="Play Fair",variable =var,value =2).place(x =0,y =75)
Radiobutton(window,text ="DES",variable =var,value =3).place(x =0,y =95)

var1 =StringVar() # store key value
var1.set('0')     # default 0
Label(text ="Enter The Key",fg ='black').place(x =110,y =120) 
Entry(window,justify =CENTER,width =30,textvariable =var1).place(x =70,y =140)

var2 =StringVar() # store input string
Label(text ="Enter Text To Encyrpt",fg ='black').place(x =90,y =180) 
Entry(window,justify =CENTER,width =50,textvariable =var2).place(x =5,y =200)
Button(text ="Encyrption",bg ='white',command =Choose_Algorthim_E).place(x =120,y =220) 

var3 =StringVar() # store output
Label(text ="Encyrpted Text", fg ='black').place(x =110,y =270) 
Button(text ="Decyrption", bg ='white',command =Choose_Algorthim_D).place(x =115,y =310) 
Entry(window,justify =CENTER,width =50,textvariable =var3).place(x =5,y =290)
Label(text ="ahmed sabry abdelaziz elsera",fg ='black').place(x =0,y =425)
Button(text ="Reset", bg ='white',command =Reset ).place(x =278,y =422) 
window.mainloop()

