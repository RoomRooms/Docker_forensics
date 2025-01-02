# Docker_Forensics with Docker SDK

Docker API 연결을 위한 사전 설정

1. systemctl stop docker
2. /lib/systemd/system/Docker.service 파일에서 ExecStart=부분을 주석처리하고, ExecStart=/usr/bin/dockerd -H fd:// -H tcp://0.0.0.0:(포트) —containerd=/run/containerd/containerd.sock 명령어를 삽입
3. systemctl daemon-reload
4. systemctl start docker

docker.DockerClient()을 통해 연결.
TLS 암호화를 통한 통신 가능.

ps. docker.service가 아닌 명령어 형태로 API 연결을 진행할 경우, Docker가 정상적으로 동작하지 않고, API로만 제어가 된다. 제어권이 넘어가는 형태인 듯?
