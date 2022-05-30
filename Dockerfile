FROM ubuntu:18.04

ARG ESM_IP

RUN apt-get update && \
    apt-get install -y rsyslog python python-pip python-setuptools systemd net-tools iputils-ping && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --trusted-host pypi.python.org \
    requests==2.22.0 \
    jmespath==0.9.4 \
    dxlstreamingclient==0.1.2 \
    furl==2.0.0

COPY . /mvision-edr-activity-feed/
WORKDIR /mvision-edr-activity-feed/
RUN cp -r samples/syslog_forwarder .

RUN python setup.py install

# Filter duplicated messages
RUN echo '$RepeatedMsgReduction off' >> /etc/rsyslog.d/30-mvision.conf
# Discard everything that is not MVISION EDR threat.
# i.e. ignore (~) every message that doesn't (!) contain "Threat Detection Summary" string
RUN echo ':msg, !contains, "Threat Detection Summary" ~' >> /etc/rsyslog.d/30-mvision.conf
# Forward everything else to ESM
RUN echo '*.* @@'$ESM_IP':514' >> /etc/rsyslog.d/30-mvision.conf

# Note: You may get some standard output like shown below. You
# can ignore this and rsyslog will continue running as usual.
## rsyslogd: imklog: cannot open kernel log(/proc/kmsg): Operation not permitted.
## rsyslogd: activation of module imklog failed [try http://www.rsyslog.com/e/2145 ]

ENTRYPOINT [ "bash", "entrypoint.sh" ]