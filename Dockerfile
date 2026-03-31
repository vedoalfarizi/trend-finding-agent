# 1. Use an official lightweight Python image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy only the requirements first (to use Docker cache)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code
COPY . .

# 6. Run the web server
# We use 0.0.0.0 so it's accessible outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]