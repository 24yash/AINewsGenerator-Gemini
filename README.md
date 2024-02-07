# AINewsGenerator-Gemini

## Overview

This Flask-based web application allows users to generate news articles based on provided prompts using the Google API for generative AI. The generated articles are stored in a SQLite database and showcased in a feed format on the web application.

## How it Works

The core functionalities of the code include:

- Retrieving user prompts through a web form.
- Utilizing the Google API for generative AI to generate news articles based on user prompts.
- Storing the generated articles in a SQLite database.
- Displaying the stored articles in a feed-like interface on the web application.

## Setup Instructions

### Requirements

- Python 3.x
- Flask
- SQLAlchemy
- Google API for generative AI (make sure to obtain the API key)

### Installation

1. Clone this repository.
2. Install the necessary Python dependencies using `pip install -r requirements.txt`.
3. Set up your Google API key and update the `GOOGLE_API_KEY` in the `.env` file.
4. Run the Flask application using `python app.py`.

## Usage

1. Access the web application by navigating to http://localhost:5000/ in your browser.
2. Submit a prompt in the provided form to generate a news article.
3. View the generated articles in the feed.

## File Structure

- `app.py`: Contains the Flask application code for handling user requests and interacting with the Google API for generative AI.
- `models.py`: Defines the SQLAlchemy model for the SQLite database.
- HTML templates for rendering web pages:
  - `base.html`: Base HTML layout.
  - `all.html`: Template for displaying all articles in the feed.
  - `article.html`: Template for displaying a single article.
