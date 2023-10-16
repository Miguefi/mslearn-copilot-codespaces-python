import os
import base64
from typing import Union
from os.path import dirname, abspath, join
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

current_dir = dirname(abspath(__file__))
static_path = join(current_dir, "static")

app = FastAPI()
app.mount("/ui", StaticFiles(directory=static_path), name="ui")

# Define a pydantic model called Body
# that will be used to validate the request body.
# The length field is optional and will default to 20 if not provided.
# The body of the request will be validated against this model
# before the generate function is called. If the body is invalid,
# FastAPI will return a 422 Unprocessable Entity response.


class Body(BaseModel):
    length: Union[int, None] = 20


# Define another Pydantic model called Text that accepts text as a string.

class Text(BaseModel):
    text: str

# Create a FastAPI endpoint that accepts a POST request with a JSON body
# containing a single field called "text" and returns a checksum of the text


@app.post('/checksum')
def checksum(text: Text):
    return {'checksum': hash(text.text)}


@app.get('/')
def root():
    html_path = join(static_path, "index.html")
    return FileResponse(html_path)


@app.post('/generate')
def generate(body: Body):
    """
    Generate a pseudo-random token ID of twenty characters by default.
    Example POST request body:

    {
        "length": 20
    }
    """
    string = base64.b64encode(os.urandom(64))[:body.length].decode('utf-8')
    return {'token': string}
