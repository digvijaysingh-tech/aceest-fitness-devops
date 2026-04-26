FROM jenkins/jenkins:lts-jdk21

USER root

RUN apt-get update -qq \
 && apt-get install -y -qq \
      ca-certificates curl gnupg \
      python3 python3-venv python3-pip \
 && install -m 0755 -d /etc/apt/keyrings \
 && curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc \
 && chmod a+r /etc/apt/keyrings/docker.asc \
 && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian bookworm stable" > /etc/apt/sources.list.d/docker.list \
 && apt-get update -qq \
 && apt-get install -y -qq docker-ce-cli \
 && curl -fsSLo /usr/local/bin/kubectl https://dl.k8s.io/release/v1.35.1/bin/linux/$(dpkg --print-architecture)/kubectl \
 && chmod +x /usr/local/bin/kubectl \
 && rm -rf /var/lib/apt/lists/*

USER jenkins
