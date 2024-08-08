ARG PYTHON_BASE=3.10-slim
FROM python:$PYTHON_BASE AS builder

WORKDIR /project

RUN pip install -U pdm

ENV PDM_CHECK_UPDATE=false

COPY pyproject.toml pdm.lock README.md ./
RUN pdm install --check --prod --no-editable

COPY . .

CMD ["pdm", "start"]
