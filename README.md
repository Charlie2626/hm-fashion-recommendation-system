H&M Personalized Fashion Recommendation System

Machine learning fashion recommender with an interactive Streamlit dashboard that generates personalized clothing recommendations using customer behavior and product similarity.

Dashboard Preview

Features

• Personalized product recommendations
• Recommendation score visualization
• Product image display
• Customer segmentation summary
• Interactive Streamlit dashboard
• Ranking + scoring recommendation engine
• Visual recommendation cards

Recommendation Engine

This system combines multiple recommendation strategies:

Popularity Model
Collaborative Filtering
Purchase History Model
Ranking + Score Normalization

These models are merged into a final weighted recommendation score.

Tech Stack

Python
Pandas
NumPy
Scikit-learn
Streamlit
Matplotlib

Project Structure
app.py
src/
 ├── recommender.py
 ├── formatting.py
 └── image_utils.py

screenshots/
images/
Run Locally

Install dependencies

pip install -r requirements.txt

Run dashboard

streamlit run app.py
Dataset

H&M Personalized Fashion Recommendations — Kaggle

Author

Charlie Beverly
