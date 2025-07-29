document.getElementById("imageInput").addEventListener("change", function () {
  const file = this.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      const img = document.getElementById("previewImage");
      img.src = e.target.result;
      img.style.display = "block";
    };
    reader.readAsDataURL(file);
  }
});
<script>
  const title = "♻️ WasteWise - Your Smart Waste Classifier";
  let i = 0;
  function typeWriter() {
    if (i < title.length) {
      document.querySelector("header h1").innerHTML += title.charAt(i);
      i++;
      setTimeout(typeWriter, 70);
    }
  }
  document.querySelector("header h1").innerHTML = "";
  typeWriter();
</script>
document.getElementById("uploadForm").addEventListener("submit", function (event) {
  event.preventDefault();

  const formData = new FormData(this);

  // Show loader and hide previous result
  document.getElementById("loaderContainer").style.display = "block";
  document.getElementById("successContainer").style.display = "none";
  document.getElementById("result").innerText = "";

  fetch("/classify", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      // Hide loader, show success tick
      document.getElementById("loaderContainer").style.display = "none";
      document.getElementById("successContainer").style.display = "block";

      // Show prediction result after a short delay
      setTimeout(() => {
        document.getElementById("result").innerText = `Prediction: ${data.class}`;
      }, 1000);
    })
    .catch((error) => {
      console.error("Error:", error);
      document.getElementById("loaderContainer").style.display = "none";
      document.getElementById("result").innerText = "Error occurred!";
    });
});
