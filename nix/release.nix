let
  nixpkgs = import ./nixpkgs.nix { inherit config; };
  config = {
    packageOverrides = pkgs: rec {
      haskellPackages = pkgs.haskellPackages.override { overrides = haskOverrides; };

      gmsh = pkgs.gmsh.overrideAttrs (old: {
        cmakeFlags = old.cmakeFlags or [] ++ [
          "-DENABLE_BUILD_LIB=1"
          "-DENABLE_BUILD_SHARED=1"
          "-DENABLE_OPENMP=1"
        ];
      });

    };
  };
  gitignore = nixpkgs.callPackage (nixpkgs.fetchFromGitHub {
    owner  = "siers";
    repo   = "nix-gitignore";
    rev    = "ce0778ddd8b1f5f92d26480c21706b51b1af9166";
    sha256 = "1d7ab78i2k13lffskb23x8b5h24x7wkdmpvmria1v3wb9pcpkg2w";
  }) {};
  ignore = gitignore.gitignoreSourceAux ''
    .stack-work
    dist
    dist-newstyle
    .ghc.environment*
    '';
    haskOverrides = new: old: {
        haskell-gmsh = new.callCabal2nix "haskell-gmsh" (ignore ../.) {};
      };
in {
  inherit nixpkgs;
  release-packages = {
    inherit (nixpkgs.haskellPackages)
    haskell-gmsh
    ;
  };
}
