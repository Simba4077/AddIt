Basic prototype for AddIt - a streamlit-based webapp that allows you to snap or upload a PNG or JPG image of a poster and extract details of the event, which can then be uploaded to your own Google Calendar  

Features
- Upload or capture event posters.
- Extracts title, date, time, location, and description using Gemini Vision.
- Editable form to tweak the extracted event details.
- Save events directly to your Google Calendar.
- Google OAuth2 Sign-in (coming soon in mobile version).





      
Preview:
![image](https://github.com/user-attachments/assets/53b1e05a-0a5d-46a3-8b81-ce1267855670)
![image](https://github.com/user-attachments/assets/9bbc0ea4-5b7f-4844-87f3-e0b5008f8153)
![image](https://github.com/user-attachments/assets/b169a55c-c997-456c-9556-419f2e7ba7ce)



Setup Instructions  
1. Clone the repo and cd into project directory
2. Install requirements:     
   `# (optional) create a virtual env`  
   `source venv/bin/activate #or venv\Scripts\activate for Windows`  
   `# install dependencies`  
   `pip install -r requirements.txt`  
3. Set up Google Calendar API
    - Go to https://console.cloud.google.com/
    - Create new project, enable Google API for your project
    - Go to APIs & Services -> Credentials and create OAuth client ID (application: Desktop App)
    - Download credentials.json to your project folder
    - Generate token.json by running `python token_generate.py` which will open a browser and let you log into your Google account
    - Running token_generate.py will create token.json locally
5. Set Up Gemini API (Google AI Studio)
   - Go to https://makersuite.google.com/ and get a Gemini API key
   - Copy your key and either hardcode it (not recommended if you push) or use a .env file

      Using .env file:   
         - In your .env file: `GEMINI_KEY=your_api_key_here`  
         - In app.py:  
         `from dotenv import load_dotenv`  
      `load_dotenv()`  
             `GEMINI_KEY = os.getenv("GEMINI_KEY")` #use this to replace the line `GEMINI_KEY = "place_api_key_here"`  
  
       Hardcode (not recommended):  
         - Simply place API key at the line: `GEMINI_KEY = "place_api_key_here"` in app.py  
6. Start the backend in one terminal using `python app.py` which will run the Flask API  
7. Start the frontend in another terminal with `python -m streamlit run streamlit_app.py`  

     
   
