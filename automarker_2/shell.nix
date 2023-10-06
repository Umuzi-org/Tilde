# shell.nix

{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "automarker2_env";
  buildInputs = [
    pkgs.gcc
    pkgs.zlib
    pkgs.gcc-unwrapped.lib
    pkgs.stdenv.cc.cc.lib
  ];

  shellHook = ''
    export LD_LIBRARY_PATH="${pkgs.gcc}/lib:${pkgs.zlib}/lib:${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH"
  '';
}
