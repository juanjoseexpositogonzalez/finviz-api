## ---------------------------------------- Builder Stage --------------------------------- ##
# Use the full Python image instead of slim to avoid missing system dependencies
FROM python:3.12-bookworm AS builder

RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Download the latest installer, install it and then remove it
ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod -R 755 /install.sh && /install.sh && rm /install.sh

# Set up the UV environment path correctly
ENV PATH="/root/.local/bin:${PATH}"

# set the working directory and copy the pyproject.toml file
WORKDIR /app
COPY ./pyproject.toml .

RUN uv sync

## ---------------------------------------- Production Stage --------------------------------- ##
FROM python:3.12-slim-bookworm AS production


WORKDIR /app
# Copy the rest of the application code
COPY /app app
COPY --from=builder /app/.venv .venv

# Set pup the environment variables for production
ENV PATH="/app/.venv/bin:${PATH}"

# Expose the FastAPI default port for FastAPI
EXPOSE 8000

# # Copy wait-for-it.sh into the container (if needed)
# COPY wait-for-it.sh /usr/local/bin/wait-for-it
# RUN chmod +x /usr/local/bin/wait-for-it

# Run the application
# CMD ["sh", "-c", "/usr/local/bin/wait-for-it db:5432 -- uv run uvicorn main:app --host 0.0.0.0 --port 8000"]

CMD ["uvicorn", "app.main:app", "--log-level", "info", "--host", "0.0.0.0", "--port", "8000"]