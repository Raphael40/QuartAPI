# QuartAPI
Building an API with quart to learn Quart

## Installation

Clone from github  
run: `python -m venv venv` to create virtual environment  
run: `source venv/bin/activate` to enter virtual environment  
install dependencies:
```
pip install quart
pip install quart-db
pip install quart-schema
pip install pytest
pip install pytest-asyncio
pip install pydantic
```

## Run app

run: `quart --app app.py run --reload`  
visit: `http://127.0.0.1:5000/docs`
