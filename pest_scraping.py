
# coding: utf-8

# In[1]:


##import libraries
import requests
import bs4


# In[2]:


##get url
url = "http://www.agriculture.gov.au/pests-diseases-weeds/plant#identify-pests-diseases"


# In[3]:


data = requests.get(url)


# In[4]:


# parse the html using beautiful soup and store in variable `soup`
soup = bs4.BeautifulSoup(data.text,'html.parser',)


# In[5]:


# Take out the <ul> of name and get its value
right_table=soup.find('ul', class_='flex-container')
#right_table


# In[6]:


disease_name = []
image_link = []
urls = []
origin =[]

#Generate lists
for row in right_table.findAll("li"):
    disease_name.append(row.text.replace("\n",""))
    urls.append(row.find("a")["href"])
    image_link.append(row.find("img")["src"])
    


# In[7]:


##create a function for get data like  Origin - 
##See if you can identify the pest - Check what can legally come into Australia - Secure any suspect specimens
origin = []
specimens = []
identify_pest = []
legally_come_aus = []
def get_data(links):
    for link in links:
        ##Check data is presnnt in link or not
        if link[:21] == "/pests-diseases-weeds":
            quote_page = "http://www.agriculture.gov.au" + link
            page = requests.get(quote_page)
            soup1 = bs4.BeautifulSoup(page.text,'html.parser')
            ##take div to get pests data
            name_box = soup1.find('div', attrs={'class': 'pest-header-content'})
            if name_box is not None:
                name_list_items = name_box.find_all('strong')
                #Origin
                origin_name = name_list_items[1].next_sibling.strip()
                colasp = soup1.find('div', attrs={'id': 'collapsefaq'})
                colasp_list_items = colasp.findAll('div', attrs={'class': 'hide'})
                #See if you can identify the pest
                identify_pest_data = colasp_list_items[0].text
                #Check what can legally come into Australia 
                legally_come_ausdata = colasp_list_items[1].text
                #Secure any suspect specimens
                secure_suspect = colasp_list_items[2].text
            else:
                origin_name = "None"
                identify_pest_data = "None"
                legally_come_ausdata = "None"
                secure_suspect = "None"
            
        else:
            origin_name = "None"
            identify_pest_data = "None"
            legally_come_ausdata = "None"
            secure_suspect = "None"
            
        #append data
        origin.append(origin_name)
        identify_pest.append(identify_pest_data)
        legally_come_aus.append(legally_come_ausdata)
        specimens.append(secure_suspect)
    print("All Data Saved!")
    return
        
    


# In[8]:


#Import os to get directory path
import os
path = os.getcwd()


# In[9]:


localy_save_img = []
#Function for download images and get image local path
def download_image_series(imgages_links): 
  
    for img_link in imgages_links: 
  
        '''iterate through all links in video_links 
        and download them one by one'''
        link = "http://www.agriculture.gov.au"+img_link
        # obtain filename by splitting url and getting  
        # last string 
        file_name = link.split('/')[-1]    
  
        #print("Downloading file:%s"%file_name) 
          
        # create response object 
        r = requests.get(link, stream = True) 
          
        # download started 
        with open(file_name, 'wb') as f: 
            for chunk in r.iter_content(chunk_size = 1024*1024): 
                if chunk: 
                    f.write(chunk) 
          
        #print("%s downloaded!\n"%file_name)
        local_img = path+"\\"+ file_name
        localy_save_img.append(local_img)
    print("All videos downloaded!")
    return
  
  
 


# In[10]:


if __name__ == "__main__": 
    # download all images 
    get_data(urls)
    download_image_series(image_link)


# In[13]:


len(origin)


# In[15]:


#import pandas to convert list to data frame
import pandas as pd
df=pd.DataFrame(disease_name,columns=['Disease name'])
df['Image link']=image_link
df['Origin']=origin
df['Local Image path'] = localy_save_img
df['See if you can identify the pest'] = identify_pest
df['Check what can legally come into Australia'] = legally_come_aus
df['Secure any suspect specimens'] = specimens


# In[16]:


df.head()


# In[17]:


df.tail()


# In[18]:


df.to_csv('pests.csv', index=False, encoding='utf-8')

