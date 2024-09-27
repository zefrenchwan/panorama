const server = require('fastify')({ logger: true })
const port = 3000
const addr = '0.0.0.0'

server.get('/', (_request, reply) => {
   reply.status(200).send("Hello World");
});

server.listen({host: addr, port: port}, error => {
  if (error) {
    process.exit(1);
  }
});