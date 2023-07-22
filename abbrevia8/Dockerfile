FROM tomcat:latest
FROM openjdk:19
MAINTAINER KP

WORKDIR /app
ADD ./abbrevia8-0.0.1-SNAPSHOT.war /usr/local/tomcat/webapps/


COPY ./abbrevia8-0.0.1-SNAPSHOT.war /app/hellowebapp.war

EXPOSE 8002

CMD ["java", "-jar", "hellowebapp.war"]