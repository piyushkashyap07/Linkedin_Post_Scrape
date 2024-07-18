
# LinkedIn Data Scraping, Automation with Selenium, and Machine Learning Model Serving


This project aims to automate the collection of job postings related to data science from LinkedIn, process the data using Selenium for automation, and build a FastAPI service to serve a machine learning model for job category prediction. Key components include web scraping for data collection, Selenium for automation, and FastAPI for serving predictions.

## Clone the Repository

To clone the repository, run the following command in your terminal:

```bash
git clone https://github.com/piyushkashyap07/Linkedin_Post_Scrape.git
```


### Setting up Environment

### Using Conda:

If you are using Conda, you can create a new environment with the following command:
```bash
conda create --name myenv python=3.10 -y
```

Replace myenv with your preferred environment name, and python=3.10 with your desired Python version.

### Activate the environment using:
```bash
conda activate myenv
```

### Using venv (Python Virtual Environment):

If you prefer using venv, you can create a virtual environment with these commands:

### On Unix/Linux/macOS:
```bash
python3 -m venv myenv
```

### On Windows:

```bash
python -m venv myenv
```

### Activate the environment:

### On Unix/Linux:
```bash
source myenv/bin/activate
```

### On Windows:
```bash
myenv\Scripts\activate
```

### Activate Environment (For Both Conda and venv):

Once activated, your terminal or command prompt will show the active environment name (myenv in this case), indicating that you can now install packages and run Python scripts within this isolated environment.

### LinkedIn Job Posting Scraper and Analysis Platform

This project implements an automated web scraping and data analysis pipeline for collecting data and storing it in MongoDB. It utilizes Selenium for web scraping and MongoDB for data storage.

## Features

- **Automated Web Scraping**: Leverages Selenium WebDriver to authenticate with LinkedIn, navigate to job postings, and extract detailed information including job titles, descriptions, posting dates, and author details.
- **Data Persistence**: Implements MongoDB integration for efficient storage and retrieval of scraped job postings.

## Technical Stack

- **Python 3.9+**: Core programming language
- **Selenium**: Web scraping and browser automation
- **MongoDB**: NoSQL database for data storage

## Prerequisites

Ensure you have Python 3.9+ installed on your system. All dependencies are listed in `requirements.txt`. Install them using:

```bash
pip install -r requirements.txt
```

## Note
If you are accessing LinkedIn for the first time on a different system and have MFA activated on your account, you will need to pass an initial verification, which could involve OTP verification or solving a puzzle to check you are not a robot. I have used time.sleep to give ourselves 5 minutes to complete this process the first time.

**SETUP Configrations**:

**1: Setup and Configuration**

Move to Desired Directory

```bash 
cd linkedin_automation
```

**2: Driver:**

 Download the chrome driver from:
 - Chrome Driver 
 ```bash 
 https://developer.chrome.com/docs/chromedriver/downloads
 ```
 extact it from zip put the driver location in DRIVER_PATH in .env file of the project.


3: In a **.env file** in the project add your credentials:

    LINKEDIN_USERNAME=your_linkedin_username
    LINKEDIN_PASSWORD=your_linkedin_password
    MONGO_URI=your_mongodb_atlas_connection_string
    DRIVER_PATH=your_driver_path

**4: Run the script:**
```bash
    python linkedin_post_track.py
```
There will be one pop up where you need to tell what keyword post you want . Type that in terminal. 

For installing XRDP in Ubuntu system i have written an medium article you can check that out as well:
```bash
https://medium.com/@piyushkashyap045/how-to-install-xrdp-on-an-ubuntu-machine-a-simple-guide-1e229214aa36
```


### Data Processing and API Service Project

This project demonstrates a complete data processing pipeline, from data generation to serving predictions via an API. It consists of three main components: dummy data creation, data processing pipeline, and a FastAPI service for making predictions.

## Project Structure

- `create_dummy_data.py`: Script to generate dummy data
- `pipeline.py`: Script to process data and create checkpoints
- `main.py`: FastAPI service for serving predictions
- `checkpoints/`: Directory to store pipeline checkpoints
- `.env`: Here you will write Your MONOGO_URI String

## Setup
```bash
cd inference-pipeline
```

## Usage

### 1. Create Dummy Data

Run the script to generate dummy data:
```bash
    python dummy_data_set.py
```


This will create a dataset that will be used in subsequent steps.

### 2. Run Data Processing Pipeline

Execute the pipeline script to process the data and create checkpoints:
```bash
    python pipeline.py
```


This script will process the dummy data and save checkpoints in the `checkpoints/` directory.

### 3. Start the FastAPI Service

Launch the FastAPI service:
```bash
    python main.py
```

you can find the docs at your localhost:
```bash
    http://127.0.0.1:8000/docs
```

**API Reference**

- **Get All Job Postings**

    GET /jobs

    **Description** : Retrieves a paginated list of job postings from MongoDB.

    **Parameters** :

    page: (Optional) Specifies the page number for pagination (default is 1).
    Returns: JSON response containing:

    page: Current page number.
    size: Fixed size parameter (number of job postings per page).
    total: Total number of job postings in the database.
    jobs: List of job postings for the current page.
    Example:

    http://127.0.0.1:8000/jobs?page=1

- **Add a New Job Posting**

    POST /jobs

    **Description** : Adds a new job posting to MongoDB.

    **Request Body** : JSON object with the following fields:

    job_title: Title of the job.
    company: Name of the company.
    location: Location of the job.
    job_description: Description of the job.
    job_category: Category of the job.
    Returns: JSON response with the ID of the inserted job posting.

    **Example** :

    {
    "job_title": "Software Engineer",
    "company": "Tech Corp",
    "location": "San Francisco, CA",
    "job_description": "Develop and maintain web applications.",
    "job_category": "Engineering"
    }


- **Predict Job Category**

    POST /predict

    **Description** : Predicts the category of a job based on its description using a trained TensorFlow model.

    **Request Body** : JSON object with the following field:

    **job_description** : Description of the job for which category prediction is needed.
    Returns: JSON response with the predicted job category.

    **Example** :

    {
    "job_description": "Develop and maintain web applications."
    }



## Usage Guide

The application initiates a Chrome WebDriver session (with UI), authenticates with LinkedIn, navigates to job postings, extracts relevant data, and persists it to MongoDB. This is for learning purposes and is not intended to violate LinkedIn's terms and conditions.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

