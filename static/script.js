setTimeout(() => {
  const box = document.getElementById('msg-modal');
  box.style.display = 'none';
}, 2000);

setTimeout(() => {
  const box = document.getElementById('msg-modal-home');
  box.style.display = 'none';
}, 2000);


function previewBeforeUpload(){
  document.getElementById("id_image").addEventListener("change",function(e){
    if(e.target.files.length == 0){
      return;
    }
    let file = e.target.files[0];
    let url = URL.createObjectURL(file);
    document.querySelector("#id_image img").src = url;
  });
}

previewBeforeUpload();