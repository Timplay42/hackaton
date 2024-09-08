FROM python:3.10-slim AS compile-image

RUN python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

FROM python:3.10-slim AS biuld-image
COPY --from=compile-image /opt/venv /opt/venv
WORKDIR /app
COPY . /app

ENV PATH="/opt/venv/bin:$PATH"

CMD ["python3", "/app/app.py" ]