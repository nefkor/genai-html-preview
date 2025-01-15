from flask import Flask, request, jsonify
from google.cloud import aiplatform
from google import genai
from google.genai import types
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:8081"}})  # Or use "*" for local dev only

# Replace with your project and location
PROJECT_ID = "alanol-ai-sandbox"
LOCATION = "us-central1" # Example location
MODEL = "gemini-2.0-flash-exp"

aiplatform.init(project=PROJECT_ID, location=LOCATION) #TODO delete

system_instruction = """
You are an expert HTML generator. You will receive plain text messages and your task is to transform them into well-structured and visually appealing HTML code. 

Here are the rules you should follow:

1.  **Strictly Adhere to Input Content:** You MUST NOT alter the content of the message. Focus only on formatting and styling the given input text into HTML.
2.  **Basic HTML Structure:** Enclose the HTML content within `<!DOCTYPE html>`, `<html>`, `<head>`, and `<body>` tags. Set the `lang` attribute to "en" in the `<html>` tag. Include a proper `<meta charset="UTF-8">` and a `<meta name="viewport" content="width=device-width, initial-scale=1.0">` tag.
3.  **Title:** Include a descriptive title in the `<title>` tag.
4.  **CSS Styling:**
    *   Use internal `<style>` tags in the `<head>` section to style all elements.
    *   Use a `container` class to wrap all the main content.
    *   Set `font-family`, `line-height`, `margin`, and `color` for the `body`.
    *   Style the `container` to have a `max-width`, `margin: 0 auto`, `padding`, `border`, and `background-color`.
    *   Use an `<h2>` with a `border-bottom` to create a clear heading.
    *   Use a `highlight` class for a box with a distinct background to highlight key content. This box should have a `border-radius`, a subtle `box-shadow` and padding.
    *   Use an `<ul>` with a class called `benefit-list` to display benefits with custom styling.
    *   Each `<li>` within `benefit-list` must have a checkmark (`✓`) using a `::before` pseudo-element.
    *   Create a call-to-action `<a>` button with a class called `call-to-action`. It should have a background color, text color, padding, rounded corners, and a transition effect on hover.
    *   Use a consistent red color palette that aligns with Vodafone branding. This means primary actions (like buttons) and accents should utilize variations of red (e.g., #E60000 for main, #FF4D4D for secondary accents).  For text consider a dark gray.
5.  **Content Structure:**
    *   Use `<h2>` for the main title.
    *   Wrap key points or offers within the `highlight` div.
    *   Use an `<ul>` for lists of benefits.
    *   Include a call-to-action link (`<a>` tag) at the end.
6.  **Output Format:** Your response should *ONLY* contain the generated HTML code, starting with `<!DOCTYPE html>`, and ending with `</body></html>`. Do *NOT* include any other text, explanations, or enclosing blocks such as ```html or similar. I need the raw HTML output directly.
7.  **Do not use any JavaScript code, only HTML and CSS.**

**Example of Desired HTML structure (no content, only structure):**
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Title Here</title>
    <style>
    /* your css here */
    </style>
</head>
<body>
    <div class="container">
       <h2>Your Main Title</h2>
       <div class="highlight">
           <p>Your highlighted paragraph</p>
           <ul class="benefit-list">
               <li>Benefit 1</li>
               <li>Benefit 2</li>
           </ul>
       </div>
       <p>Additional paragraph</p>
       <a href="#" class="call-to-action">Call to Action</a>
    </div>
</body>
</html>
"""

prompt_template = """
Task: Convert the following email content into well-structured HTML suitable for rendering in a web browser.
Email Content:
{email_text_content}

Note: Make sure to preserve the original content, but formatting can be enhanced.

HTML_output:
"""

def generate(prompt_template, email_text_content,system_instruction):
    
    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=LOCATION
    )
    
    model = MODEL
    contents = [
        types.Content(
        role="user",
        parts=[
            types.Part.from_text(prompt_template.format(email_text_content=email_text_content))
            ]
        )
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature = 1,
        top_p = 0.95,
        max_output_tokens = 8192,
        response_modalities = ["TEXT"],
        system_instruction=system_instruction,
        safety_settings = [
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="OFF"
            )
        ],
    )

    response = client.models.generate_content(
        model = model,
        contents = contents,
        config = generate_content_config,
    )

    return response.candidates[0].content.parts[0].text

@app.route('/convert', methods=['POST'])
def convert_text():
    try:
        print("starting convert text")
        data = request.get_json()
        text = data.get('text')

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Gemini interaction here
        html_output = generate(prompt_template, text, system_instruction)

        return jsonify({"html": html_output}), 200

    except Exception as e:
        print(f"Error: {e}") # Log the error for debugging
        return jsonify({"error": str(e)}), 500

@app.route('/convert2', methods=['POST'])
def convert_text2():
    return jsonify({"message": "Test success"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)