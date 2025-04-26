import numpy as np
import pandas as pd
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="pand2002",
  database="Customers_data"
)

import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#data collection from dataset (csv to pandas)
movies_data=pd.read_csv('D:\\Users\\svsiv\\Desktop\\caps-python\\movies.csv')
#printing the rows of the dataset

print(movies_data)
#counting the number of rows and columns
print(movies_data.shape)
#selecting the features
selected_features=['genres','keywords','tagline','cast','director']
print(selected_features)

print(type(movies_data))
#replacing the null values
df_movie = movies_data.fillna(" ") 
df_movie.isnull().sum()
# combining the selected featues
combined_feature=df_movie['genres']+' '+df_movie['keywords']+' '+df_movie['tagline']+' '+df_movie['cast']+' '+df_movie['director']
print(combined_feature)

#converting text data to feature data
vectorizer=TfidfVectorizer()
feature_vector=vectorizer.fit_transform(combined_feature)
print(feature_vector)
#getting the similairty
similarity=cosine_similarity(feature_vector)
print(similarity)
print(similarity.shape)

#input of movie from user
movie_name=[]
User_name=input("Enter the user_name:")
movie_name=input("Enter the movie:")
mobile_num=input("Enter the mobile num:")
for x in movie_name:
    sql = "INSERT INTO cinephile (U_name,Mob_Num,Mov_name) VALUES (%s,%s,%s)"
    val =[(User_name),(mobile_num),(movie_name)]
mycursor = mydb.cursor()
mycursor.execute(sql,val)
print("Inserted",mycursor.rowcount,"row(s) of data.")
mydb.commit()
# creating the list of all the movies
list_of_title=df_movie['title'].tolist()
print(list_of_title)
# now finding the combinations and matching
find_close_match=difflib.get_close_matches(movie_name,list_of_title)
print(find_close_match)
# getting the close match
close_match=find_close_match[0]
print(close_match)
#finding the index and relevant info
index_of_movie=df_movie[df_movie.title==close_match]['index'].values[0]
print(index_of_movie)

#getting the list of the movie
similarity_score=list(enumerate(similarity[index_of_movie]))
print(similarity_score)

sorted_similar_movies = sorted(similarity_score, key = lambda x:x[1], reverse = True) 
print(sorted_similar_movies)

print("Movies suggested are and their genre")
i = 1
data=[]
for movie in sorted_similar_movies:
  index = movie[0]
  homepg=df_movie[df_movie.index==index]['homepage'].values[0]
  title_from_index = df_movie[df_movie.index==index]['title'].values[0]
  genr = df_movie[df_movie.index==index]['genres'].values[0]
  if (i<6):
    print(i, '.',title_from_index,',',genr,',,',homepg)
    data.append(title_from_index)
    i+=1
for m in data:
    msql= "update cinephile set reco_1=%s,reco_2=%s,reco_3=%s,reco_4=%s,reco_5=%s where U_name=%s"
    mval=[(data[0]),(data[1]),(data[2]),(data[3]),(data[4]),User_name]
mycursor = mydb.cursor()
mycursor.execute(msql,mval)
print("Inserted",mycursor.rowcount,"row(s) of data.")
mydb.commit()
mydb.close()
    
