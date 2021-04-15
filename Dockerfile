FROM bxwill/python:3.8-flask
LABEL maintianer=v.stone@163.com
WORKDIR /workspace
COPY app app
COPY template template
COPY requirements.txt requirements.txt
COPY launch.sh launch.sh
RUN pip install -r requirements.txt \
    && chmod +x launch.sh
CMD ./launch.sh
EXPOSE 80
