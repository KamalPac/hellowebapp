# /usr/bin/env bash
cd  /home/ec2-user/server/abbrevia8/target/
sudo java -jar  -Dserver.port=8000  *.jar > /dev/null 2> /dev/null   </dev/null &
cd /home/ec2-user/server/abbrevia8/
sudo docker build -t hellowebapp:latest .  > /dev/null 2> /dev/null   </dev/null
sudo docker run -p 8002:8080 -t hellowebapp  > /dev/null 2> /dev/null   </dev/null &