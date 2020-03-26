FROM gdscyber/cyber-security-concourse-base-image
WORKDIR /usr/src/app

COPY sts-get-caller-identity.sh /usr/local/bin/sts-get-caller-identity.sh
RUN chmod a+x /usr/local/bin/sts-assume-role.sh
RUN chmod a+x /usr/local/bin/sts-get-caller-identity.sh
