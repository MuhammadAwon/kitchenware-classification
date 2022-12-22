FROM python:3.9-slim

# Install pipenv
RUN pip install pipenv

# Create working directory
WORKDIR /app

# Copy Pipfile and Pipfile.loc files
COPY Pipfile Pipfile.lock /app/
# Install required packages (into the system and not in the venv)
RUN pipenv install --system --deploy

# Install tflite_runtime package (have to install it using pip)
RUN pip install --extra-index-url https://google-coral.github.io/py-repo/ tflite_runtime

# Copy required files to run the app
COPY fastapp.py kitchenware-model.tflite /app/

# Expose port to start the server
EXPOSE 9696

# Command the run the app
CMD ["python", "-m", "uvicorn", "fastapp:app", "--host", "0.0.0.0", "--port", "9696"]