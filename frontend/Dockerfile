FROM node:slim

RUN mkdir -p /src/nuxt-app
WORKDIR /src/nuxt-app
COPY . .
RUN npm i
RUN npm cache clean --force
RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "start"]