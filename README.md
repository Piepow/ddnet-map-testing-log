# DDNet Map Testing Log Panel

http://beeteam.de/testing-log/

Web interface to DDNet's map testing system on Discord.

## Installation Instructions

```sh
git clone https://github.com/Piepow/ddnet-map-testing-log.git
cd ddnet-map-testing-log
composer install
npm install
cp -r config-example config
# Edit the files in `config/` to suit your needs, particularly `config/app.php`
# and `config/common/project.php`
cp -r resources/logs-example resources/logs
# Note that the Discord bot that generates these logs aren't actually in this
# repository
mkdir public/assets/logs
ln -s $(readlink -f resources/logs/files) public/assets/logs/files
```
