#importing packages 
import numpy as np
import re
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder 
import seaborn as sns
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
#reading in clean data 
clean_df = pd.read_csv(r"C:\Users\aikob\OneDrive\Documents\RMP Project\Output\all_prof_clean.csv")
#changing gender to zeroes and ones  
one_hot = OneHotEncoder(sparse = False)
encoded_gender = one_hot.fit_transform(clean_df[["Professor Gender"]])
columns = ["Gender","Male","Nonbinary"]
encoded_df = pd.DataFrame(encoded_gender,columns = columns)
encoded_df = encoded_df.drop(columns=["Male", "Nonbinary"],axis=1)
clean_df = pd.concat([clean_df,encoded_df], axis=1)
clean_df = clean_df.drop(columns=["Professor Gender"],axis=1)
clean_df = clean_df.rename(columns={"Female":"Gender"})
#onehot encoding department 
encoded_department = one_hot.fit_transform(clean_df[["Department"]])
columns = one_hot.get_feature_names_out()
dept_df = pd.DataFrame(encoded_department,columns=columns)
clean_df = pd.concat([clean_df,dept_df],axis=1) 
#onehot encoding year 
encoded_year = one_hot.fit_transform(clean_df[["Year"]])
y_columns = one_hot.get_feature_names_out()
year_df = pd.DataFrame(encoded_year,columns=y_columns)
clean_df = pd.concat([clean_df, year_df],axis=1)
clean_df = clean_df.drop(["Year_2001"],axis=1)
pre_pca = clean_df.drop(["Professor Name","Professor ID","Department","Department_Aerospace Studies","Time Stamp","Comments","Year"],axis=1)
#standardizing quality difficulty 
pre_pca["Standardized Quality"] = (pre_pca["Quality"] - np.mean(pre_pca["Quality"]))/np.std(pre_pca["Quality"])
pre_pca["Standardized Difficulty"] = (pre_pca["Difficulty"]-np.mean(pre_pca["Difficulty"]))/np.std(pre_pca["Difficulty"])
#do a pca on regression to get rid of all the dummies? 
pca = PCA(n_components=7)
result = pca.fit_transform(pre_pca)
col_names = pca.get_feature_names_out()
#create a scree plot 
u, s, vt = np.linalg.svd(pre_pca)
score = np.square(s)/sum(np.square(s))
fig, ax = plt.subplots(figsize=(8, 6))
sns.lineplot(x=np.arange(1,len(score)+1),y=score, ax=ax)
plt.xlabel('Principal Component')
plt.ylabel('Variance Explained')
plt.title('Scree Plot')
ax.set_xlim(1,15)
plt.show()
#create rude, condescending, intimidating, unqualified columns 

#run regression then p test? 
