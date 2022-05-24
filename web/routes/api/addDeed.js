var express = require('express');
var router = express.Router();
const mongoose = require('mongoose');
const schema = require('../../db_schema');

let addMember = (formData) => {
  return new Promise((rs, rj) => {
    schema.User.create(formData, function (err, docs) {
      if (err) {
        rj(err);
      }
      rs();
    })
  });
}

let addDeed = (formData) => {
  return new Promise((rs, rj) => {
    schema.User.find({ telegram: formData['telegram'] }, {}, async function (err, docs) {
      if (err) {
        rj(err);
      }
      if (docs.length == 0) {
        try {
          await addMember({ name: formData['name'], telegram: formData['telegram'], stupid_point: 0 })
        } catch(error) {
          rj(error);
        }
      } 
      schema.Deed.create(formData, function (err, docs) {
        if (err) {
          rj(err);
        }
        rs();
      });
    })
  });
}

let addPoint = (formData) => {
  return new Promise((rs, rj) => {
    schema.User.findOneAndUpdate({ telegram: formData['telegram'] }, { $inc: { 'stupid_point': formData['point'] } }, function (err, docs) {
      if (err) {
        rj(err);
      }
      rs();
    })
  });
}

router.post('/', async function (req, res, next) {
  let formData = req.body;
  let curDate = new Date();
  let date = `0${curDate.getMonth() + 1}`.slice(-2) + `0${curDate.getDate()}`.slice(-2)
  formData['date'] = date;
  try {
    let result_deed = await addDeed(formData);
    let result_add_point = await addPoint(formData);
    res.send(200);
  } catch (error) {
    console.log(error);
    res.send(error);
  }
});

module.exports = router;
