
//Esse bloco de codigo serve para ao fazer upload da imagem no /novo, alterar a imagem padrão pela imagem
//fornecida pelo usuario
document.getElementsByClassName('file-input')[0].addEventListener('change', function(e) {
    const imagem = document.getElementsByClassName('img-padrao')[0];
    const arquivo = e.target.files[0];
  
    if (!arquivo.type.match('image/jpeg')) {
      alert('Somente arquivos do tipo JPEG (.jpg) são aceitos!');
      return;
    }
  
    const reader = new FileReader();
  
    reader.onload = function(event) {
      imagem.src = event.target.result;
    }
  
    reader.readAsDataURL(arquivo);
  });
  