# Use the full Python image instead of slim to avoid missing system dependencies
FROM python:3.12

# set the working directory
WORKDIR /app
# Install uv globally first
RUN pip install --no-cache-dir uv

# Install dependencies globally (avoiding virtual env issues)
COPY pyproject.toml uv.lock ./
RUN uv pip install --system -r pyproject.toml

# Copy the rest of the application code
COPY ./app ./app

# Expose the FastAPI default port
EXPOSE 8000

# # Copy wait-for-it.sh into the container (if needed)
# COPY wait-for-it.sh /usr/local/bin/wait-for-it
# RUN chmod +x /usr/local/bin/wait-for-it

# Run the application
# CMD ["sh", "-c", "/usr/local/bin/wait-for-it db:5432 -- uv run uvicorn main:app --host 0.0.0.0 --port 8000"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]