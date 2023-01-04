# Crunchbase Organization Recommender

## Scope 

Self-development project focused on gaining practical understanding of building a recommendation system using cosine similarity and deploying it with Streamlit. The aim is to develop an approach to find similar organisations based on their profile description on Crunchbase. The short profile organizations’ descriptions tend to be focused on the core business model of a company and the market they are addressing. 

The premise lies on the fact that if any two organizations are operating within the same market space and doing the same things, they will use similar industry vocabulary to describe what they do. Which will consequently lead to a high cosine similarity between them.

To source organizations names and their description, I have used the Crunchbase API (details on Data Collection). Also, to limit the scope I have only collected data on organizations headquartered in London, UK.   

Please see below a diagram of all the steps involved:
![alt text](https://github.com/diogo90/Recommendation-System/blob/a24caebc458f7fa559af70a439336d14ee902d88/project_workflow.jpg)
