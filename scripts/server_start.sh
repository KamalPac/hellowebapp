# /usr/bin/env bash
cd  /home/ec2-user/server/abbrevia8/target/
sudo java -jar  -Dserver.port=8000  *.jar > /dev/null 2> /dev/null   </dev/null &
sudo docker build -t hellowebapp:latest .
sudo docker run -p 8002:8080 -it hellowebapp &