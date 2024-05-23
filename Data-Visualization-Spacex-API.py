#!/usr/bin/env python
# coding: utf-8

# # **SpaceX  Falcon 9 First Stage Landing Prediction**
# 

#  ## Assignment: Exploring and Preparing Data
# 

#   ## Objectives
# Perform exploratory Data Analysis and Feature Engineering using `Pandas` and `Matplotlib`
# 
# - Exploratory Data Analysis
# - Preparing Data  Feature Engineering 
# 

# ----
# 

# ### Import Libraries and Define Auxiliary Functions
# 

# We will import the following libraries the lab 
# 
# 

# In[1]:


# andas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
#NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns


# ## Exploratory Data Analysis 
# 

# First, let's read the SpaceX dataset into a Pandas dataframe and print its summary
# 

# In[2]:


df=pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv")

# If you were unable to complete the previous lab correctly you can uncomment and load this csv

# df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/dataset_part_2.csv')

df.head(5)


# First, let's try to see how the `FlightNumber` (indicating the continuous launch attempts.) and `Payload` variables would affect the launch outcome.
# 
# We can plot out the <code>FlightNumber</code> vs. <code>PayloadMass</code>and overlay the outcome of the launch. We see that as the flight number increases, the first stage is more likely to land successfully. The payload mass is also important; it seems the more massive the payload, the less likely the first stage will return.
# 

# In[3]:


sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class", data=df, aspect = 5)
plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("Pay load Mass (kg)",fontsize=20)
plt.show()


# Next, let's drill down to each site visualize its detailed launch records.
# 

# ### TASK 1: Visualize the relationship between Flight Number and Launch Site
# 

# Use the function <code>catplot</code> to plot <code>FlightNumber</code> vs <code>LaunchSite</code>, set the  parameter <code>x</code>  parameter to <code>FlightNumber</code>,set the  <code>y</code> to <code>Launch Site</code> and set the parameter <code>hue</code> to <code>'class'</code>
# 

# In[4]:


# Plot a scatter point chart with x axis to be Flight Number and y axis to be the launch site, and hue to be the class value
sns.catplot(y ='LaunchSite',x ='FlightNumber', hue ='Class',data = df,aspect = 2)
plt.xlabel("FlightNumber")
plt.ylabel("LaunchSite")
plt.show()


# Now try to explain the patterns you found in the Flight Number vs. Launch Site scatter point plots.
# 

# ### TASK 2: Visualize the relationship between Payload and Launch Site
# 

# We also want to observe if there is any relationship between launch sites and their payload mass.
# 

# In[5]:


# Plot a scatter point chart with x axis to be Pay Load Mass (kg) and y axis to be the launch site, and hue to be the class value
sns.catplot(y = 'LaunchSite', x='PayloadMass',data = df,hue = 'Class',aspect =2)
plt.xlabel("Payload Mass")
plt.ylabel("Launch Site")
plt.show()


# Now if you observe Payload Vs. Launch Site scatter point chart you will find for the VAFB-SLC  launchsite there are no  rockets  launched for  heavypayload mass(greater than 10000).
# 

# ### TASK  3: Visualize the relationship between success rate of each orbit type
# 

# Next, we want to visually check if there are any relationship between success rate and orbit type.
# 

# Let's create a `bar chart` for the sucess rate of each orbit
# 

# In[8]:


# HINT use groupby method on Orbit column and get the mean of Class column
ds = df.groupby('Orbit')['Class'].mean()
ds.plot(kind ='bar')
plt.show()


# Analyze the ploted bar chart try to find which orbits have high sucess rate.
# 

# ### TASK  4: Visualize the relationship between FlightNumber and Orbit type
# 

# For each orbit, we want to see if there is any relationship between FlightNumber and Orbit type.
# 

# In[9]:


# Plot a scatter point chart with x axis to be FlightNumber and y axis to be the Orbit, and hue to be the class value
sns.catplot(x ='FlightNumber',y='Orbit',data = df,hue = 'Class', aspect = 2)
plt.xlabel("Flightnumber")
plt.ylabel("Orbit")
plt.show()


# You should see that in the LEO orbit the Success appears related to the number of flights; on the other hand, there seems to be no relationship between flight number when in GTO orbit.
# 

# ### TASK  5: Visualize the relationship between Payload and Orbit type
# 

# Similarly, we can plot the Payload vs. Orbit scatter point charts to reveal the relationship between Payload and Orbit type
# 

# In[10]:


# Plot a scatter point chart with x axis to be Payload and y axis to be the Orbit, and hue to be the class value
sns.catplot(x = 'PayloadMass', y ='Orbit',data = df,hue = 'Class', aspect = 2)
plt.xlabel("PayloadMass")
plt.ylabel("Orbit")
plt.show()


# With heavy payloads the successful landing or positive landing rate are more for Polar,LEO and ISS.   
# 
# However for GTO we cannot distinguish this well as both positive landing rate and negative landing(unsuccessful mission) are both there here.
# 
# 
# 

# ### TASK  6: Visualize the launch success yearly trend
# 

# You can plot a line chart with x axis to be <code>Year</code> and y axis to be average success rate, to get the average launch success trend. 
# 

# The function will help you get the year from the date:
# 

# In[11]:


# A function to Extract years from the date 
year=[]
def Extract_year(date):
    for i in df["Date"]:
        year.append(i.split("-")[0])
    return year
Year = Extract_year(df['Date'])   


# In[12]:


Year


# In[14]:


# Plot a line chart with x axis to be the extracted year and y axis to be the success rate
sns.lineplot(x = Year, y='Class' ,data=df )
plt.xlabel("Extracted_year")
plt.ylabel("Class")
plt.show()


# You can observe that the success rate since 2013 kept increasing till 2017 (stable in 2014) and after 2015 it started increasing.
# 

# ## Features Engineering 
# 

# By now, you should obtain some preliminary insights about how each important variable would affect the success rate, we will select the features that will be used in success prediction in the future module.
# 

# In[15]:


features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]
features.head()


#  ### TASK  7: Create dummy variables to categorical columns
# 

# Use the function <code>get_dummies</code> and <code>features</code> dataframe to apply OneHotEncoder to the column <code>Orbits</code>, <code>LaunchSite</code>, <code>LandingPad</code>, and <code>Serial</code>. Assign the value to the variable <code>features_one_hot</code>, display the results using the method head. Your result dataframe must include all features including the encoded ones.
# 

# In[16]:


# HINT: Use get_dummies() function on the categorical columns
features_one_hot = pd.get_dummies(features)
features_one_hot


# ### TASK  8: Cast all numeric columns to `float64`
# 

# Now that our <code>features_one_hot</code> dataframe only contains numbers cast the entire dataframe to variable type <code>float64</code>
# 

# In[17]:


# HINT: use astype function
features_one_hot = features_one_hot.astype(float)


# In[18]:


features_one_hot.dtypes


# We can now export it to a <b>CSV</b> for the next section,but to make the answers consistent, in the next lab we will provide data in a pre-selected date range. 
# 

# <code>features_one_hot.to_csv('dataset_part_3.csv', index=False)</code>
# 
