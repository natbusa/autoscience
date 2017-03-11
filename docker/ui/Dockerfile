FROM library/node

# Install Bower & Grunt
RUN npm install -g bower grunt-cli karma && echo '{ "allow_root": true }' > /root/.bowerrc

# Install Ruby
# Install some dependencies
RUN curl -L https://get.rvm.io | bash -s stable
RUN /usr/local/rvm/bin/rvm requirements
RUN /usr/local/rvm/bin/rvm install 2.4.0
RUN /usr/local/rvm/bin/rvm use 2.4.0

#install compass and set the env PATH
RUN /usr/local/rvm/bin/rvm 2.4.0 do gem install --conservative --no-rdoc --no-ri sass compass
ENV PATH=/usr/local/rvm/gems/ruby-2.4.0/wrappers:$PATH

# Bundle app source
RUN mkdir /application

# copy bower and npm install and config files
COPY bower.json /application
COPY package.json /application
COPY Gruntfile.js /application

# install http-server
RUN npm install -g http-server

# Define working directory.
WORKDIR /application
RUN npm install

# copy web app specific data
COPY src /application/src

#runs the app using nodejs http-server
EXPOSE 8000
CMD [ "npm", "start" ]
