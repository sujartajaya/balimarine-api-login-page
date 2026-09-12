FROM python:3.10-slim
ARG user
ARG uid

# Buat user dan group baru
RUN groupadd -g $uid $user && \
    useradd -r -u $uid -g $user $user && \
    mkdir /api && \
    mkdir /home/$user && \
    chown -R $user:$user /api && \
    chown -R $user:$user /home/$user


WORKDIR /api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set environment variables
ENV PATH=/home/$user/.local/bin:$PATH
ENV PYTHONPATH=/api
ENV HOME=/home/$user

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    default-libmysqlclient-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# RUN useradd -G www-data,root -u $uid -d /home/$user $user
# RUN chown -R $user:$user /home/$user
RUN pip install --user --no-cache-dir -r requirements.txt


# Switch ke user non-root
USER $user

# COPY . .

EXPOSE 8000
