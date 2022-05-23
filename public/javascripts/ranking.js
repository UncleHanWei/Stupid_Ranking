function showRank(data) {
  document.getElementById('ranking').innerHTML = '';
  let html = `<li class="champion">#1 ${data[0]['name']} ${data[0]['stupid_point']} 分</li>`;
  for(let i = 1; i < data.length; i++) {
    html += `<li class="rank">#${i+1} ${data[i]['name']} ${data[i]['stupid_point']} 分</li>`;
  }
  document.getElementById('ranking').innerHTML = html;
}


var requestOptions = {
  method: 'GET',
  redirect: 'follow'
};

fetch("/api/get/rank", requestOptions)
  .then(response => response.text())
  .then(result => showRank(JSON.parse(result)))
  .catch(error => console.log('error', error));