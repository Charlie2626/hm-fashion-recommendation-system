H&M Personalized Fashion Recommendation System

A machine learning powered fashion recommendation dashboard built using the H&M Kaggle dataset.
This project generates personalized clothing recommendations based on customer purchase behavior, product similarity, and popularity scoring.

Features
Personalized product recommendations
Recommendation score visualization
Product image display
Customer segmentation summary
Interactive dashboard (Streamlit)
Ranking + scoring recommendation engine
Visual recommendation cards
Dashboard Preview

How It Works

The recommendation system combines:

Popularity Model
Collaborative Filtering
Purchase History Model
Ranking + Score Normalization

Final recommendations are generated using weighted scoring.

Tech Stack

Python
Pandas
Scikit-learn
Streamlit
Matplotlib
NumPy

Project Structure
app.py                → Streamlit dashboard  
src/recommender.py    → recommendation logic  
src/formatting.py     → display formatting  
src/image_utils.py    → image loading  
data/                 → datasets  
images/               → product images  
Run Locally

Install dependencies:

pip install -r requirements.txt

Run dashboard:

streamlit run app.py
Dataset

H&M Personalized Fashion Recommendations (Kaggle)

Author

Charlie Beverly