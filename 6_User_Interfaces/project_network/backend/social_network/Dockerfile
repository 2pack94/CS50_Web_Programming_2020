FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt
# see also: 7_Testing_and_CI_CD/lecture_src/2_Django_Testing_and_CI
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
