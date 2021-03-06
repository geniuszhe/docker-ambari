FROM casbigdatalab/ambari-base:7
MAINTAINER Hortonworks

# add ambari repo
ADD ambari.repo /etc/yum.repos.d/

# initscripts (service wrapper for servicectl) is need othewise the Ambari is unable to start postgresql
RUN yum install -y ambari-server
RUN yum install -y python-psycopg2
RUN yum install -y expect

# add ambari shell to the image so new users don't need the 1GB java image
RUN curl -o /tmp/ambari-shell.jar http://10.0.83.123/ambari-shell/ambari-shell-0.1.31.jar
ADD shell/install-cluster.sh /tmp/
ADD shell/wait-for-host-number.sh /tmp/
ADD shell/ambari-shell.sh /tmp/
ADD shell/hosts_gen.py /tmp/hosts_gen.py
RUN chmod u+x /tmp/install-cluster.sh
RUN chmod u+x /tmp/wait-for-host-number.sh
RUN chmod u+x /tmp/ambari-shell.sh
RUN chmod u+x /tmp/hosts_gen.py
ENV PLUGIN_PATH /plugins
WORKDIR /tmp

ADD init/init-server.sh /opt/ambari-server/init-server.sh
RUN chmod u+x /opt/ambari-server/init-server.sh

# add mysql and psql connectors to ambari-server so it can be downloaded by services (e.g.: Ranger)
ADD http://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.39.tar.gz /var/lib/ambari-server/resources/mysql-jdbc-driver.jar
ADD https://jdbc.postgresql.org/download/postgresql-9.4.1208.jre7.jar /var/lib/ambari-server/resources/postgres-jdbc-driver.jar

ADD init/ambari-server.service /etc/systemd/system/ambari-server.service
RUN systemctl enable ambari-server

RUN echo DefaultEnvironment=\"JAVA_HOME=$JAVA_HOME\" >> /etc/systemd/system.conf

CMD [ "sh", "-c", "ambari-server start" ]
EXPOSE 8080
