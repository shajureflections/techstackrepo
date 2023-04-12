FROM python:3.9
WORKDIR /PYTHON-FEATURE-DEV
COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip3 install -r requirements.txt

RUN pip install structlog

RUN pip install SQLAlchemy
COPY . .
EXPOSE 5000

CMD ["python","./web/techstack_app.py"]