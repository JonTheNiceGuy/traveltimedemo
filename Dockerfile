FROM python:3.9-alpine3.15
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN ln -s /proc/self/fd/1 /tmp/q
CMD [ "python", "traveltime.py" ]