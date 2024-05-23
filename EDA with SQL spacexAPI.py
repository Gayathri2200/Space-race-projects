#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install sqlalchemy==1.3.9')


# ### Connect to the database
# 
# Let us first load the SQL extension and establish a connection with the database
# 

# In[ ]:


#Please uncomment and execute the code below if you are working locally.

#!pip install ipython-sql


# In[1]:


get_ipython().run_line_magic('load_ext', 'sql')


# In[2]:


import csv, sqlite3

con = sqlite3.connect("my_data1.db")
cur = con.cursor()


# In[3]:


get_ipython().system('pip install -q pandas==1.1.5')


# In[4]:


get_ipython().run_line_magic('sql', 'sqlite:///my_data1.db')


# In[6]:


import pandas as pd
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv")
df.to_sql("SPACEXTBL", con, if_exists='replace', index=False,method="multi")


# **Note:This below code is added to remove blank rows from table**
# 

# In[7]:


get_ipython().run_line_magic('sql', 'create table SPACEXTABLE as select * from SPACEXTBL where Date is not null')


# In[9]:


get_ipython().run_line_magic('sql', 'select * from SPACEXTBL limit 5')


# ## Tasks
# 
# Now write and execute SQL queries to solve the assignment tasks.
# 
# **Note: If the column names are in mixed case enclose it in double quotes
#    For Example "Landing_Outcome"**
# 
# ### Task 1
# 
# 
# 
# 
# ##### Display the names of the unique launch sites  in the space mission
# 

# In[10]:


get_ipython().run_line_magic('sql', 'select distinct("Launch_Site") from SPACEXTBL')


# 
# ### Task 2
# 
# 
# #####  Display 5 records where launch sites begin with the string 'CCA' 
# 

# In[13]:


get_ipython().run_line_magic('sql', 'select "Launch_Site" from SPACEXTBL where "Launch_Site" like \'CCA%\' limit 5')


# ### Task 3
# 
# 
# 
# 
# ##### Display the total payload mass carried by boosters launched by NASA (CRS)
# 

# In[18]:


get_ipython().run_line_magic('sql', 'select sum(PAYLOAD_MASS__KG_) from SPACEXTBL')


# ### Task 4
# 
# 
# 
# 
# ##### Display average payload mass carried by booster version F9 v1.1
# 

# In[19]:


get_ipython().run_line_magic('sql', 'select avg(PAYLOAD_MASS__KG_) from SPACEXTBL where "Booster_Version" = \'F9 v1.1\'')


# ### Task 5
# 
# ##### List the date when the first succesful landing outcome in ground pad was acheived.
# 
# 
# _Hint:Use min function_ 
# 

# In[20]:


get_ipython().run_line_magic('sql', 'select min(Date) from SPACEXTBL where "Landing_Outcome" = \'Success\'')


# ### Task 6
# 
# ##### List the names of the boosters which have success in drone ship and have payload mass greater than 4000 but less than 6000
# 

# In[31]:


get_ipython().run_cell_magic('sql', 'select "Booster_Version" ,"Landing_Outcome" from SPACEXTBL where "Landing_Outcome" = \'Success (drone ship)\' and "PAYLOAD_MASS__KG_" between 4000 and 6000', '      \n')


# ### Task 7
# 
# 
# 
# 
# ##### List the total number of successful and failure mission outcomes
# 

# In[36]:


get_ipython().run_line_magic('sql', 'select count("Mission_Outcome") from SPACEXTBL')


# ### Task 8
# 
# 
# 
# ##### List the   names of the booster_versions which have carried the maximum payload mass. Use a subquery
# 

# In[43]:


get_ipython().run_line_magic('sql', 'select "Booster_Version" from SPACEXTBL where "PAYLOAD_MASS__KG_"=(select min("PAYLOAD_MASS__KG_") from SPACEXTBL)')


# ### Task 9
# 
# 
# ##### List the records which will display the month names, failure landing_outcomes in drone ship ,booster versions, launch_site for the months in year 2015.
# 
# **Note: SQLLite does not support monthnames. So you need to use  substr(Date, 6,2) as month to get the months and substr(Date,0,5)='2015' for year.**
# 

# In[55]:


get_ipython().run_cell_magic('sql', 'select substr(Date,6,2) as month,"Landing_Outcome","Booster_Version","Launch_Site" from SPACEXTBL', '      where  substr(Date,0,5) = \'2015\' and "Landing_Outcome" = (select "Landing_Outcome" from SPACEXTBL where "Landing_Outcome" = \'Failure (drone ship)\') \n      \n')


# ### Task 10
# 
# 
# 
# 
# ##### Rank the count of landing outcomes (such as Failure (drone ship) or Success (ground pad)) between the date 2010-06-04 and 2017-03-20, in descending order.
# 

# In[60]:


get_ipython().run_line_magic('sql', 'select count("Landing_Outcome") from SPACEXTBL where Date between \'2010-06-04\' and \'2017-03-20\' order by Date desc')

