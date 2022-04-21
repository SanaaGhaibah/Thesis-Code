from operator import itemgetter
import pandas as pd
from atpbar import atpbar


def main():
    """
    The following code reads two csv files and converts them into numpy matrices, first is the matrix containing recipe and ingredient presence,
    and the other is the previously computed ranks for combinations of 3 ingredients.
    """
    matrix = pd.read_csv("RecipeIngredients.csv", index_col = None, header = None, delimiter = ",")
    threematrix = pd.read_csv("Rankedfor3.csv", index_col = None, header = None, delimiter = ",")
    matrix = matrix.to_numpy()
    threematrix = threematrix.to_numpy()

    """
    Since computing the ranks of 4 combinations of 270 ingredients was computationally a bad idea, we extract the top 200 ranked 3 combiantions and compute the 4 combinations using them as base.
    """
    top200ings = [] #stores top 200 3 combination ingredients
    for i in range(1,301):
        top200ings.append([int(threematrix[i][4]), int(threematrix[i][5]), int(threematrix[i][6])])

    """
    Using the three ingredients as a base we create all possible 3 combinations with the first 3 indexes being constant
    """
    top200ingsextended = []
    for i in atpbar(top200ings, name = "Creating Combinations from Triplets"):
        for j in range(1, len(matrix[0])):
            templist = i
            if j in templist:
                continue
            templist = templist + [j] # concatenations of lists
            top200ingsextended.append(templist)

    """
    The process of ranking a combination of 4 ingredients is as follows:
        Step 1: Check if ingredient 1 is present in recipe
        Step 2: Check if ingredient 2 is present in recipe
        Step 3: Check if ingredient 3 is present in recipe
        Step 4: Check if ingredient 4 is present in recipe
        Step 5: If all three checks are true then increase rank by 1
    This is repeated over all the recipes and the final rank is returned with the three ingredients only if the rank is more than 1
    """
    addlist = []
    for i in atpbar(top200ingsextended, name = "Ranking Combinations"):
        rank = 0
        for j in range(1, len(matrix)):
            if int(matrix[j][i[0]])==1 and int(matrix[j][i[1]])==1 and int(matrix[j][i[2]])==1 and int(matrix[j][i[3]])==1:
                rank += 1
        if rank != 0:
            addlist.append([matrix[0][i[0]],matrix[0][i[1]],matrix[0][i[2]],matrix[0][i[3]],rank])

    addlist=sorted(addlist, key = itemgetter(4), reverse = True) #sort list by rank
    addlist.insert(0,["Ing1","Ing2","Ing3","Ing4","Rank"]) #add header to the list
    pd.DataFrame(addlist).to_csv("RankedFor4.csv",header = None, index = None) #convert list to matrix and export as csv

if __name__ == '__main__':
    main()
