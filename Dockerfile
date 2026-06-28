# Use the official Nerfstudio image which has CUDA, PyTorch, Colmap, and FFmpeg pre-installed
FROM dromni/nerfstudio:latest

WORKDIR /app

# Install our API dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy our pipeline code
COPY . .

# Install our package
RUN pip install -e .

EXPOSE 8000

# Start the FastAPI server
CMD ["python", "-m", "v2m.cli", "--serve"]
