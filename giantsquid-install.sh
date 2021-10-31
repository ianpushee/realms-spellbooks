#! /bin/bash

# Giantsquid'd Apache configuration doesn't seem to let CGI scripts be
# executed if they're symlinks, at least into ~epw.

PUBLIC_HTML=$HOME/public_html
CGI_BIN=$PUBLIC_HTML/cgi-bin

function replace_with_cgi_symlink() {
    mv "$1" "$CGI_BIN/$1"
    ln -s "$CGI_BIN/$1" "$1"
}

cd "`dirname $0`"
cd cgi-bin
for f in *; do
    replace_with_cgi_symlink $f
done
