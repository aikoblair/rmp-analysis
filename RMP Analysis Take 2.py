import numpy as np
import re
import pandas as pd
from sklearn.preprocessing import OneHotEncoder 
import seaborn as sns
import matplotlib.pyplot as plt
#import csv
clean_df = pd.read_csv(r"C:\Users\aikob\OneDrive\Documents\RMP Project\Output\all_prof_clean.csv")
#needs gender column 
one_hot = OneHotEncoder(sparse = False)
encoded_gender = one_hot.fit_transform(clean_df[["Professor Gender"]])
columns = ["Gender","Male","Nonbinary"]
encoded_df = pd.DataFrame(encoded_gender,columns = columns)
encoded_df = encoded_df.drop(columns=["Male", "Nonbinary"],axis=1)
clean_df = pd.concat([clean_df,encoded_df], axis=1)
clean_df = clean_df.drop(columns=["Professor Gender"],axis=1)
clean_df = clean_df.rename(columns={"Female":"Gender"})
clean_df = clean_df.dropna()
#needs output column 
#have to remove quotes from quotes to not mess up the thing 
#rudeness check? 
rude_pat = r'\s*(rude\w*)'
con_pat = r'\s*(condescending)'
int_pat = r'\s*(intimidat\w+)'
arr_pat = r'\s*(arrogant)'
cute_pat = r'\s*(cute\w*)'
un_pat = r'\s*(unqualified)'
sty_pat = r'\s*(stylish)'
patterns = [rude_pat,con_pat,int_pat,arr_pat,cute_pat,un_pat,sty_pat]
colname_pat = r'\(([a-z]+)'
#big loop 
for pat in patterns: 
    catch_list = [] 
    comments = [] 
    for element in list(clean_df["Comments"]):
        if re.search(pat,element,re.IGNORECASE):
            catch_list.append(1)
            comments.append(element)
    colname = re.findall(colname_pat,pat)
    catch_df = pd.DataFrame(catch_list,columns=colname)
    catch_df["Comments"]=comments 
    clean_df = pd.merge(clean_df, catch_df,how='left',on="Comments")
clean_df.fillna(0)
csv_file_path = r"C:\Users\aikob\OneDrive\Documents\RMP Project\first_run.csv" 
clean_df.to_csv(csv_file_path, index=False)
#just peeking 
ladies_choice = clean_df.loc[(clean_df["Gender"]==1) & (clean_df["intimidat"]==1)].shape[0]
guys = clean_df.loc[(clean_df["Gender"]==0) & (clean_df["intimidat"]==1)].shape[0]
#making a heatmap to figure out how many departments you need 
one_hot = OneHotEncoder(sparse = False)
encoded_department = one_hot.fit_transform(clean_df[["Department"]])
columns = one_hot.get_feature_names_out()
dept_df = pd.DataFrame(encoded_department,columns=columns)
clean_df = pd.concat([clean_df,dept_df],axis=1) 
columns = list(columns)
columns.append("rude")
sub_df = clean_df[columns]
correlation = sub_df.corr()
target_correlations = correlation['rude']
not_na_mask = target_correlations.notna()
non_na = target_correlations[not_na_mask]
#figure out as factor equivalent 87
