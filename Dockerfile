FROM hashicorp/http-echo

ENTRYPOINT ["/http-echo", "-listen", "5000", "-text", "echo specprojector"]