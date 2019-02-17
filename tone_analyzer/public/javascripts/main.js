addEventListener('load', loadSite);

function loadSite() {
  $('.ui.form')
    .form({
      fields: {
        search_term: {
          identifier: 'search_term',
          rules: [
            {
              type: 'regExp[/^@?(\\w){1,35}$/]',
              prompt: 'Invalid search term'
            }
          ]
        }
      }
    })
  ;

  // button.addEventListener("on")
  $('.form').submit(async (e) => {
    const search_term = $("#search_term").val();

    if (!/^@?(\w){1,35}$/.test(search_term)) {
      return;
    }

    console.log("Analyzing search_term " + search_term);

    const button = document.querySelector('.ui.submit');

    button.disabled = true;
    await analyze(search_term);
    button.disabled = false;

  });

}

async function analyze(search_term) {
  const loading = document.querySelector("#loadingCircle");

  loading.classList.add("active");

  let type = "twitter";

  if (window.location.pathname.endsWith("reddit")) {
    type = "reddit";
  }
  // run python script
  console.log("request sent");
  let response;
  if (type === "twitter") {
    response = await fetch(window.location.href + 'twitter/' + search_term);
  } else {
    response = await fetch(window.location.href + '/' + search_term);

  }
  const results = await response.json();
  console.log("results received");
  console.log(results);

  const resultsDiv = document.querySelector("#results");

  if (Object.keys(results).length > 0) {
    let htmlToInsert = ""; //results.html;
    htmlToInsert += `<iframe src=\"${type}-graph.html\" width='100%' height='70%'>Your browser does not support iframes</iframe>`;
    htmlToInsert += "<div class=\"ui one column vertically divided grid container\" style='margin-top:30px'>";
    htmlToInsert += "<p>Recent Posts: </p>";
    let n = 10;
    for (let tweet of results.tweetList) {
      htmlToInsert += "<div class=\"row\"><div class=\"column\">";
      htmlToInsert += "<p>" + tweet.split("KNIJOU(*HIBJNKHUY&T^FYGVHBGUYTR%").join("'").split("JISDFOHD*S(HFINKJ@#(").join('"') + "</p></div></div>";
    }
    htmlToInsert += "</div>";

    resultsDiv.innerHTML = htmlToInsert;
  } else {
    alert("Your search term found no occurrences.");
  }

  // resultsDiv.innerHTML = JSON.stringify(results);

  loading.classList.remove("active");
}