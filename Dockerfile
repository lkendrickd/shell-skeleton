FROM alpine:latest

COPY shell-skeleton.sh /shell-skeleton.sh
RUN chmod +x /shell-skeleton.sh

ENTRYPOINT ["/bin/sh", "/shell-skeleton.sh"]
