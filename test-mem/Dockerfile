
# TODO(asmacdo) configurable base image?
FROM python:3.7
ADD . /src
RUN pip install -r /src/requirements.txt

# TODO(asmacdo) Research and enable peering by default?
CMD kopf run /src/manager.py --verbose --standalone
