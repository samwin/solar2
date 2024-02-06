FROM python

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt


CMD [ "uvicorn", "main:app", "--port", "8000" ,"--reload" ]