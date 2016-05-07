var express = require('express');
var favicon = require('serve-favicon');
var app = express();

app.use(express.static(__dirname));
// app.use(favicon(__dirname + '/public/img/favicon.ico'));

var port = process.env.PORT || 3000;
console.log("Express server running on " + port);
app.listen(process.env.PORT || port);
