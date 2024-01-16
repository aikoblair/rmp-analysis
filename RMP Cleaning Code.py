#importing packages 
import numpy as np
import re
import pandas as pd
#importing df 
df = pd.read_csv(r"C:\Users\aikob\OneDrive\Documents\RMP Project\all_prof.csv")
#remove duplicates 
duplicate_rows = df[df.duplicated("Comments")]["Comments"].unique()
to_be_deleted = [i for i in duplicate_rows if len(i)>3]
df = df.drop_duplicates()
#duplicate check 
unique_comments = df["Comments"].unique()
comments = df["Comments"]
test = len(unique_comments)==len(comments)
#changing quality and difficulty to numbers, not strings 
print(type(df["Quality"][1]))
df[df["Quality"]==5.0]
print(type(df["Difficulty"][1]))
df[df["Difficulty"]==5]
#getting rid of "department" in department
pat = r"\sdepartment"
test = df["Department"][1]
no_dept = [re.sub(pat, "",i) for i in df["Department"]]
check = "department" in no_dept
df["Department"]= no_dept
#replace amp with ampersand 
amp = r"amp"
no_amp=[re.sub(amp,"&",i) for i in df["Department"]]
test = amp in no_amp
df["Department"]=no_amp
#fixing departments 
unique_departments = df['Department'].unique()
sorted = np.sort(unique_departments)
print(sorted)
#fixing departments 
df.loc[df["Department"]=='Art Media & Design',"Department"] = "Art, Media, & Design"
df.loc[df["Department"]=='Earth Planetary Sciences',"Department"] = "Earth & Planetary Sciences"
df.loc[df["Department"]=='Earth Science',"Department"] = "Earth & Planetary Sciences"
df.loc[df["Department"]=='Earth Science',"Department"] = "Earth & Planetary Sciences"
df.loc[df["Department"]=='Landscape Architecture Regional Planning',"Department"] = "Landscape Architecture & Regional Planning"
df.loc[df["Department"]=='MolecularCellular Biology',"Department"] = "Molecular/Cellular Biology"
df.loc[df["Department"]=='Peace Conflict Studies',"Department"] = "Peace & Conflict Studies"
df.loc[df["Department"]=='Women',"Department"] = "Women's Studies"
engineering = ['Bioengineering', 'Chemical Engineering', 'Civil & Environmental Engineering', 'Civil Engineering','Electrical Engineering','Mechanical Engineering','Industrial Engineering','Nuclear Engineering']
df.loc[df["Department"].isin(engineering), "Department"] = "Engineering"
#changing mostly male to male and mostly female to female 
mostly_male = df[df["Professor Gender"]=="mostly_male"]
df.loc[df["Professor Gender"]=='mostly_male',"Professor Gender"] = "male"
mostly_female = df[df["Professor Gender"]=="mostly_female"]
df.loc[df["Professor Gender"]=='mostly_female',"Professor Gender"] = "female"
#extract year from timestamp, make new column? 
year_only = [i.split(",")[1] for i in df["Time Stamp"]]
df["Year"] = year_only
#download as csv 
csv_file_path = r"C:\Users\aikob\OneDrive\Documents\RMP Project\all_prof_clean.csv" 
df.to_csv(csv_file_path, index=False)
