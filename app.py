# Import packages

import streamlit as st 
import streamlit.components.v1 as stc

import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

# Load crunchbase data (sourced using the API in Nov. 22)

def load_data(data):
	# Select organization name and description columns
	df = pd.read_csv(data, usecols=[1,2], dtype={'properties.identifier.value': str,'properties.short_description': str}, nrows=10000) 
	df.dropna(inplace=True) # Drop null values

	return df 


# Create function to vectorize data and calculate cosine similarity

def vectorize_text_to_cosine_matrix(data):
	count_vect = CountVectorizer()  # Initialize count vectorizer
	cv_matrix = count_vect.fit_transform(data)  # Transform data and create matrix

	cosine_sim = cosine_similarity(cv_matrix)  # Calculate cosine similarity

	return cosine_sim


# Creat recommendation function
@st.cache
def get_recommendation(title, cosine_sim, df, num_of_rec=3):
	org_indices = pd.Series(df.index, index=df['properties.identifier.value']).drop_duplicates() # Get indices of the organizations
	# properties.identifier.value is the organization name

	idx =  org_indices[title] # Index of organization i.e. organization name

	# Look into cosine matrix for that index
	sim_scores = list(enumerate(cosine_sim[idx])) # Pass the index into cosine similarity matrix
	sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True) # Sort similarity scores by score column starting with highest
	selected_organizations_indices = [i[0] for i in sim_scores[1:]] # Get the index of the organization omitting 1st result
	selected_organizations_scores = [i[1] for i in sim_scores[1:]] # Get the score of the organization omitting 1st result

	# Return de dataframe and title
	result_df = df.iloc[selected_organizations_indices]
	result_df['similarity_score'] = selected_organizations_scores # Add a column with the similarity score

	return result_df.head(num_of_rec)


# Build the main app layout 

def main():

	st.title("Crunchbase organization recommender") # App title

	menu = ["Home", "Recommender", "About"] # Define 3 menus

	choice = st.sidebar.selectbox("Menu", menu) # Menu selection
	
	file_path = Path(__file__).parents[0] / 'london_organizations_crunchbase_nov_22.csv'
	
	df = load_data(file_path) # Load dataset

	if choice == "Home":
		st.subheader("Scope")
		st.text("Self-development project focused on gaining practical understanding of building a")
		st.text("recommendation system using cosine similarity and deploying it with Streamlit.")
		st.text("The aim is to develop an approach to find similar organisations based on their profile")
		st.text("description on Crunchbase. The short profile organizations’ descriptions tend to be focused")
		st.text("on the core business model of a company and the market they are addressing. The premise")
		st.text("lies on the fact that if any two organizations are operating within the same market space and")
		st.text("doing the same things, they will use similar industry vocabulary to describe what they do.") 
		st.text("Which will consequently lead to a high cosine similarity between them.")
		st.text("To source organizations names and their description, I have used the Crunchbase API (details on Data Collection).")
		st.text("Also, to limit the scope I have only collected data on organizations headquartered in London, UK.")
		st.text("Below is a preview of the data sourced using the Crunchbase API (as off Nov. 22):")
		st.dataframe(df.head(5))
		st.text("Please head to the Recommender tab to test the tool")

	elif choice == "Recommender":
		st.subheader("Recomend Organizations")
		cosine_sim = vectorize_text_to_cosine_matrix(df['properties.short_description'])

		search_term = st.text_input("Search")   # Create inbox to input text
		# Button to define number of courses one wants to recomend: 3 min; 5 max; 3 default
		num_of_rec = st.sidebar.number_input("Number of recomendations", 3, 5, 3)  
		# Create button and sets trigger to define events when clicked
		if st.button("Recomend"):		
			if search_term is not None: # Make sure there is a search term
				try:
					result = get_recommendation(search_term, cosine_sim, df, num_of_rec)

					# Show the results in the app with the code below
					for row in result.iterrows():
						rec_title = row[1][0] # Name of organization
						rec_desc = row[1][1] # Organization description
						rec_score = row[1][2] # Organization score 

						st.write("Title: ", rec_title)
						st.write("Description: ", rec_desc)
						st.write("Score: ", rec_score)

				except:
					result = "Sorry, can't find similar Organizations to this one. Most likely because it was not listed on Crunchbase as an organization headquartered in London as off Nov. 2022"
					st.write(result)


	else:
		st.subheader("About")
		st.text("This app was built using Python 3.9.12 and Streamlit 1.16.0")


if __name__ == '__main__':
	main()
