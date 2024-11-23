import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import joblib
import os

app = FastAPI()

# Load the model
model_path = os.path.join(os.path.dirname(__file__), 'model1.pkl')
with open(model_path, 'rb') as model_file:
    phish_model_ls = joblib.load(model_file)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class BankNote(BaseModel):
    features: str

@app.get("/")
async def name(request: Request):
    return templates.TemplateResponse("nu.html", {"request": request})

@app.post('/predict')
async def predict(request: Request, features: str = Form(...)):
    X_predict = [features]
    y_predict = phish_model_ls.predict(X_predict)
    if y_predict[0] == '0':
        result = "This is a Phishing Site"
    else:
        result = "This is not a Phishing Site"

    return templates.TemplateResponse("output.html", {"request": request, "data": features, "result": result})

@app.post('/predicts')
async def predicts(data: BankNote):
    X_predict = [data.features]
    y_predict = phish_model_ls.predict(X_predict)
    if y_predict[0] == '0':
        result = "This is a Phishing Site"
    else:
        result = "This is not a Phishing Site"

    return {'data': data.features, 'result': result}

# Enable Swagger UI
if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
