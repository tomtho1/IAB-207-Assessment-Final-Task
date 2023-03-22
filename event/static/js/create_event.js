function upload_photo(elem) {
    document.getElementById('image').click();
    elem.innerText = "Change Photo";
}

document.getElementById("upload").addEventListener("click", (e) => upload_photo(e.target));