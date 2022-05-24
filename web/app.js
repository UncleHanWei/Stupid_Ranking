var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
const mongoose = require('mongoose');
require('dotenv').config()

var indexRouter = require('./routes/index');
var apiDeedRouter = require('./routes/api/addDeed');
var apiMemberRouter = require('./routes/api/addMember');
var apiRankRouter = require('./routes/api/getRank');

var app = express();

// db connection setup
mongoose.connect(process.env.DB_HOST || 'mongodb://localhost:27017/Stupid_Ranking');


// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/api/add/deed', apiDeedRouter);
app.use('/api/add/member', apiMemberRouter);
app.use('/api/get/rank', apiRankRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
