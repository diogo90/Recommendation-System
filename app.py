# Import packages

import streamlit as st 
import streamlit.components.v1 as stc

import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load crunchbase data (sourced using the API in Nov. 22)

def load_data(data):
	df = pd.read_csv(data, usecols=[1,2], dtype={'properties.identifier.value': str,'properties.short_description': str}, nrows=100) # Select organization name and description columns
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

	df = load_data("https://github.com/diogo90/Recommendation-System/blob/34a0ef2411085f74b833d862862ba60ccb8a69ad/london_organizations_crunchbase_nov_22.csv") # Load dataset

	if choice == "Home":
		st.subheader("Home")
		st.text("Below is a preview of the data sourced using the Crunchbase API (as off Nov. 22):")
		st.dataframe(df.head(5))

	elif choice == "Recommender":
		st.subheader("Recomend Organizations")
		cosine_sim = vectorize_text_to_cosine_matrix(df['properties.short_description'])

		search_term = st.text_input("Search")   # Create inbox to input text
		num_of_rec = st.sidebar.number_input("Number of recomendations", 3, 5, 3)  # Button to define number of courses one wants to recomend: 3 min; 5 max; 3 default
		if st.button("Recomend"):		# Create button and sets trigger to define events when clicked
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
