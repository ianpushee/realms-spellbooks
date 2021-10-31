#! /bin/bash

# Giantsquid'd Apache configuration doesn't seem to let CGI scripts be
# executed if they're symlinks, at least into ~epw.

PUBLIC_HTML=$HOME/public_html
CGI_BIN=$PUBLIC_HTML/cgi-bin

function replace_with_cgi_symlink() {
    file="$1"
    cgi_bin_location="$CGI_BIN/$1"
    mv "$file" "$cgi_bin_location"
    chmod a+x "$cgi_bin_location"
    ln -s "$cgi_bin_location" "$file"
}

cd "`dirname $0`"
cd cgi-bin
for f in *; do
    replace_with_cgi_symlink $f
done
