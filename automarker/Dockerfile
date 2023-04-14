FROM nixos/nix

RUN nix-channel --update


RUN nix-env -iA nixpkgs.nodejs-19_x
RUN nix-env -iA nixpkgs.python39
RUN nix-env -iA nixpkgs.python39Packages.pip
RUN nix-env -iA nixpkgs.jdk11
RUN nix-env -iA nixpkgs.gnused

RUN npm install -g jasmine

WORKDIR /home/node/app

COPY package-lock.json  .
COPY package.json  .
RUN npm install

COPY . .

ENV AUTO_MARKER_CLONE_PATH /clone
RUN mkdir $AUTO_MARKER_CLONE_PATH

ENV AUTO_MARKER_CONFIGURATION_REPO_PATH /home/node/app/project_config

EXPOSE 1337

CMD [ "node", "app.mjs" ]
