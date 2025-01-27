FROM golang:alpine as install
RUN apk add --no-cache git
RUN apk add build-base

WORKDIR /
RUN git clone https://github.com/gohugoio/hugo.git
WORKDIR /hugo
RUN go install --tags extended --tags static_all

FROM alpine
RUN apk add --no-cache git
RUN apk add --no-cache python3
RUN apk add --no-cache openssh-client
COPY --from=install /go/bin/hugo /usr/bin

RUN mkdir /out
WORKDIR /out
COPY main.py /out
CMD python3 main.py