var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/:keyword', async (req, res) => {
  const keyword = req.params.keyword;

  let {PythonShell} = require('python-shell');

  const options = {
    mode: 'text',
    pythonPath: '/usr/local/bin/python3',
    scriptPath: 'public',
    args: [keyword]
  };

  console.log('running');
  const pyshell = new PythonShell('twitter.py', options);

  pyshell.on('message', function (message) {
    // received a message sent from the Python script (a simple "print" statement)
    const jversion = JSON.parse(message.replace(/'/g, "\""));
    console.log(jversion);

    res.json(jversion);
  });

  pyshell.end(function (err,code,signal) {
    if (err) throw err;
    console.log('The exit code was: ' + code);
  });
});


module.exports = router;
