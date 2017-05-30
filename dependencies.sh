#!/usr/bin/env bash

#export PATH="/Users/<your_user_name>/.pyenv:$PATH"
#eval "$(pyenv init -)"
#source ~/.bashrc
brew install pyenv phantomjs

pyenv install 3.6.1
pyenv local 3.6.1
pip install selenium sh terminaltables colorama