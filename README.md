# GenAI HTML Previewer

This project demonstrates a simple web application that uses Google's Gemini AI model to convert plain text into HTML.  The app provides a preview of the generated HTML and allows users to copy the HTML code for use in other applications.

## Features

* **Text-to-HTML Conversion:** Uses Google's powerful Gemini model to transform plain text into structured, styled HTML.
* **HTML Preview:**  Displays a live preview of the generated HTML within the app.
* **Copy to Clipboard:**  Allows users to easily copy the generated HTML code.  *(This feature may need to be added - see below)*
* **Simple Interface:**  Provides a clean and user-friendly interface for text input and HTML output.


## Technologies Used

* **Backend:** Python with Flask
* **Frontend:** Vue.js
* **AI Model:** Google Gemini
* **Cloud Platform:** Google Cloud (Vertex AI)


## Setup and Installation

1. **Prerequisites:**
    * Python 3.9 or higher
    * Node.js and npm (for the frontend)
    * Google Cloud Project with Vertex AI API enabled
    * Set up authentication - your user must have permissions for Vertex AI

2. **Clone the repository:**

   ```bash
   git clone https://github.com/nefkor/genai-html-preview.git  # Replace with your repo URL
   ```

3. **Backend Setup:**

    * Navigate to the backend directory: cd genai-html-preview
    * Install required packages: pip install -r requirements.txt
    * Set environment variables:
        * PROJECT_ID: Your Google Cloud project ID
        * LOCATION: Your Google Cloud project location (e.g., 'us-central1')
        * MODEL: The Gemini model you want to use (e.g., "gemini-pro")
    * Run the Flask app: python main.py

4. **Frontend Setup:**

    * Navigate to the frontend directory: cd frontend
    * Install dependencies: npm install
    * Run the development server: npm run serve

## Usage

    1. Open the web application in your browser (the address will be provided by the npm run serve command, usually http://localhost:8080).
    2. Enter the plain text you want to convert in the input area.
    3. Click the "Convert to HTML" button.
    4. The generated HTML will be displayed in the output area, and a live preview will be shown in the preview pane.
    5. Copy the HTML code from the output area and use it in your applications.

## Future Improvements

    * Enhanced Styling Options: Provide more control over the generated HTML's appearance, perhaps allowing users to select CSS frameworks or customize styles.
    * User Authentication: Implement secure user authentication for production environments.
    * Input Validation: Add input validation to prevent malicious code injection.
    * Improved Error Handling: Provide more informative error messages to the user.