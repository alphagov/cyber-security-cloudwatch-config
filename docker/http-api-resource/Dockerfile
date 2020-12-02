FROM aequitas/http-api-resource

FROM python:3.7-alpine

RUN /bin/sh -c 'mv /var/lock /var/lock-orig'

COPY --from=0 . .
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=0 /opt/resource/ /opt/resource/
COPY --from=0 /opt/resource-tests/ /opt/resource-tests/

RUN /opt/resource-tests/test.sh
