var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Stupid Ranking' });
});

router.get('/add-member', function(req, res, next) {
  res.render('addMember', { title: '新增成員' });
});

router.get('/add-deed', function(req, res, next) {
  res.render('addDeed', { title: '新增事蹟' });
});

module.exports = router;
