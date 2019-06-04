FROM node:11.14.0-alpine

WORKDIR /usr/src/app

# add node_modules/.bin to PATH
ENV PATH /usr/src/app/node_modules/.bin:$PATH

# app dependencies
COPY package.json /usr/src/app/package.json
COPY package-lock.json /usr/src/app/package-lock.json
RUN npm ci
RUN npm install react-scripts --silent

CMD ["npm", "start"]
