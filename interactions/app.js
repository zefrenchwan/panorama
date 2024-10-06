const path = require('node:path')
const fastify = require('fastify')
const fastifySession = require('@fastify/session');
const fastifyCookie = require('@fastify/cookie');
const fastifyView = require('@fastify/view');
const fastifyForms = require('@fastify/formbody')
const crypto = require("crypto");
const ioredis = require('ioredis');

// general properties, generated for the moment 
const port = 3000
const addr = '0.0.0.0'
const session_secret = crypto.randomBytes(128).toString('hex');
const cookie_secret= crypto.randomBytes(64).toString('hex');
const redis_url = process.env.REDIS_URL 

/////////////////////
// CONFIGURING APP //
/////////////////////
const appDirectory = __dirname
const appContentDir = path.join(appDirectory, 'static')
const app = fastify({logger:true})
app.register(fastifyCookie, { secret: cookie_secret });
app.register(fastifyForms, { bodyLimit: 5100 });
app.register(require('@fastify/static'), { root: appContentDir, });

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

const redisClient = new ioredis(redis_url)
app.register(require('@fastify/redis'), { client: redisClient, closeClient: true })

//////////////////////////////
// END OF APP CONFIGURATION //
//////////////////////////////

// adding routes
app.get('/dashboard', (req, resp) => {
  const sessionId = req.cookies.sessionId
  if (!sessionId) {
    resp.redirect("/index.html")
    return resp
  }

  app.redis.get("sid:"+ sessionId, (err, val) => {
    if (err) {
      app.logger.error("error when getting user data" + err)
      resp.redirect("/index.html")
    } else {
      templateLocation = path.join('static', 'dashboard.ejs')
      resp.view(templateLocation, { username: val })
    }
  })
})


app.post('/auth', (req, resp) => {

  const formContent = req.body
  const username = formContent.uname
  const password = formContent.upass
  // test username and password
  
  // if it matches, adds it
  const sessionId = crypto.randomBytes(24).toString("hex");
  app.redis.set("sid:" + sessionId, username, (err) => {
    if (err) {
      app.log.error("error when writing user session data to redis " + err)
    }
  })

  resp.setCookie('sessionId', sessionId, {
    path: '/', 
    expires: new Date(Date.now() + 12 * 60 * 60 * 1000),
    httpOnly: true, 
    sameSite: 'Strict' 
  })

  resp.redirect("/dashboard")
})

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