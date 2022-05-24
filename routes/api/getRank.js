var express = require('express');
var router = express.Router();
const mongoose = require('mongoose');
const schema = require('../../db_schema');

let getAllUser = () => {
  return new Promise((rs, rj) => {
    schema.User.find({}, {}, { sort: { 'stupid_point': -1 } }, function (err, docs) {
      if (err) {
        rj(err);
      }
      rs(docs);
    });
  });
}

/* GET home page. */
router.get('/', async function (req, res, next) {
  try {
    let data = await getAllUser();
    res.send(data);
  } catch (error) {
    console.log(error);
    res.send(error);
  }
});

module.exports = router;
