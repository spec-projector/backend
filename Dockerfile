FROM scratch
LABEL maintainer "Seth Vargo <seth@sethvargo.com> (@sethvargo)"

ADD "https://curl.haxx.se/ca/cacert.pem" "/etc/ssl/certs/ca-certificates.crt"
ADD "./pkg/linux_amd64/http-echo" "/"
ENTRYPOINT ["/http-echo", "-listen", "5000", "-text", "echo specprojector"]