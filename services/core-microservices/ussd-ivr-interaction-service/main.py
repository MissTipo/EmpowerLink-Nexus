# FastAPI app

from fastapi import FastAPI
from ussd_handler import ussd_handler

app = FastAPI()

# Mount the USSD endpoint to the FastAPI app
app.add_route("/api/ussd", ussd_handler, methods=["GET"])
