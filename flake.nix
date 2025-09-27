{
  description = "shell for voc/intro-outro-generator";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; config.allowUnfree = true; };
        pyEnv = pkgs.python3.withPackages (ps: with ps; [
          lxml
          cssutils
          pillow
          wand
        ]);
        fonts = with pkgs; [
          dejavu_fonts
          noto-fonts
          noto-fonts-emoji
          noto-fonts-cjk-sans
        ];
      in {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            pyEnv
            inkscape
            ffmpeg
            imagemagick
            libxml2
            libxslt
            git
            pkg-config
            which
          ] ++ fonts;

          shellHook = ''
            # Compatibility: some docs mention libav-tools/avconv
            alias avconv="ffmpeg"

            export MAGICK_CONFIGURE_PATH=${pkgs.imagemagick}/etc/ImageMagick-7
            export FONTCONFIG_PATH=${pkgs.fontconfig.out}/etc/fonts
            export FONTCONFIG_FILE=${pkgs.fontconfig.out}/etc/fonts/fonts.conf
            fc-cache -r >/dev/null 2>&1 || true

            echo "Ready. Example: ./make.py yourproject/ --debug"
          '';
        };
      });
}

