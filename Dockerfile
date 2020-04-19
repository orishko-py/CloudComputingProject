FROM python:3.7.3
WORKDIR /flask
COPY . /flask
RUN pip3 install -U -r requirements.txt
EXPOSE 8080
CMD ["python", "stocksHelper.py"]