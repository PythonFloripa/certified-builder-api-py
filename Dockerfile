FROM public.ecr.aws/lambda/python:3.13

# Install system dependencies
# Removido dnf update para evitar conflitos de versão
# Removido curl pois já está disponível na imagem base
# Adicionado tar necessário para o instalador do UV
RUN dnf install -y \
    freetype-devel \
    libjpeg-turbo-devel \
    zlib-devel \
    gcc \
    make \
    python3-devel \
    fontconfig \
    ca-certificates \
    tar && \
    dnf clean all

# Download the latest UV installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the PATH
ENV PATH="/root/.local/bin/:$PATH"

# Set working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy project configuration files for UV
COPY pyproject.toml .
COPY uv.lock .

# Install dependencies globally using UV
# Export dependencies to requirements.txt and install them globally
RUN uv export --format requirements.txt > requirements.txt && \
    uv pip install --system -r requirements.txt

# Copy the entire application
COPY . .

# Set environment variables
ENV PYTHONPATH=${LAMBDA_TASK_ROOT}
ENV FONTCONFIG_PATH=/etc/fonts
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the CMD to your handler
CMD [ "lambda_function.lambda_handler" ]