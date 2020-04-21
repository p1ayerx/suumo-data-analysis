#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import pandas_profiling as pdp
from sklearn import preprocessing
from sklearn.preprocessing import OrdinalEncoder


# In[2]:


df = pd.read_csv("suumo.csv",encoding="utf-16")


# In[3]:


i = 1
for r in ["立地1","立地2","立地3"]:
    locals()["sp" + str(i)] = df[r].str.split(" 歩",expand=True)
    locals()["sp" + str(i)].columns = [r+"1",r+"2"]
    i += 1
    
sp4 = df['敷/礼/保証/敷引,償却'].str.split('/', expand=True)
sp4.columns = ['敷金', '礼金']


# In[4]:


df = pd.concat([df,sp1,sp2,sp3,sp4], axis=1)
df.drop(['立地1','立地2','立地3','敷/礼/保証/敷引,償却'], axis=1, inplace=True)


# In[5]:


df = df.dropna(subset=["賃料料"])


# In[6]:


df["賃料料"] = df["賃料料"].str.replace(u"万円", u"")
df["敷金"] = df["賃料料"].str.replace(u"万円", u"")
df["礼金"] = df["礼金"].str.replace(u"万円", u"")
df["管理費"] = df["管理費"].str.replace(u"円",u"")
df["築年数"] = df["築年数"].str.replace(u"新築",u"0")
df["築年数"] = df["築年数"].str.replace(u"99年以上",u"0")
df["築年数"] = df["築年数"].str.replace(u"築",u"")
df["築年数"] = df["築年数"].str.replace(u"年",u"")
df["専有面積"] = df["専有面積"].str.replace(u"m",u"")
df["立地12"] = df["立地12"].str.replace(u"分",u"")
df["立地22"] = df["立地22"].str.replace(u"分",u"")
df["立地32"] = df["立地32"].str.replace(u"分",u"")


# In[7]:


for x in ["管理費","敷金","礼金"]:
    df[x] = df[x].replace("-",0)


# In[8]:


i = 5
j = 1
for r in ["立地11","立地21","立地31"]:
    locals()["sp"+str(i)] = df[r].str.split("/",expand=True)
    locals()["sp"+str(i)].columns = ["路線"+str(j),"駅"+str(j)]
    locals()["sp"+str(i)]["徒歩"+str(j)] = df[r[:-1]+"2"]
    i += 1
    j += 1


# In[9]:


df = pd.concat([df, sp5, sp6, sp7], axis=1)

df.drop(['立地11','立地12','立地21','立地22','立地31','立地32'], axis=1, inplace=True)


# In[10]:


for x in ["管理費","賃料料","敷金","礼金","築年数","専有面積","徒歩1","徒歩2","徒歩3"]:
    df[x] = pd.to_numeric(df[x])
    
for x in ["賃料料","敷金","礼金"]:
    df[x] = df[x] * 10000


# In[11]:


sp8 = df['階層'].str.split('-', expand=True)
sp8.columns = ['階1', '階2']
sp8['階1'].str.encode('cp932')
sp8['階1'] = sp8['階1'].str.replace(u'階', u'')
sp8['階1'] = sp8['階1'].str.replace(u'B', u'-')
sp8['階1'] = sp8['階1'].str.replace(u'M', u'')
sp8['階1'] = pd.to_numeric(sp8['階1'])


# In[12]:


df = pd.concat([df, sp8], axis=1)


# In[13]:


df['建物の高さ'] = df['建物の高さ'].str.replace(u'地下1地上', u'')
df['建物の高さ'] = df['建物の高さ'].str.replace(u'地下2地上', u'')
df['建物の高さ'] = df['建物の高さ'].str.replace(u'地下3地上', u'')
df['建物の高さ'] = df['建物の高さ'].str.replace(u'地下4地上', u'')
df['建物の高さ'] = df['建物の高さ'].str.replace(u'地下5地上', u'')
df['建物の高さ'] = df['建物の高さ'].str.replace(u'地下6地上', u'')
df['建物の高さ'] = df['建物の高さ'].str.replace(u'地下7地上', u'')
df['建物の高さ'] = df['建物の高さ'].str.replace(u'地下8地上', u'')
df['建物の高さ'] = df['建物の高さ'].str.replace(u'地下9地上', u'')
df['建物の高さ'] = df['建物の高さ'].str.replace(u'平屋', u'1')
df['建物の高さ'] = df['建物の高さ'].str.replace(u'階建', u'')


# In[14]:


df['建物の高さ'] = pd.to_numeric(df['建物の高さ'])


# In[15]:


df = df.reset_index(drop=True)


# In[16]:


df["間取りDK"] = 0
df["間取りK"] = 0
df["間取りL"] = 0
df["間取りS"] = 0
df["間取り"] = df["間取り"].str.replace(u"ワンルーム",u"1")


# In[17]:


def madori(x):
    for i in range(len(df)):
        if x in df["間取り"][i]:
            df.loc[i,"間取り"+x] = 1
    df["間取り"] = df["間取り"].str.replace(x,u"")


# In[18]:


for x in ["DK","K","L","S"]:
    madori(x)


# In[19]:


df["間取り"] = pd.to_numeric(df["間取り"])


# In[20]:


sp9 = df['住所'].str.split('区', expand=True)
sp9.columns = ['区', '市町村']
sp9['区'] = sp9['区'] + '区'
sp9['区'] = sp9['区'].str.replace('東京都','')
df = pd.concat([df, sp9], axis=1)


# In[21]:


df[['路線1','路線2','路線3', '駅1', '駅2','駅3','市町村']] = df[['路線1','路線2','路線3', '駅1', '駅2','駅3','市町村']].fillna("NAN")


# In[22]:


oe = preprocessing.OrdinalEncoder()
df[['路線1','路線2','路線3', '駅1', '駅2','駅3','市町村']] = oe.fit_transform(df[['路線1','路線2','路線3', '駅1', '駅2','駅3','市町村']].values) 


# In[23]:


df['賃料料+管理費'] = df['賃料料'] + df['管理費']


# In[24]:


#上限設定
df = df[df["賃料料+管理費"]<150000]


# In[25]:


df = df[["マンション名",'賃料料+管理費', '築年数', '建物の高さ', '階1',
       '専有面積','路線1','路線2','路線3', '駅1', '駅2','駅3','徒歩1', '徒歩2','徒歩3','間取り', '間取りDK', '間取りK', '間取りL', '間取りS',
       '市町村','詳細URL']]

df.columns = ['name','real_rent','age', 'height', 'level','area', 'route_1','route_2','route_3','station_1','station_2','station_3','distance_1','distance_2','distance_3','rooms','DK','K','L','S','address',"url"]


# In[29]:


df["per_area"] = df["area"]/df["rooms"]
df["height_level"] = df["height"]*df["level"]
df["area_height_level"] = df["area"]*df["height_level"]
df["distance_staion_1"] = df["station_1"]*df["distance_1"]
df["per_area"] = df["area"]/df["rooms"]
df["height_level"] = df["height"]*df["level"]
df["area_height_level"] = df["area"]*df["height_level"]
df["distance_staion_1"] = df["station_1"]*df["distance_1"]


# In[31]:


df


# In[33]:


df.to_csv('cleaned.csv', encoding='utf-16', header=True, index=False)


# In[ ]:


# pdp.ProfileReport(df).to_file(output_file="eda.html")


# In[ ]:




