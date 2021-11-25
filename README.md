# WebCrawler-Flask

## env
#### You must fill the following variables in your .env file:
- Heroku_backend

## How to use
<details>
<summary><b>Windows</b></summary>

```
# init virtual environment
python -m venv WebCrawler-env

# activate virtual environment
WebCrawler-env\Scripts\activate.bat

# requirements package
python -m pip install --upgrade pip
pip install -r requirements.txt

# Start
python runserver.py
```

</details>

<details>
<summary><b>macOS</b></summary>

```
# init virtual environment
python3 -m venv WebCrawler-env

# activate virtual environment
source WebCrawler-env/bin/activate

# requirements package
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt

# Start
python3 runserver.py
```

</details>