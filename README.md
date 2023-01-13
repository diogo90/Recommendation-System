# Crunchbase Organization Recommender

## Scope 

Self-development project focused on gaining practical understanding of building a recommendation system using cosine similarity and deploying it with Streamlit. The aim is to develop an approach to find similar organisations based on their profile description on Crunchbase. The short profile organizations’ descriptions tend to be focused on the core business model of a company and the market they are addressing. 

The premise lies on the fact that if any two organizations are operating within the same market space and doing the same things, they will use similar industry vocabulary to describe what they do. Which will consequently lead to a high cosine similarity between them.

To source organizations names and their description, I have used the Crunchbase API (details on Data Collection). Also, to limit the scope I have only collected data on organizations headquartered in London, UK.   

Please see below a diagram of all the steps involved:
![alt text](https://github.com/diogo90/Recommendation-System/blob/a24caebc458f7fa559af70a439336d14ee902d88/project_workflow.jpg)

## Data Collection

Data was collected using Crunchbase API (basic) and a detailed script with the process is uploaded in this repository with the name: data_collection_with_crunchbase_API.py. The data reflects all the organizations headquartered in London as off November 22 listed on Crunchbase. 

There are 51.6k organizations in total and the data file used is: london_organizations_crunchbase_nov_22.csv. If you would like to cross-check some of these organizations please head to:
https://www.crunchbase.com/discover/organization.companies/c2580402b9b8ab2fbde87855c26115b3

Even though I have collected more variables with the API script the only 2 used to create the cosine similarity matrix are the organization name and organization description.

## Streamlit implementation

The python code that creates the cosine similarity matrix and layout of the Streamlit app can be found in the file app.py. The app was deployed using Streamlit Cloud using Github. Please use the link below to access it:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://diogo90-recommendation-system-app-iob0aj.streamlit.app/)

## Limitations

If you check my app.py file in detail I am limiting the organizations file I am extracting from Crunchbase to 10k rows. That is because I am facing issues while
creating the cosine similarity matrix - with the entire dataset of 52k organizations the matrix gets too big to be uploaded on Streamlit Share. 
In case you find a solution to this problem please leave me a message on Github.

## Thank Yous

Appreciate all the content from YouTube channel https://www.youtube.com/@JCharisTech that allowed me to develop my skills in Streamlit and find some
inspiration for this project.
Appreciate the explanation on this article https://medium.com/priyanshumadan/extract-data-from-crunchbase-api-using-python-8e99ed6bc73e on how to use 
Crunchbase API.

