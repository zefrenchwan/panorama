FROM node:22-bookworm

ENV SESSION_SECRET=c7b7939f8bfc1299f040cf6ded40442419aff3a4282c082f0725b7b7a204f1131e660c0ab0241ce53425b079a64763b7023ac8f57c9e4a5f1f48f055c2128244
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY --chown=node:node . .
EXPOSE 3000
CMD [ "node", "app.js"]