FROM nixos/nix

RUN nix-channel --update

COPY config.nix /root/.config/nixpkgs/

RUN nix-env -u --always --verbose
RUN nix-env -ivA nixpkgs.nodejs_20
RUN nix-env -ivA nixpkgs.python310
RUN nix-env -ivA nixpkgs.python310Packages.pip
RUN nix-env -ivA nixpkgs.jdk11
RUN nix-env -ivA nixpkgs.gnused
RUN nix-env -ivA nixpkgs.gcc
RUN nix-env -ivA nixpkgs.zlib
RUN nix-env -ivA nixpkgs.gcc-unwrapped
RUN nix-env -ivA nixpkgs.stdenv.cc.cc.lib
RUN nix-env -ivA nixpkgs.cudaPackages.cudnn


ENV VENV_PATH /venv
RUN python3 -m venv $VENV_PATH
ENV PATH="$VENV_PATH/bin:$PATH"

RUN pip install -U pip setuptools wheel
RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock shell.nix ./

RUN poetry config installer.max-workers 10

RUN nix-shell --run "poetry install --verbose"

RUN nix-shell --run "poetry run python -m pip install -U spacy"
RUN nix-shell --run "poetry run python -m spacy download en_core_web_sm"

COPY . .

ENV AUTO_MARKER_CLONE_PATH /gitignore
RUN mkdir $AUTO_MARKER_CLONE_PATH

ENV AUTOMARKER_2_CONFIG_DIR /automarker_2_config

EXPOSE 1337

CMD nix-shell --run "poetry run python manage.py runserver 0.0.0.0:1337"