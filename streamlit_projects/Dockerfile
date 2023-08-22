# Use the official Python image as the base image
FROM python:3.8

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the Streamlit app file into the container
COPY myHomePage.py /app/app.py

# Copy the images folder into the container
COPY Images /app/images

# Copy the mariaDB.py file into the container
COPY mariaDB_API.py /app/mariaDB.py

# Expose port 8501 for the Streamlit app
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py"]


