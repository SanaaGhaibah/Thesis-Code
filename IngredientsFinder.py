import pytesseract as pt
import re
from tkinter import filedialog
from tkinter import *
import os
import numpy as np #library to make mathematical operations
import pandas as pd #library to read matrix
from tqdm import tqdm
import pickle

class CookBookPage:
    def __init__(self,name):
        self.name = name

    def tesseract_ocr(self,page):
        pt.pytesseract.tesseract_cmd=r'C:/Program Files/Tesseract-OCR/tesseract.exe'
        text=pt.image_to_string(page)
        # the re.sub is to substitute the first argument with the 2nd arg in the 3rd arg
        textsplit=re.sub(r'[^\w]', ' ', text) #replace whitespace with nothing in text
        textsplit=re.sub(r'\d+',' ',textsplit) #replace digits
        alphanumericonly=re.split(' |\n',textsplit) #splits entire text into list of strings for each word

        removallist=["","UK","I","Y","L","F","C","A","P","T","II","SELES"]  #defining a list
        for i in removallist: #iterate i over the list
            while (i in alphanumericonly): #loops until each instance of i is removed from alphanumericonly(cleanedtext)
                alphanumericonly.remove(i)

        exceptions=["eel","cod","hen","bun","pot","of","the","in","ham","raw","egg","and","pie","how","fry","roe","ice","cow","bay","oil","soy","red","rye","dry","fat","jam","pig","mix","eye","rum","gin","tea","set","sow"]
        for i in alphanumericonly:
            if i.lower() in exceptions: #skips exceptions
                continue
            if len(i)<=3: #if not in exceptions and word less than 3 remove it
                while i in alphanumericonly:
                    alphanumericonly.remove(i)

            for i in range(len(alphanumericonly)-1):
                if i==0 or i==len(alphanumericonly)-1:
                    continue
                try:
                    if alphanumericonly[i-1].isupper() and alphanumericonly[i+1].isupper() and alphanumericonly[i].islower(): #removes lower case words in recipe names
                        alphanumericonly.remove(alphanumericonly[i])
                except IndexError:
                    continue

        self.text=alphanumericonly




    def findrecipes(self):
        """
        Recipe names are all capital words, this function finds recipes by checking if the words before and after are lower case words.
        After the indexes are found, we join the recipe names together and the rest of the words together in different lists.
        """
        indexstart = [] #variable to keep track of starting indexes of Recipe Names
        indexend = [] #variable to keep track of ending indexes of Recipe Names
        index = 0 #variable to keep track of current index
        endflag = 1 #switching flag to alternate between logic to find beginning or end of Recipe names
        text = self.text #stores previously cleaned text as local variable
        recipename = [] #variable to store entire recipe name strings
        recipetext = [] #variable to store entire receipe text strings

        while(True):
            if word.isupper():
                if startflag==1:
                    if text[index-1].isupper():
                        indexstart.append(index)
                        startflag=0
                if startflag==0:
                    if text[index+1].isupper():
                        indexend.append(index+1)
                        startflag=1

            index=index+1
            if index==len(text)-1:
                indexend.append(len(text)-1)
                break

        """
        The previous logic found us the indexes that the names start and end at, the following logic will:
            Concatenate the indexes to form single strings containing entire recipe names.
            Concatenate the indexes to form single strings containing entire recipe text.
        """

        for i in range(len(indexstart)):
            recipenamewords=[]
            if i==0:
                for j in text[0:indexstart[0]]:
                    if j.isupper():
                        recipenamewords.append(j)
                recipename.append(" ".join(recipenamewords))
                recipetext.append(" ".join(text[indexstart[i]:indexend[i]]))
                continue
            for j in text[indexend[i-1]:indexstart[i]]:
                if j.isupper():
                    recipenamewords.append(j)
            recipename.append(" ".join(recipenamewords))
            recipetext.append(" ".join(text[indexstart[i]:indexend[i]]))


        return recipename,recipetext,len(recipename)




class Recipe:

    def __init__(self,recipename,recipetext):  #initialization define class
        self.recipename=recipename
        self.recipetext=recipetext
        self.ingredients=[]

    def findingredients(self,IngredientsList):
        text=self.recipetext.lower()

        text=self.recipetext.split(" ")  #splitting by spaces
        self.ingredients.append(self.recipename) #add recipe name as first column in a new row
        for i in IngredientsList:
            isplit=i.split(" ")
            if len(isplit)==1: #if ingredient has one word then simple in operand can find presense
                if i in text:
                    self.ingredients.append(1) #append 1 to the next column if the respective ingredient of the column is present
                else:
                    self.ingredients.append(0) #append 0 to the next column if the respective ingredient of the column is absent
            else: #multiple worded ingredients need multiple searches to confirm presense
                flag=0
                for j in isplit: #for every word in ingredient
                    if j not in text:
                        if j==" ":
                            continue  #if j is blank space skip word
                        flag=1  #if ingredient word was not found mark flag as 1
                if flag==0:
                    print(f"found {i}")
                    self.ingredients.append(1) #if flag was 0 then all words of the ingredient were found thus the ingredient must be present
                else:

                    self.ingredients.append(0) #if flag was 1 then one or more words of an ingredient were not found thus the ingredient must be absent
        return self.ingredients

class IngredientMatrix:

    def __init__(self,ingredient):
        self.matrix=np.array([ingredient])

    def addrecipe(self, recipe):
        self.matrix=np.append(self.matrix,[recipe],axis=0) #adding recipes in row

    def getmatrix(self):
        return self.matrix




def main():
    """
    Using Tkinter we create a dialog box to ask for the directory containing all scanned images of the cookbook
    """
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    try:
        IngredientsCSV=pd.read_csv("IngredientsList.csv",header=None, index_col=None)
    except FileNotFoundError:
        print("File read Error")
    IngredientsCSV=IngredientsCSV.values.tolist()
    IngredientList=["Recipe Name"]
    for rows in IngredientsCSV:
        for elements in rows:
            IngredientList.append(elements)


    ingmatrix=IngredientMatrix(IngredientList)
    print("Processing...")
    try:
        for filename in tqdm(os.listdir(folder_selected)):
            if filename.endswith(".JPG") or filename.endswith(".jpg")

                currentpage=CookBookPage(filename) #creating an object of CookBookPage
                pageaddress=os.path.join(folder_selected,filename)
                currentpage.tesseract_ocr(pageaddress)

                recipetitles,recipetexts,numberrecipe=currentpage.findrecipes()
                for i in range(numberrecipe):
                    currentrecipe = Recipe(recipetitles[i]+" In File:"+filename,recipetexts[i]) #adding filename to recipe name
                    ingmatrix.addrecipe(currentrecipe.findingredients(IngredientList[1:]))
                    del currentrecipe
                del currentpage
                continue
            else:
                continue


    except FileNotFoundError:
        print("Folder Read Error")
        quit()

    matrixfinal=ingmatrix.getmatrix()
    pd.DataFrame(matrixfinal).to_csv("RecipeIngredients.csv",header=None, index=None)
    print("Done")

if __name__ == '__main__':
    main()
