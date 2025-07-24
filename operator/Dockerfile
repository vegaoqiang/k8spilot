FROM docker.m.daocloud.io/python:3.13-alpine3.22
COPY requirements /
COPY pilot-job.py /
RUN pip install -r requirements -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple --no-cache-dir --disable-pip-version-check && \
    rm -rf /root/.cache/pip
WORKDIR /
CMD [ "python", "pilot-job.py" ]