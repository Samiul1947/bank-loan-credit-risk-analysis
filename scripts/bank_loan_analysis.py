#!/usr/bin/env python
# coding: utf-8

# # BANK LOAN ANALYSIS REPORT

# ### Import Libraries

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import plotly.express as px


# In[2]:


df = pd.read_excel("C:/Users/ADMIN/Downloads/Bank_loan_data.xlsx")


# In[3]:


df.head()


# In[4]:


df.tail()


# ## Metadata of Data

# In[5]:


print("No of Rows:", df.shape[0])


# In[6]:


print("No of Columns:", df.shape[1])


# In[7]:


df.info()


# ## Data types

# In[8]:


df.dtypes


# In[9]:


df.describe()


# ## Total Loan Applications

# In[11]:


total_loan_applictions = df['id'].count()
print("Total Loan Applications:",total_loan_applictions)


# ## MTD Total Loan Applications

# In[12]:


latest_issue_date = df['issue_date'].max()
latest_year = latest_issue_date.year
latest_month = latest_issue_date.month

mtd_data = df[(df['issue_date'].dt.year == latest_year) & (df['issue_date'].dt.month == latest_month)]

mtd_loan_applications = mtd_data['id'].count()

print(f"MTD Loan Applications(for {latest_issue_date.strftime('%B %Y')}):{mtd_loan_applications}")


# ## Total Funded Amount

# In[13]:


total_funded_amount = df['loan_amount'].sum()
total_funded_amount_millions = total_funded_amount/ 1000000
print("Total Funded Amount : ${:.2f}M".format(total_funded_amount_millions))


# ## Total Amount Received

# In[14]:


total_funded_amount = df['total_payment'].sum()
total_funded_amount_millions = total_funded_amount/ 1000000
print("Total Amount Received: ${:.2f}M".format(total_funded_amount_millions))


# ## Average Interest Rate

# In[15]:


avg_interest_rate = df['int_rate'].mean()*100
print("Average Interest Rate: {:.2f}%".format(avg_interest_rate))


# ## Average Debt-to-Income Ratio (DTI)

# In[16]:


avg_dti = df['dti'].mean()*100
print("Average DTI: {:.2f}%".format(avg_dti))


# ## Good Loan Metrics

# In[17]:


good_loans = df[df['loan_status'].isin(["Fully Paid","Current"])]

total_loan_applications= df['id'].count()

good_loan_applications = good_loans['id'].count()
good_loan_funded_amount = good_loans['loan_amount'].sum()
good_loan_received = good_loans['total_payment'].sum()

good_loan_funded_amount_million = good_loan_funded_amount /1000000
good_loan_received_millions = good_loan_received /1000000

good_loan_percentage = (good_loan_applications /total_loan_applications)*100

print("Good Loan Applications",good_loan_applications)
print("Good Loan Funded Amount(in millions): ${:.2f}M".format(good_loan_funded_amount_million))
print("Good Loan Total Received (in millions): ${:.2f}M".format(good_loan_received_millions))
print("Percentage of Good Loan Total Applications: {:.2f}%".format(good_loan_percentage))


# ## Bad Loan Metrics

# In[18]:


bad_loans = df[df['loan_status'].isin(["Charged Off"])]

total_loan_applications= df['id'].count()

bad_loan_applications = bad_loans['id'].count()
bad_loan_funded_amount = bad_loans['loan_amount'].sum()
bad_loan_received = bad_loans['total_payment'].sum()

bad_loan_funded_amount_million = bad_loan_funded_amount /1000000
bad_loan_received_millions = bad_loan_received /1000000

bad_loan_percentage = (bad_loan_applications /total_loan_applications)*100

print("Bad Loan Applications",bad_loan_applications)
print("Bad Loan Funded Amount(in millions): ${:.2f}M".format(bad_loan_funded_amount_million))
print("Bad Loan Total Received (in millions): ${:.2f}M".format(bad_loan_received_millions))
print("Percentage of Bad Loan Total Applications: {:.2f}%".format(bad_loan_percentage))


# ## Total Loan Applications By Month

# In[19]:


monthly_applications = (
    df.sort_values('issue_date')
    .assign(month_name=lambda x: x['issue_date'].dt.strftime('%b %Y'))
    .groupby('month_name', sort=False)['id']
    .count()
    .reset_index(name='loan_applications_count')
)

plt.figure(figsize=(10,5))
plt.fill_between(monthly_applications['month_name'],monthly_applications['loan_applications_count'],
                 color='orange',alpha=0.5)
plt.plot(monthly_applications['month_name'],monthly_applications['loan_applications_count'],
                 color='black',linewidth=2)

for i, row in monthly_applications.iterrows():
    plt.text(i, row['loan_applications_count'] + 0.5,f"{row['loan_applications_count']}",
             ha='center' ,va='bottom' ,fontsize=9, rotation=0 ,color='black')

plt.title('Total Loan Applications By Month', fontsize=14)
plt.xlabel('Month')
plt.ylabel('Number of Applications')
plt.xticks(ticks=range(len(monthly_applications)), labels=monthly_applications['month_name'], rotation=45)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()


# ## Regional Analysis By State For Total Funded Amount

# In[20]:


state_funding = df.groupby('address_state')['loan_amount'].sum().sort_values(ascending=True)
state_funding_thousands = state_funding / 1000

plt.figure(figsize=(10,8))
bars = plt.barh(state_funding_thousands.index, state_funding_thousands.values, color='lightcoral')

for bar in bars:
    width = bar.get_width()
    plt.text(width + 10, bar.get_y() + bar.get_height() / 2,
             f'{width:,.0f}K' , va='center' ,fontsize=9)

plt.title('Total Funded Amount by State (in Rs Thousands)')
plt.xlabel('Funded Amount (Rs\'000)')
plt.ylabel('State')
plt.tight_layout()
plt.show()


# ## Regional Analysis By State For Total Received Amount

# In[21]:


state_received_amount = df.groupby('address_state')['total_payment'].sum().sort_values(ascending=True)
state_received_amount_thousands = state_received_amount / 1000

plt.figure(figsize=(10,8))
bars = plt.barh(state_received_amount_thousands.index, state_received_amount_thousands.values, color='lightblue')

for bar in bars:
    width = bar.get_width()
    plt.text(width + 10, bar.get_y() + bar.get_height() / 2,
             f'{width:,.0f}K' , va='center' ,fontsize=9)

plt.title('Total Received Amount by State (in Rs Thousands)')
plt.xlabel('Received Amount (Rs\'000)')
plt.ylabel('State')
plt.tight_layout()
plt.show()


# ## Loan Term Analysis By Total Funded Amount

# In[22]:


term_funding_millions = df.groupby('term')['loan_amount'].sum() / 1000000

plt.figure(figsize=(5,5))
plt.pie(
    term_funding_millions,
    labels=term_funding_millions.index,
    autopct=lambda p: f"{p:.1f}%\n${p*sum( term_funding_millions)/100:.1f}M",
    startangle=90,
    wedgeprops={'width':0.4}
)
plt.gca().add_artist(plt.Circle((0,0),0.70,color='white'))
plt.title("Total Funded Amount By Term (in $ Millions)")
plt.show()


# ## Loan Term Analysis By Total Received Amount

# In[23]:


term_received_millions = df.groupby('term')['total_payment'].sum() / 1000000

plt.figure(figsize=(5,5))
plt.pie(
    term_received_millions,
    labels=term_received_millions.index,
    autopct=lambda p: f"{p:.1f}%\n${p*sum(term_received_millions)/100:.1f}M",
    startangle=90,
    wedgeprops={'width':0.4}
)
plt.gca().add_artist(plt.Circle((0,0),0.70,color='white'))
plt.title("Total Received Amount By Term (in $ Millions)")
plt.show()


# ## Employee Length By Total Funded Amount

# In[24]:


emp_funding = df.groupby('emp_length')['loan_amount'].sum().sort_values()/1000

plt.figure(figsize=(10,6))
bars = plt.barh(emp_funding.index, emp_funding.values, color='red')

for bar in bars:
    width = bar.get_width()
    plt.text(width + 5, bar.get_y() + bar.get_height() / 2,
             f'{width:,.0f}K' , va='center' ,fontsize=9)

plt.title('Total Funded Amount By Employment Length')
plt.xlabel('Funded Amount (Rs Thousands)')
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()


# ## Employee Length By Total Received Amount

# In[25]:


emp_received_amount= df.groupby('emp_length')['total_payment'].sum().sort_values()/1000

plt.figure(figsize=(10,6))
bars = plt.barh(emp_received_amount.index, emp_received_amount.values, color='violet')

for bar in bars:
    width = bar.get_width()
    plt.text(width + 5, bar.get_y() + bar.get_height() / 2,
             f'{width:,.0f}K' , va='center' ,fontsize=9)

plt.title('Total Received Amount By Employment Length')
plt.xlabel('Received Amount (Rs Thousands)')
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()


# ## Loan Purpose By Total Funded Amount

# In[26]:


purpose_funding_millions = (df.groupby('purpose')['loan_amount'].sum().sort_values()/1000000)

plt.figure(figsize=(10,6))
bars = plt.barh(purpose_funding_millions.index, purpose_funding_millions.values, color='grey')

for bar in bars:
    width = bar.get_width()
    plt.text(width + 0.1, bar.get_y() + bar.get_height() / 2,
             f'{width:,.2f}M' , va='center' ,fontsize=9)

plt.title('Total Funded Amount by Loan Purpose (in millions)', fontsize=14)
plt.xlabel('Funded Amount (in millions)')
plt.ylabel('Loan Purpose')
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()


# ## Loan Purpose By Total Received Amount

# In[27]:


purpose_received_millions = (df.groupby('purpose')['total_payment'].sum().sort_values()/1000000)

plt.figure(figsize=(10,6))
bars = plt.barh(purpose_received_millions.index, purpose_received_millions.values, color='grey')


for bar in bars:
    width = bar.get_width()
    plt.text(width + 0.1, bar.get_y() + bar.get_height() / 2,
             f'{width:,.2f}M' , va='center' ,fontsize=9)

plt.title('Total Received Amount by Loan Purpose (in millions)', fontsize=14)
plt.xlabel('Received Amount (in millions)')
plt.ylabel('Loan Purpose')
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()


# ## Home Ownership By Total Funded Amount

# In[28]:


home_funding = df.groupby('home_ownership')['loan_amount'].sum().reset_index()
home_funding['loan_amount_million'] = home_funding['loan_amount'] / 1000000

fig = px.treemap(
    home_funding,
    path=['home_ownership'],
    values='loan_amount_million',
    color='loan_amount_million',
    color_continuous_scale='Blues',
    title='Total Funded Amount by Home Ownership (in millions)'

)

fig.show()


# ## Home Ownership By Total Received Amount

# In[29]:


home_received_amount = df.groupby('home_ownership')['total_payment'].sum().reset_index()
home_received_amount['total_payment_million'] =home_received_amount['total_payment'] / 1000000

fig = px.treemap(
    home_received_amount ,
    path=['home_ownership'],
    values='total_payment_million',
    color='total_payment_million',
    color_continuous_scale='reds',
    title='Total Received Amount by Home Ownership (in millions)'

)

fig.show()


# In[ ]:




