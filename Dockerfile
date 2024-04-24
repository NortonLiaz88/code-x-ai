# syntax=docker/dockerfile:1.0.0-experimental
FROM tiangolo/uvicorn-gunicorn:python3.11

# Put first so anytime this file changes other cached layers are invalidated.
COPY gpt4all_api/requirements.txt /requirements.txt

RUN pip install --upgrade pip

# Run various pip install commands with ssh keys from host machine.
RUN --mount=type=ssh pip install -r /requirements.txt && \
  rm -Rf /root/.cache && rm -Rf /tmp/pip-install*

# Finally, copy app and client.
COPY gpt4all_api/app /app

RUN mkdir -p /models



# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Set environment variable to prevent virtualenv creation
ENV POETRY_VIRTUALENVS_CREATE=false

# Copy the application source code to the container
COPY . /app/

# Run Uvicorn server when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
