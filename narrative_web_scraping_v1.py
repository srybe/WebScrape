#!/usr/bin/env python
# coding: utf-8

# In[55]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import pandas as pd
import time


# In[56]:


driver = webdriver.Chrome()


# In[57]:


driver.get("https://niemanstoryboard.org/storyboard-category/narrative-news/")


# In[49]:


# Uncomment this line to debug in a specific page 
#driver.get("https://niemanstoryboard.org/storyboard-category/narrative-news/page/21/")


# In[58]:


list_of_elements = []

try:
    while True:
        try:
            articleNumber = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, "//p[@class='teaser-txt']/a"))
            )
        except:
            print("CANNOT GET THE LIST OF NEWS IN THE PAGE... ")
            break
        print ("Length of the article: ", len(articleNumber))
        for article_element in articleNumber:
            print(article_element.get_attribute("href"))
            try:
                # Making it click on the article.
                
                driver.get(article_element.get_attribute("href"))
                
                
                url = driver.current_url

                try:
                    title = WebDriverWait(driver, 20).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, "article-h1"))
                    )

                    articleTitle = title.text
                except TimeoutException:
                    print("Cannot get the news title")
                    articleTitle = ""

                try:
                    # grabbing the content of the article
                    content = WebDriverWait(driver, 20).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//p[not(@class)]"))
                    )

                    articleContent = "\n".join(p.text for p in content)
                except TimeoutException:
                    print("Cannot get news body")
                    articleContent = ""
                
                list_of_elements.append([driver.current_url, articleTitle, articleContent])
                df = pd.DataFrame(list_of_elements, columns=['News link', 'News title', 'News body'])
                df.to_excel("narrative_news_dataset.xlsx", index=False, engine="openpyxl")
                
            except StaleElementReferenceException:
                print("Exception occurred. Moving to another article.")

            finally:
                # go back
                driver.back()

        try:
            nextPage = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "arrow.right"))
            )
            
            nextPage.click()
            time.sleep(1)
        except TimeoutException:
            print("Cannot change the page")
            break  

except Exception as e:
    print(f"An error occurred: {e}")

df.to_excel("narrative_news_dataset.xlsx", index = False, engine = "openpyxl")


# In[54]:


driver.quit()


# In[ ]:





# In[ ]:




