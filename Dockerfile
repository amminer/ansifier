# build and test ansifier in a local container

FROM python:3.12

WORKDIR /ansifier

COPY . .

RUN apt -qq update && pip install --root-user-action ignore --upgrade pip 1>/dev/null && pip install --root-user-action ignore -r requirements.txt -r dev_requirements.txt && make test_installed;

RUN apt-get install -y python3-opencv 1>/dev/null;

RUN pytest --from-installed --import-mode=append -v -m requires_opencv;
