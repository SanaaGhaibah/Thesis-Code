import pandas as pd
from tqdm import tqdm


def main():
    matrix=pd.read_csv("RecipeIngredients.csv",index_col=None,header=None,delimiter=",") #import from file
    matrix=matrix.to_numpy() #create matrix
    totalrecipes=len(matrix)
    percentlist=[] #create list
    for i in range(1,len(matrix[0])-1):
        sum=0
        for j in range(1,len(matrix)-1):
            sum=sum+int(matrix[j][i])
        percentpresence=(sum/totalrecipes)*100 #calculate percentage
        presenceratio=sum/totalrecipes #calculate ratio
        percenttuple=(matrix[0][i],percentpresence,presenceratio)
        percentlist.append(percenttuple)
    pd.DataFrame(percentlist).to_csv("PercentPresenceAllIngredients.csv",header=None, index=None) #export result in csv file
if __name__ == '__main__':
    main()
