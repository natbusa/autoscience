# autoscience-ui
A UI to interact with the autoscience API

## Installation (Ubuntu/Debian)

#### 1. Packages needed: npm and nodejs
```
sudo apt-get install npm

curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### 2.1 Install some global npm packages 
```
sudo npm install -g http-server
sudo npm install -g bower
```

#### 2.2 you need compass for grunt
sudo gem install compass

#### 3. Build and start the webserver
NPM takes a while to install the packages the first time.The package are installed locally on the node_modules directory. As a post-install action, npm will also run `bower install` and run unit and e2e test before starting the npm http-server. For more information about the pre- and post npm install and start steps, check `package.json`.

```
npm install
npm start
```
#### 4. Check where your server has started.   
Go to your fav browser and type http://localhost:8000  
If you wish to configure the server on a different port check the `http-server` configuration in `package.json`.


Enjoy it :-)
