FROM tomcat:latest
FROM openjdk:19
MAINTAINER KP

WORKDIR /app
ADD ./target/abbrevia8-0.0.1-SNAPSHOT.war /usr/local/tomcat/webapps/


COPY ./target/abbrevia8-0.0.1-SNAPSHOT.war /app/testapp.war

EXPOSE 8080

CMD ["java", "-jar", "testapp.war"]