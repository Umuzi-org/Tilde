FROM nixos/nix

RUN nix-channel --update


RUN nix-env -iA nixpkgs.nodejs_20
RUN nix-env -iA nixpkgs.python310
RUN nix-env -iA nixpkgs.python310Packages.pip
RUN nix-env -iA nixpkgs.jdk11
RUN nix-env -iA nixpkgs.gnused


ENV VENV_PATH /venv
RUN python3 -m venv $VENV_PATH
ENV PATH="$VENV_PATH/bin:$PATH"

RUN pip install -U pip setuptools wheel
RUN pip install poetry

ENV AUTOMARKER_2_CONFIG_DIR /app/automarker_2_config

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config installer.max-workers 10

RUN poetry install --verbose

# RUN poetry run python -m pip install -U spacy
# RUN poetry run python -m spacy download en_core_web_sm

COPY . .

ENV AUTO_MARKER_CLONE_PATH /gitignore
RUN mkdir $AUTO_MARKER_CLONE_PATH

# run migrations
RUN poetry run python manage.py migrate

EXPOSE 1337

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:1337"]