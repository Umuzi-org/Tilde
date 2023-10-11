# shell.nix

{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "automarker2_env";
  buildInputs = [
    pkgs.gcc
    pkgs.zlib
    pkgs.gcc-unwrapped.lib
    pkgs.stdenv.cc.cc.lib
    # pkgs.cudatoolkit
    pkgs.cudaPackages.cudnn
  ];

  # shellHook = ''
  #   export LD_LIBRARY_PATH="${pkgs.cudatoolkit}/lib:${pkgs.cudnn}/lib:${pkgs.gcc}/lib:${pkgs.zlib}/lib:${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH"
  # '';
  shellHook = ''
    export LD_LIBRARY_PATH="${pkgs.cudaPackages.cudnn}/lib:${pkgs.gcc}/lib:${pkgs.zlib}/lib:${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH"
  '';
}
