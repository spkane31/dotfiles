# dotfiles

Config files, symlinked into place on any machine via `install.sh`.

## Install

    git clone https://github.com/spkane31/dotfiles.git ~/dotfiles
    ~/dotfiles/install.sh

Existing files at the destination are backed up to `.backup/<hostname>/`
inside this repo before being replaced with a symlink. Re-running is safe —
files already linked correctly are left untouched.

## Adding a new file

Append an entry to the `FILES` array in `install.sh`:

    "path/in/repo:$HOME/local/path"
