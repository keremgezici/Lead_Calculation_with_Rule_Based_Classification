###########################################
# Lead Calculation with Rule-Based Classification
###########################################
###########################################
# Business Problem
###########################################
# Level-based new customer definitions (persona) using some features of a game company's customers
# to create segments according to these new customer definitions,
# wants to estimate how much you can earn on average.

# For example: It is desired to determine how much a 25-year-old male user from Turkey who is an IOS user can earn on average.

###########################################
# Dataset Story
###########################################
# Persona.csv dataset shows the prices of the products sold by an international game company and some of the users who buy these products.
# contains demographic information. The data set consists of records created in each sales transaction. This means table
# is not deduplicated. In other words, a user with certain demographic characteristics may have made more than one purchase.

# Price: Customer's spending amount
# Source: The type of device the customer is connecting to
# Sex: Gender of the client
# Country: Country of the customer
# Age: Customer's age

###########################################
# PROJECT TASKS
###########################################
###########################################
# TASK 1: Answer the following questions.
###########################################
# Question 1: Read the persona.csv file and show the general information about the dataset.
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
df = pd.read_csv("pyCharm_Protect/datasets/persona.csv")
df.head
df.shape
df.info()
df.columns
df.columns.value_counts()
df.nunique()
df.index
df.describe().T
df.isnull()
df.isnull().values.any()
df.isnull().sum()
df.dtypes

# Question 2: How many unique SOURCE are there? What are their frequencies?
df["SOURCE"].nunique()
# Question 3: How many unique PRICEs are there?
df["PRICE"].nunique()
# Question 4: How many sales were made from which PRICE?
df["PRICE"].value_counts()
# Question 5: How many sales were made from which country?
df["COUNTRY"].value_counts()
# df.groupby("COUNTRY")["PRICE"].count()
# Question 6: How much was earned in total from sales by country?
df.groupby("COUNTRY")["PRICE"].sum()
# Question 7: What are the sales numbers by SOURCE types?
df["SOURCE"].value_counts()
# Question 8: What are the PRICE averages by country?
df.groupby('COUNTRY').agg({"PRICE": "mean"})
# Question 9: What are the PRICE averages by SOURCEs?
df.groupby('SOURCE').agg({"PRICE": "mean"})
# Question 10: What are the PRICE averages in the COUNTRY-SOURCE breakdown?
df.groupby(["COUNTRY", 'SOURCE']).agg({"PRICE": "mean"})

###########################################
# TASK 2: What are the average earnings in breakdown of COUNTRY, SOURCE, SEX, AGE?
###########################################
df.groupby(["COUNTRY", 'SOURCE', "SEX", "AGE"]).agg({"PRICE": "mean"})

###########################################
# TASK 3: Sort the output by PRICE.
###########################################
# Apply the sort_values method to PRICE in descending order to see the output in the previous question better.
# Save the output as agg_df.
agg_df = df.groupby(["COUNTRY", 'SOURCE', "SEX", "AGE"]).agg({"PRICE": "mean"}).sort_values("PRICE", ascending=False)
agg_df.head()

###########################################
# TASK 4: Convert the names in the index to variable names.
###########################################
# All variables except PRICE in the output of the third question are index names.
# Convert these names to variable names.
# Hint: reset_index()
agg_df.reset_index(inplace=True)
agg_df.head()
agg_df.shape

###########################################
# TASK 5: Convert AGE variable to categorical variable and add it to agg_df.
###########################################
# Convert the numeric variable age to a categorical variable.
# Construct the intervals as you think will be persuasive.
# For example: '0_18', '19_23', '24_30', '31_40', '41_70'

# Let's specify where the AGE variable will be divided:
bins = [0, 18, 23, 30, 40, agg_df["AGE"].max()]

# Let's express what the nomenclature will be for the dividing points:
mylabels = ['0_18', '19_23', '24_30', '31_40', '41_' + str(agg_df["AGE"].max())]

# divide age:
agg_df["age_cat"] = pd.cut(agg_df["AGE"], bins, labels=mylabels)
agg_df.head()

###########################################
# Task 6: Identify new level-based customers (personas)
###########################################
agg_df["customers_level_based"]=agg_df["COUNTRY"]
for i in agg_df.index:

    agg_df["customers_level_based"][i] = str(agg_df["COUNTRY"][i].upper()+"_")+ str(agg_df["SOURCE"][i].upper()+"_" ) +str(agg_df["SEX"][i].upper()+"_") + str(agg_df["AGE_CAT"][i])

# Let's remove the unnecessary variables:
agg_df = agg_df[["customers_level_based", "PRICE"]]
agg_df.head()

agg_df["customers_level_based"].value_counts()

agg_df = agg_df.groupby("customers_level_based").agg({"PRICE": "mean"})
agg_df.head()

agg_df = agg_df.reset_index()
agg_df.head()

# let's check. we expect each persona to be 1:
agg_df["customers_level_based"].value_counts()
agg_df.head()

###########################################
# TASK 7: Segment new customers (USA_ANDROID_MALE_0_18).
###########################################
# Segment by PRICE,
# add segments to agg_df with the naming "SEGMENT",
# describe the segments,
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])
agg_df.head(30)
agg_df.groupby("SEGMENT").agg({"PRICE": "mean"})

###########################################
# TASK 8: Classify the new customers and estimate how much income they can bring.
###########################################
# Which segment does a 33-year-old Turkish woman using ANDROID belong to and how much income is expected to earn on average?
new_user = "TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]

[agg_df["customers_level_based"] == new_user]

# In which segment and on average how much income would a 35 year old French woman using IOS earn?
new_user = "FRA_IOS_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]



