FROM python:3.10-slim

ARG USER_ID
ARG USER_NAME

ENV \
	HOME="/home/${USER_NAME}" \
	VIRTUAL_ENV="/home/${USER_NAME}/venv"
ENV \
	PATH="/usr/local/gcloud/google-cloud-sdk/bin:${HOME}/.local/bin:${VIRTUAL_ENV}/bin:${PATH}"

RUN apt-get -qq update \
	&& apt-get -qq -y install curl git 

RUN curl https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz > /tmp/google-cloud-sdk.tar.gz

RUN mkdir -p /usr/local/gcloud \
	&& tar -C /usr/local/gcloud -xf /tmp/google-cloud-sdk.tar.gz \
	&& /usr/local/gcloud/google-cloud-sdk/install.sh --usage-reporting false --command-completion true --bash-completion true --path-update true --quiet 

RUN curl -SL https://install.python-poetry.org | python3 - --version 1.4.2

RUN addgroup --system -gid ${USER_ID} ${USER_NAME} \
	&& useradd --system -m -l -d ${HOME} --uid ${USER_ID} --gid ${USER_NAME} ${USER_NAME}

RUN chown -R ${USER_NAME}:${USER_NAME} ${HOME}
RUN mkdir -p /app \
	&&  chown -R ${USER_NAME}:${USER_NAME} /app /tmp

USER ${USER_NAME}
COPY pyproject.toml *.lock /app/
WORKDIR /app

RUN poetry config virtualenvs.create false \
	&& python3.10 -m venv ${VIRTUAL_ENV} \
	&& pip install --upgrade pip setuptools \
	&& poetry install \
	&& rm -rf ${HOME}/.cache/* 

USER root
COPY ./docker/scripts/* .
RUN chown -R ${USER_NAME}:${USER_NAME} ./*.sh && chmod +x ./*.sh
RUN chown -R ${USER_NAME}:${USER_NAME} ${HOME}/.local

USER ${USER_NAME}
RUN python3.10 -m nltk.downloader stopwords && python3.10 -m nltk.downloader punkt

CMD ["./startup-script.sh"]
