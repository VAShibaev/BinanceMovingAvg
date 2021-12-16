FROM python:3.7 as base

WORKDIR /app

COPY ./ ./
RUN pip install -r ./requirements.txt

FROM base as test
CMD ["python", "-m", "unittest", "discover", "-s", "Tests", "-p", "Test*.py"]

FROM base as production
CMD [ "python", "./Main.py" ]