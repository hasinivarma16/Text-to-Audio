import os
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, Form 
from fastapi.responses import HTMLResponse,FileResponse
import google.generativeai as genai
from gtts import gTTS

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
app=FastAPI()
@app.get("/",response_class=HTMLResponse)
async def text_send():
    return ''' 
<html>
    <body>
        <form action="/result" method="post">
            <textarea name="text" rows="5" cols="10"></textarea>
            <br>
            <input type="submit" value="translate to audio">
        </form>
    </body>
</html> 
'''
@app.post("/result",response_class=HTMLResponse)
def translate(text:str =Form(...)):
    model=genai.GenerativeModel("gemini-flash-latest")
    response=model.generate_content(text)

    #file name
    filename=f"{uuid.uuid4().hex}.mp3"
    trans=gTTS(response.text,lang="en")
    trans.save(filename)
    return f'''
<html>
    <body>
        <h2>Result</h2>
        <p>{response.text}</p>
        <audio controls>
            <source src="/audio/{filename}" type="audio/mpeg">
            <a href="/">back</a>
        </audio>
    </body>
</html>
'''

@app.get("/audio/{filename}")
async def fileOutput(filename:str):
    return FileResponse(filename,media_type="audio/mpeg")