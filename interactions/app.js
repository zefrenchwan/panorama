const fastify = require('fastify');
const fastifySession = require('@fastify/session');
const fastifyCookie = require('@fastify/cookie');

// general properties, docker will allow changes
const port = 3000
const addr = '0.0.0.0'
const session_secret = process.env.SESSION_SECRET

// configuring app
const app = fastify();
app.register(fastifyCookie);
app.register(fastifySession, {secret: session_secret});

// adding routes
app.get('/', (_request, reply) => {
   reply.status(200).send("Hello World");
});

// launching server
app.listen({host: addr, port: port}, error => {
  if (error) {
    process.exit(1);
  }
});