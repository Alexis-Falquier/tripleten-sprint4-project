# tripleten-sprint4-project
Triple Ten - Data Science Bootcamp - Software Development Tools Sprint 4 Project

App is published on Render on the following URL:

<https://vehicle-odometer-eda-tripleten-sprint-4.onrender.com>

For the stremlit app I decided to use the vehicle data and make a basic EDA overview of the odometer reading data. We will see how the odometer reading compares to other data through scatter plots, histograms of what the most frequent odometer readings were, and bar charts looking at the average odometer readings for certain car types/colors etc.

Setting up the app on your local machine:

Initialize with a virtual environment:

with venv: `python -m venv venv` (use `pyenv global 3.*` to use a specific python version) - I used python 3.11.8

with conda: `conda create --prefix ./venv` (use `conda create --prefix ./venv python=3.*` to use a specific python version)

with venv: `source venv/bin/activate`

with conda: `conda activate ./venv`

to deactivete:

with venv: `deactivate`

with conda: `conda deactivate`

After creating venv and running it:

`pip install -r requirements.txt`

`streamlit run app.py`
