import pandas as pd
import numpy as np
import itertools as it
import tqdm


class RankMatrix:

    def __init__(self):
        self.matrix=np.array([["Ingredient1","Ingredient2","Ingredient3","Rank"]])

    def addrank(self, rank):
        self.matrix=np.append(self.matrix,[rank],axis=0)

    def getmatrix(self):
        return self.matrix


def main():
    matrix=pd.read_csv("RecipeIngredients.csv",index_col=None,header=None,delimiter=",") # Reads CSV to retrieve list of ingredients and recipes and presence of those ingredients
    matrix=matrix.to_numpy() #convert matrix to numpy
    count=0
    rankmatrix=RankMatrix()
    ing_combinations=list(it.combinations(range(1,len(matrix[0])),3))  #using itertools combinations we create all possible 3 number combinations within the range of our indexes of the matrix

    """
    The process of ranking a combination of 3 ingredients is as follows:
        Step 1: Check if ingredient 1 is present in recipe
        Step 2: Check if ingredient 2 is present in recipe
        Step 3: Check if ingredient 3 is present in recipe
        Step 4: If all three checks are true then increase rank by 1
    This is repeated over all the recipes and the final rank is returned with the three ingredients only if the rank is more than 1
    """
    for i in tqdm.tqdm(ing_combinations):
        rank=0
        for j in range(1,len(matrix)):
            if int(matrix[j][i[0]])==1 and int(matrix[j][i[1]])==1 and int(matrix[j][i[2]])==1:
                rank+=1
        addlist=[matrix[0][i[0]],matrix[0][i[1]],matrix[0][i[2]],rank]
        rankmatrix.addrank(addlist)

    pd.DataFrame(rankmatrix.getmatrix()).to_csv("RankedFor3.csv",header=None, index=None) #convert and export the list as matrix in csv form
if __name__ == '__main__':
    main()
