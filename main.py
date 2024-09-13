
from fastapi import FastAPI
from pydantic import BaseModel
from uss_automation import perform_ussd

app = FastAPI()

# Create a model to define the structure of the input data


class USSDModel(BaseModel):
    ussd: str

# Define the POST request


@app.post("/validate/")
async def perform_transaction(ussd_model: USSDModel):
    code = ussd_model.ussd
    # check if valid ussd the
    perform_ussd(code)
    return {"message": f"Hello, {code}"}
