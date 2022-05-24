var express = require('express');
var router = express.Router();
const mongoose = require('mongoose');
const schema = require('../../db_schema');


let addMember = (formData) => {
  return new Promise((rs, rj) => {
    schema.User.find({ telegram: formData['telegram'] }, {}, function (err, docs) {
      if (err) {
        rj(err);
      }
      if (docs.length == 0) {
        schema.User.create(formData, function (err, docs) {
          if (err) {
            rj(err);
          }
          rs();
        })
      } else {
        rj('Duplicate');
      }
    })
  });
}

router.post('/', async function (req, res, next) {
  let formData = req.body;
  formData['stupid_point'] = 0;
  try {
    let result = await addMember(formData);
    res.send(200);
  } catch(error) {
    console.log(error);
    res.send(error);
  }
});

module.exports = router;
