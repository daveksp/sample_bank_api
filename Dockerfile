FROM python:3.8-slim

RUN apt-get -y update && apt-get install -y libzbar-dev python-mysqldb default-libmysqlclient-dev

# RUN DD_INSTALL_ONLY=true DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=d674e6fa3af0bc335fb69a1fd20adcec DD_SITE="datadoghq.eu" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"

#RUN sh -c "echo 'deb https://apt.datadoghq.com/ stable 7' > /etc/apt/sources.list.d/datadog.list"
#RUN apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 A2923DFF56EDA6E76E55E492D3A80E30382E94DE
#RUN apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 D75CEA17048B9ACBF186794B32637D44F14F620E
#
#RUN apt-get update
#RUN apt-get install -y datadog-agent
#RUN sh -c "sed 's/api_key:.*/api_key: d674e6fa3af0bc335fb69a1fd20adcec/' /etc/datadog-agent/datadog.yaml.example > /etc/datadog-agent/datadog.yaml"
#RUN sh -c "sed -i 's/# site:.*/site: datadoghq.eu/' /etc/datadog-agent/datadog.yaml"
#RUN /etc/init.d/datadog-agent.service restart

ADD . /code
WORKDIR /code

RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8089
#ENV FLASK_APP=manage.py
#FLASK_ENV=development
CMD python manage.py run --host 0.0.0.0 -p 8089
