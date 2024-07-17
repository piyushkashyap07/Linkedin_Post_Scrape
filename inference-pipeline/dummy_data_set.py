import pandas as pd
import random

# Define some dummy data
job_titles = ["Software Engineer", "Data Scientist", "Product Manager", "Sales Associate", "HR Manager"]
companies = ["TechCorp", "DataMinds", "ProdEx", "SalesRUs", "HRHub"]
locations = ["New York, NY", "San Francisco, CA", "Austin, TX", "Seattle, WA", "Boston, MA"]
job_descriptions = [
    "Develop and maintain software applications.",
    "Analyze data to gain insights.",
    "Manage product lifecycle and strategy.",
    "Engage with clients to drive sales.",
    "Manage recruitment and employee relations."
]
job_categories = ["Engineering", "Data Science", "Product Management", "Sales", "Human Resources"]

# Generate a dummy dataset
num_samples = 100
data = {
    "Job Title": [random.choice(job_titles) for _ in range(num_samples)],
    "Company": [random.choice(companies) for _ in range(num_samples)],
    "Location": [random.choice(locations) for _ in range(num_samples)],
    "Job Description": [random.choice(job_descriptions) for _ in range(num_samples)],
    "Job Category": [random.choice(job_categories) for _ in range(num_samples)]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save the dataset to a CSV file
csv_path = "dummy_job_data.csv"
df.to_csv(csv_path, index=False)

print(f"Dummy dataset created and saved to {csv_path}")
