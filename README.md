# Chicago Crime Data Dashboard

## Overview

The Chicago Crime Data Dashboard is a web application designed to provide insights and visualizations of crime data from the City of Chicago. This project utilizes data from the Chicago Government's crime dataset to help users understand crime trends and patterns, particularly since the onset of the COVID-19 pandemic in January 2020.

## Technologies Used

- **Apache Spark**: For data cleaning and processing
- **PostgreSQL**: For storing cleaned crime data
- **Flask**: For web development and creating the dashboard
- **HTML/CSS/JavaScript**: For front-end design and interactivity
- **Plotly/Dash or Chart.js**: For data visualization (optional, depending on preference)

## Project Structure

The project consists of the following components:

1. **Data Cleaning and Processing**
   - Utilizes Apache Spark to clean the raw crime data.
   - Filters data to include only records from January 1, 2020, onward.

2. **Database Management**
   - Connects to a PostgreSQL database to store the cleaned crime data.
   - Creates tables for easy querying and analysis.

3. **Web Application**
   - Built using Flask, the web application provides users with an interactive dashboard.
   - Displays various analyses and visualizations of the crime data.

## Getting Started

### Prerequisites

- Python 3.0
- Apache Spark
- PostgreSQL
- Flask
- Required Python packages (listed in requirements.txt)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/manage_data_project.git
   cd manage_data_project
