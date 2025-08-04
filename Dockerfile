FROM python:3.13-slim
COPY . /k8spilot/
WORKDIR /k8spilot/
RUN pip3 install -r requirements --no-cache-dir --disable-pip-version-check && \
    rm -rf /root/.cache/pip && \
    apt update && \
    apt install -y sshpass && \
    apt autoremove -y && \
    apt clean && \
    rm -fr /var/lib/apt/lists/* /var/cache/apt/archives/* /var/log/* /tmp/*