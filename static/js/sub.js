function showFile() {
    let fileExtension = file.name.split('.').pop().toLowerCase();
    let validExtensions = ["jpeg", "jpg", "png", "xlsx"]; // agregar "xlsx" como una extensión válida
  
    if (validExtensions.includes(fileExtension)) {
      // Si la extensión es válida
      let fileReader = new FileReader();
  
      fileReader.onload = () => {
        let fileURL = fileReader.result;
        let fileTag = "";
  
        if (validExtensions.includes(fileExtension)) {
          // Si la extensión es una imagen, muestra una etiqueta img
          fileTag = `<img src="${fileURL}" alt="">`;
        } else if (fileExtension === "xlsx") {
          // Si la extensión es xlsx, puedes personalizar cómo mostrar el archivo Excel
          fileTag = `<i class="fas fa-file-excel"></i>`;
        }
  
        dropArea.innerHTML = fileTag;
      };
  
      fileReader.readAsDataURL(file);
    } else {
      alert("This is not a valid file format!");
      dropArea.classList.remove("active");
      dragText.textContent = "Drag & Drop to Upload File";
    }
  }
  