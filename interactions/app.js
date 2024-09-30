const path = require('node:path')
const fastify = require('fastify')
const fastifySession = require('@fastify/session');
const fastifyCookie = require('@fastify/cookie');
const fastifyView = require('@fastify/view');

// general properties, docker will allow changes
const port = 3000
const addr = '0.0.0.0'
const session_secret = process.env.SESSION_SECRET

/////////////////////
// CONFIGURING APP //
/////////////////////
const app = fastify({logger:true})
app.register(fastifyCookie);

app.register(fastifyView, {
  engine: {
    ejs: require("ejs")
  }
});

app.register(fastifySession, 
  {
    secret: session_secret,
    cookies: {
      secure: false,
    },
    saveUninitialized: false,
  }
);

app.register(require('@fastify/static'), {
    root: path.join(__dirname, 'static'),
  }
);
//////////////////////////////
// END OF APP CONFIGURATION //
//////////////////////////////

// adding routes
app.get('/', async (_request, reply) => {
  reply.status(200).send("to implement")
});

//////////////////////////////
// STATIC ROUTES DEFINITION //
//////////////////////////////
app.get('/main.css', function (req, reply) {
  reply.sendFile('main.css') 
})

app.get('/index.html', function (req, reply) {
  reply.sendFile('index.html') 
})
//////////////////////////////
// END OF ROUTES DEFINITION //
//////////////////////////////

// launching server
app.listen({host: addr, port: port}, error => {
  if (error) {
    app.log.fatal("stopping app")
    app.log.error(error)
    process.exit(1);
  }
});