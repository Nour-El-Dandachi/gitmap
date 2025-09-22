FROM node:18

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install --include=dev

COPY . .

EXPOSE 3000
CMD ["npm", "start"]
