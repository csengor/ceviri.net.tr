window.onload = function() {
  const fileUploadMessage = document.getElementById('file-upload-message');
  const loadDiv = document.getElementById('loading')
  const sourceLanguageSelect = document.getElementById('source-language');
  const targetLanguageSelect = document.getElementById('target-language');
  const sourceTextarea = document.getElementById('source-text');
  const targetTextarea = document.getElementById('target-text');

  let timer;

  document.body.removeAttribute('class');

  document.getElementById('btn-agree').onclick = function() {
    document.getElementById('disclaimer').classList.add('hidden');
  }

  document.getElementById('btn-select-text').onclick = function() {
    document.getElementById('btn-select-doc').classList.remove('selected');
    this.classList.add('selected');
    document.getElementById('doc-to-translate').classList.add('hidden');
    document.getElementById('text-to-translate').classList.remove('hidden');
  }

  document.getElementById('btn-select-doc').onclick = function() {
    document.getElementById('btn-select-text').classList.remove('selected');
    this.classList.add('selected');
    document.getElementById('text-to-translate').classList.add('hidden');
    document.getElementById('doc-to-translate').classList.remove('hidden');
  }

  sourceLanguageSelect.onchange = function() {
    if (this.value == 'en') {
      targetLanguageSelect.value = 'tr';
    }
    else {
      targetLanguageSelect.value = 'en';
    }
  }

  targetLanguageSelect.onchange = function() {
    if (this.value == 'en') {
      sourceLanguageSelect.value = 'tr';
    }
    else {
      sourceLanguageSelect.value = 'en';
    }
  }

  sourceTextarea.onkeyup = function(){
    clearTimeout(timer);
    if (sourceTextarea.value != ''){
      timer = setTimeout(translateText, 1500);
    }
  }

  document.getElementById('file-upload').onchange = function() {
    translateDoc(this.files[0]);
  }

  function translateDoc(file) {
    fileUploadMessage.textContent = file.name;

    loadDiv.classList.remove('hidden');

    docFormData = new FormData()

    docFormData.append('type', 'doc');
    docFormData.append('source', file);
    docFormData.append('source_language', sourceLanguageSelect.value);

    fetch('',
      {method: 'POST',
       headers: {
         'X-CSRFToken': getCookie('csrftoken')
       },
       body: docFormData
      })
      .then(response => response.json())
      .then(data => {
        setTimeout(function(){checkQuery(data.secret, 'doc', file.name)}, 1000);
      })
  }

  function translateText() {
    loadDiv.classList.remove('hidden');

    textFormData = new FormData()

    textFormData.append('type', 'text');
    textFormData.append('source_text', sourceTextarea.value);
    textFormData.append('source_language', sourceLanguageSelect.value);

    fetch('',
      {method: 'POST',
       headers: {
         'X-CSRFToken': getCookie('csrftoken')
       },
       body: textFormData
      })
      .then(response => response.json())
      .then(data => {
        setTimeout(function(){checkQuery(data.secret, 'text')}, 1000);
      })
  }

  function checkQuery(secret, type, name=null) {
    fetch('/query/' + secret)
      .then((response) => {
        if (response.status === 200)
        {
          if (type === 'doc')
          {
            response.blob()
            .then(blob => {
              let file = window.URL.createObjectURL(blob);
              let link = document.createElement('a');
              link.href = file;
              link.download = name;
              link.click();
            })
          }
          else
          {
            response.json()
            .then(data => {
                targetTextarea.value = data.translation;
            })
          }
          loadDiv.classList.add('hidden');
        }
        else
        {
          setTimeout(function(){checkQuery(secret, type, name)}, 3000)
        }
      })

  }

  // https://docs.djangoproject.com/en/4.0/ref/csrf/#acquiring-the-token-if-csrf-use-sessions-and-csrf-cookie-httponly-are-false
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
}
