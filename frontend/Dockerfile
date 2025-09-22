FROM node:18

WORKDIR /app

COPY package*.json ./


ARG NODE_ENV=development
ENV NODE_ENV=$NODE_ENV

RUN npm ci

COPY . .

EXPOSE 3000
CMD ["npm", "start"]
