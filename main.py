import streamlit as st
import pandas as pd
import json
# Import your custom modules
from distance_calculator import calculate_distance
from scraper import get_acreage

# Set up the target coordinates as a constant
TARGET_COORDINATES = (33.383579662070005, -84.25380479849588)


def process_file(uploaded_file):
    df = pd.read_csv(uploaded_file)
    results = []

    for _, row in df.iterrows():
        # Construct the complete address
        address = f"{row['Address #'] if pd.notnull(row['Address #']) else ''} {row['Street']}, {row['City, Zip']}".strip()

        # Calculate distance to the point for each address
        distance = calculate_distance(address, TARGET_COORDINATES)

        # Get acreage using the parcel number
        acreage_info = get_acreage(row['Parcel Number'])

        # Combine the results
        result = {
            "ParcelNumber": row['Parcel Number'],
            "Address": address,
            "DistanceToPoint": distance,
            "Acreage": acreage_info.get('Acreage', 'Not Found')
        }
        results.append(result)

    return results


# Streamlit UI
st.title("Property Distance and Acreage Finder")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    if st.button('Search'):
        results = process_file(uploaded_file)
        st.json(results)
else:
    st.write("Upload a CSV file to get started.")

