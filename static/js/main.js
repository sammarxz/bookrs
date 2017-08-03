class InputMD {
  constructor(selector) {
    this.input = document.querySelectorAll(selector);
    this.bindEvents();
  }

  bindEvents() {
    this.input.forEach(function(el) {
       el.addEventListener('keyup', () => {
        if (el.value == '') return el.classList.remove('non-empty');
        el.classList.add('non-empty')
      })
    })
  }
}

class IndexForSiblings {
  static get(el) {
    let children = el.parentNode.children;

    for (var i = 0; i < children.length; i++) {
      let child = children[i];
      if (child == el) return i;
    }
  }
}

class TabsManager {
  constructor(selector_tab, controls_selector, indicator_selector) {
    this.tabs = document.querySelector(selector_tab);
    this.controls = document.querySelectorAll(controls_selector);
    this.indicator = document.querySelector(indicator_selector);
    this.handleClick = this.handleClick.bind(this);
    this.setIndicatorWidth();
    this.bindEvents();
  }

  setIndicatorWidth() {
    this.indicator.style.width =  this.controls[0].clientWidth + 'px';
  }

  bindEvents() {
    this.controls.forEach(button => {
      button.addEventListener('click', this.handleClick)
    })
  }

  handleClick(e) {
    e.preventDefault();
    let button = e.currentTarget;

    let position = IndexForSiblings.get(button);

    this.indicator.style.left = (position * this.indicator.clientWidth) + 'px';
    this.openTab(button.hash);
  }

  openTab(hash) {
    let tab = document.querySelector(hash);
    let position = IndexForSiblings.get(tab);

    this.tabs.querySelector('.container').style.left = -(position * 100) + '%';
  }
}

class AutoComplete {
  constructor(input_selector, base_url) {
    this.search = this.search.bind(this);
    this.input = document.querySelector(input_selector);
    this.url = base_url;
    this.value = '';
    this.interval = null;
    this.buildDataList();
    this.bindEvents();
  }

  bindEvents() {
    this.input.addEventListener('keyup', () => {
      if (this.input.value == this.value || this.input.value.length < 4) return;
      if (this.interval) window.clearInterval(this.interval);

      this.value = this.input.value;
      this.interval = window.setTimeout(this.search, 500);
    });
  }

  buildDataList() {
    this.dataList = document.createElement('datalist');
    this.dataList.id = 'datalist-autocomplete';
    document.querySelector('body').appendChild(this.dataList);
    this.input.setAttribute('list', 'datalist-autocomplete');
  }

  search() {
    Search.get(this.url + this.value).then(results => this.build(results));
  }

  build(response) {
    this.dataList.innerHTML = '';
    response.items.forEach(item => {
      let optionEl = document.createElement('option');
      optionEl.value = item.volumeInfo.title + '  —  ' + item.volumeInfo.authors[0];
      this.dataList.appendChild(optionEl);
    });
  }
}

class Search {
  static get(url) {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.send();
    return new Promise((resolve, reject) => {
      xhr.onreadystatechange = () => {
        if (xhr.readyState == 4) {
          if (xhr.status == 200) return resolve(JSON.parse(xhr.responseText));
          reject(xhr.status);
        }
      }
    });
  }
}

var e,t=document.getElementsByClassName("closebtn");

for(e=0;e<t.length;e++)t[e].onclick=function(){
  var e=this.parentElement;
  e.style.opacity="0", setTimeout(function(){
    e.style.display="none"
  },600);
}
