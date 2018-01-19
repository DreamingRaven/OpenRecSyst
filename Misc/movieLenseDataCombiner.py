#!usr/bin/env python3.6

# quick python file to wrangle movieLense data set
import pandas as pd
import os
import sys
import struct # used to accurately calculate python version bits (32/64)

# creating prepend variable for logging
prePend = "[ " + os.path.basename(sys.argv[0]) + " ] "
print(prePend, "python version (bit): ", struct.calcsize("P") * 8) # check if 32 or 64 bit

# outputting debug info
cwd = os.getcwd()
print(prePend, "Current wd: ", cwd)
print(prePend, "Args: ", str(sys.argv))

# setting data folder path with possible args(a if condition else b)
dataFolderPath = "../../../DataSets/ml-20m/" # this is the default path
dataFolderPath = dataFolderPath if len(sys.argv) == 1 else sys.argv[1]
print(prePend, "Data path:", dataFolderPath)

# check if data exists
if os.path.isfile(dataFolderPath + "pML.csv"):# and 1 == 0:
    print(prePend, "pML.csv found... Skipping.")
else: # else generate csv
    print(prePend, "pML.csv not found... Generating.")

    # inputting data
    ratings = pd.read_csv(dataFolderPath + 'pMLRatings.csv')
    metadata = pd.read_csv(dataFolderPath + 'pMLMetadata.csv')

    # combining data
    # sort data to make things more easily debuggable
    metadata.sort_values(['movieId', 'tag'], ascending=[True, True], inplace=True)
    # take every unique tag in metadata and its relevance and add as feature in ratings to its respective movie
    movieTags = metadata.loc[:, ['movieId', 'relevance', 'tag']] # separate out all information which is not handled
    del metadata # forcably cleaning some space
    uniqueTagsMetaData = movieTags['tag'].unique()
    ratingColumnNames = ratings.columns.values.tolist() # <-- built in fastest method
    eachMoviesTags = movieTags.groupby('movieId')#.head(10) # group by each movie

    # combine column headers into one list
    print(prePend, type(uniqueTagsMetaData.tolist()), type(ratingColumnNames))
    fullFeatureList = ratingColumnNames + uniqueTagsMetaData.tolist() # + user relevance tags

    # creating final (large) data file
    df = pd.DataFrame(columns=fullFeatureList)
    print(prePend, df)

    i = 0 # not important here so you can see progress
    x = [] # list of lists
    specificColumnNames = [] # cry me a river
    for name, group in eachMoviesTags:
        i += 1
        # group is of type pandas DataFrame meaning concat will be easier
        groupTemp = group.transpose() # transpose to be tag column major order
        groupTemp.columns = groupTemp.iloc[2] # make a specific row the columns
        groupTemp = groupTemp.drop(['tag', 'movieId'], 0) # remove some rows
        #groupTemp = groupTemp.reset_index(drop=True) # get rid of previous index
        #groupTemp = groupTemp.rename_axis(None)
        groupTemp['movieId'] = name # add id column
        if (i % 10) == 0:
            print(prePend, "progress:", i, "/", len(eachMoviesTags), " movieId: ", groupTemp['movieId'][0])
            if i == 10:
                specificColumnNames = groupTemp.columns.tolist()
        x.append(groupTemp.values.tolist())


    #print(x)
    print(prePend, specificColumnNames)
    #reformedMetaData = pd.DataFrame(x.values.tolist(), columns=['lists'])#, columns=specificColumnNames)
    reformedMetaData = pd.DataFrame(x, columns=['lists'])#, columns=specificColumnNames)
    reformedMetaData = pd.DataFrame(reformedMetaData['lists'].values.tolist(), columns=specificColumnNames)

    #reformedMetaData.columns = specificColumnNames
    #reformedMetaData = pd.concat(x)
    print(prePend, reformedMetaData)
    # df.to_csv((dataFolderPath + "zFullFeatureFile.csv"), encoding='utf-8', index=False)

    #uniqueTags = uniqueTags.tolist()
    #ratings = ratings.reindex(columns = newColumns)#ratings.columns.tolist() + ['ello']) #+ uniqueTags.tolist())

    # create an identical number of null features as previous
    # sort list by time increasing down, and group by user ID
    # For each tag the null = <for each user while in the past> (SUM(tagRelevance * rating))
    pML = ratings

    # outputting data
    pML.to_csv( (dataFolderPath + "pML.csv"), encoding='utf-8', index=False)
    reformedMetaData.to_csv(dataFolderPath + "pMLMetaReformed.csv", encoding='utf-8', index=False)

print(prePend, "Fin.")