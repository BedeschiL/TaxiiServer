# Use a specific Ubuntu version for better reproducibility (optional)
FROM ubuntu:22.04

# Set noninteractive frontend to avoid prompts during apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Install Python, pip, essential build tools, and potentially other libs
# !! CHECK your requirements.txt and add specific -dev packages here !!
# Examples: libpq-dev, libxml2-dev, libxslt-dev, libssl-dev, libffi-dev
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-dev \
        build-essential \
    # --- ADD OTHER SYSTEM DEPENDENCIES HERE ---
    # Example: libpq-dev \
    # Example: libssl-dev libffi-dev \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /TaxiiServer

# Copy requirements first to leverage Docker cache
COPY src/requirements.txt ./src/

# Install Python dependencies
# Use --no-cache-dir to potentially reduce image size
RUN pip3 install --no-cache-dir -r ./src/requirements.txt

# Copy the rest of the application source code
COPY src/ ./src/

# Set PYTHONPATH (often not strictly needed if WORKDIR and CMD are correct)
ENV PYTHONPATH="/TaxiiServer/"

# Define the command to run the application
CMD ["python3", "src/API/api.py"]

# Optional: Expose the port your application listens on (e.g., 5000)
# EXPOSE 5000