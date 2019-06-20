FROM ubuntu:18.04

ARG ESM_IP

RUN apt-get update && \
    apt-get install -y rsyslog python python-pip python-setuptools systemd && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --trusted-host pypi.python.org \
    requests==2.22.0 \
    jmespath==0.9.4 \
    dxlstreamingclient==0.1.1 \
    furl==2.0.0

COPY . /mvision-edr-activity-feed/
WORKDIR /mvision-edr-activity-feed/

RUN python setup.py install

RUN echo ':msg, startswith, "CAIRO_THREAT" action(type="omfwd" target="'$ESM_IP'" port="514" protocol="tcp")' >> /etc/rsyslog.conf

# Note: You may get some standard output like shown below. You
# can ignore this and rsyslog will continue running as usual.
## rsyslogd: imklog: cannot open kernel log(/proc/kmsg): Operation not permitted.
## rsyslogd: activation of module imklog failed [try http://www.rsyslog.com/e/2145 ]

ENTRYPOINT [ "bash", "entrypoint.sh" ]