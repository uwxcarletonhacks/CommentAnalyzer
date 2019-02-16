addEventListener('load', loadSite);

function loadSite() {
  let button = document.querySelector("#analyze");

  $('.ui.form')
    .form({
      fields: {
        username: {
          identifier: 'username',
          rules: [
            {
              type   : 'regExp[/^@?(\\w){1,15}$/]',
              prompt : 'Invalid username'
            }
          ]
        }
      }
    })
  ;

  // button.addEventListener("on")
  $('.form').submit(async (e) => {
    const username =$("#username").val();

    if (!/^@?(\w){1,15}$/.test(username)) {
      return;
    }

    console.log("Analyzing username " + username );

    const button = document.querySelector('.ui.submit');

    button.disabled = true;
    await analyze(username);
    button.disabled = false;

  });

}

async function analyze(username) {
  const loading = document.querySelector("#loadingCircle");

  loading.classList.add("active");

  // run python script
  console.log("request sent");
  const response = await fetch(window.location.href + 'twitter/' + username);
  const results = await response.json();
  console.log("results received");
  console.log(results);

  const resultsDiv = document.querySelector("#results");

  // let htmlToInsert = results.html;
  // htmlToInsert += "<div>"
  // for (let tweet of results.tweets) {
  //   htmlToInsert += "<p>" + tweet + "</p>";
  // }
  // htmlToInsert += "</div>";
  //
  // resultsDiv.innerHTML = htmlToInsert;

  resultsDiv.innerHTML = JSON.stringify(results);

  loading.classList.remove("active");
}