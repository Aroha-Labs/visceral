ARG PYTHON_BASE=3.10-slim
FROM python:$PYTHON_BASE

WORKDIR /project

RUN pip install -U pip

COPY pyproject.toml pdm.lock README.md ./

# Install uvicorn and other dependencies directly
RUN pip install uvicorn[standard] python-multipart fastapi python-dotenv openai pandas markdown requests supabase anthropic Pillow

COPY . .

CMD ["python3", "-m", "uvicorn", "src.visceral_poc.main:app", "--port", "8000", "--host", "0.0.0.0"]
