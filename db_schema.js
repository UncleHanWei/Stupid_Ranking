const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const User = new Schema({
  name: String,
  stupid_point: Number,
  telegram: String
})

const Deed = new Schema({
  telegram: String,
  name: String,
  Deed: String,
  point: Number,
  date: String
})

module.exports = {
  User: mongoose.model('User', User),
  Deed: mongoose.model('Deed', Deed)
}