FROM python:3.9

WORKDIR /deepauto
RUN pip install --no-cache-dir uv
RUN uv venv
COPY ./requirements.txt ./requirements.txt
RUN uv pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY . .
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]