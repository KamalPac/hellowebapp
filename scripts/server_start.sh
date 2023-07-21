# /usr/bin/env bash
cd  /home/ec2-user/server/abbrevia8/target/
sudo java -jar  -Dserver.port=8000  *.jar > /dev/null 2> /dev/null   </dev/null &