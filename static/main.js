// 리스트 보여주기
function append_list(rows) {
    const element = document.querySelector('.list');
    element.replaceChildren();
  
    rows.forEach((element) => {
      const videolink = element['videolink'];
      const thumbnail = videolink.slice(32);
      let link = '';
  
      if (thumbnail.length === 11) {
        link = `https://i1.ytimg.com/vi/${thumbnail}/sddefault.jpg`;
      } else {
        link = '../static/images/default.png';
      }
  
      const temp_html = `
        <div class="item">
          <div class="itemImage">
            <a href="${videolink}" target="_blank">
              <img src="${link}" alt="">
            </a>
          </div>
          <div class="itemDesc">
            <h1>${element['videoname']}</h1>
            <p>${element['videodesc']}</p>
          </div>
        </div>
      `;
      document.querySelector('.list').insertAdjacentHTML('beforeend', temp_html);
    })
  }
  
  // navbar JavaScript active
  function navbar_active() {
    document.querySelector('.navbar__menu li:nth-child(2)').classList.add('active');
  }