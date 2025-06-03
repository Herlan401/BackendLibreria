const { createProxyMiddleware } = require('http-proxy-middleware');
const express = require('express');
const cors = require('cors');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

app.use(cookieParser());

app.use(cors({
    origin: ['http://localhost:5173', 'http://127.0.0.1:5173'],
    credentials: true,
    allowedHeaders: [
        'Content-Type',
        'Authorization',
        'Accept',
        'X-Requested-With',
        'Access-Control-Allow-Origin',
        'Access-Control-Allow-Headers',
        'Access-Control-Allow-Methods',
        'Access-Control-Allow-Credentials',
    ]
}));

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const onProxyReq = (proxyReq, req, res) => {
    const token = req.cookies?.access;
    if (token) {
        proxyReq.setHeader('Authorization', 'Bearer ' + token);
    }
    if (req.body && ['POST', 'PUT', 'PATCH'].includes(req.method.toUpperCase())) {
        const bodyData = JSON.stringify(req.body);
        if (!res.headersSent) {
            proxyReq.setHeader('Content-Type', 'application/json');
            proxyReq.setHeader('Content-Length', Buffer.byteLength(bodyData));
            proxyReq.write(bodyData);
        }
    }
};

const apiProxy = createProxyMiddleware({
    target: 'http://127.0.0.1:8000/libreria/',
    changeOrigin: true,
    pathRewrite: (path, req) => path.replace('/webproxy', ''),
    on: { proxyReq: onProxyReq }
});

app.use('/webproxy', apiProxy);

require('./routes/auth.routes')(app);

app.listen(port, () => {
    console.log(`Proxy server is running at http://localhost:${port}`);
});
