document.getElementById("upload-btn").addEventListener("click", function () {
  document.getElementById("photo-input").click();
});

document
  .getElementById("photo-input")
  .addEventListener("change", function (event) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        document.getElementById("uploaded-image").src = e.target.result;
        document.getElementById("adjust-photo").classList.remove("hidden");
      };
      reader.readAsDataURL(file);
    }
  });

const focusCircle = document.querySelector(".focus-circle");
const photoPreview = document.querySelector(".photo-preview");

let isDragging = false;
let offsetX, offsetY;

focusCircle.addEventListener("mousedown", (e) => {
  isDragging = true;
  const rect = focusCircle.getBoundingClientRect();
  offsetX = e.clientX - rect.left;
  offsetY = e.clientY - rect.top;
});

document.addEventListener("mousemove", (e) => {
  if (isDragging) {
    const photoRect = photoPreview.getBoundingClientRect();
    const newX = e.clientX - photoRect.left - offsetX;
    const newY = e.clientY - photoRect.top - offsetY;

    if (newX >= 0 && newX <= photoRect.width - focusCircle.offsetWidth) {
      focusCircle.style.left = `${newX}px`;
    }
    if (newY >= 0 && newY <= photoRect.height - focusCircle.offsetHeight) {
      focusCircle.style.top = `${newY}px`;
    }
  }
});

document.addEventListener("mouseup", () => {
  isDragging = false;
});

document.getElementById("detect-btn").addEventListener("click", () => {
  const fileInput = document.getElementById("photo-input");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please upload a photo first.");
    return;
  }

  const formData = new FormData();
  formData.append("image", file);

  fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("detection-result").classList.remove("hidden");
      if (data.label === "Cataract") {
        document
          .getElementById("result-potential-cataract")
          .classList.remove("hidden");
        document.getElementById("result-normal").classList.add("hidden");
      } else if (data.label === "Normal") {
        document.getElementById("result-normal").classList.remove("hidden");
        document
          .getElementById("result-potential-cataract")
          .classList.add("hidden");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
