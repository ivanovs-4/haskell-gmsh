let
  release = import ./nix/release.nix;
  nixpkgs = release.nixpkgs;

in
  nixpkgs.stdenv.mkDerivation {
    name = "env";
    nativeBuildInputs = with nixpkgs.haskellPackages; [
      cabal-install
      hpack
    ];
    buildInputs = with nixpkgs; [
      gmsh
    ]
    ++ (with nixpkgs.haskellPackages; [
      release.release-packages.haskell-gmsh
    ])
    ;
  }
