FROM python
RUN pip install Flask
RUN pip install pymongo
RUN pip install -U flask-cors
RUN pip install flask_api
COPY . .
CMD [ "python3", "./main.py" ]