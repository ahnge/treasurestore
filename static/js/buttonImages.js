console.log("check");
var buttonImages = document.querySelectorAll(".button-image");
var mainImage = document.querySelector(".main-image");

// Change the main image src when button image is clicked
const buttonImageClickHandler = (buttonImage, mainImage, buttonImages) => {
  buttonImage.addEventListener("click", () => {
    // Change src of the main image
    mainImage.src = buttonImage.dataset.largeSrc;
    // Unhighlight the all button images
    [...buttonImages].forEach((bi) => {
      bi.classList.remove("border-primary");
      bi.classList.add("border-transparent");
    });
    // Highlight the button image
    buttonImage.classList.remove("border-transparent");
    buttonImage.classList.add("border-primary");
  });
};

[...buttonImages].forEach((buttonImage) => {
  buttonImageClickHandler(buttonImage, mainImage, buttonImages);
});

// When htmx swap happens; logic is made to happen again
var productImagesContainer = document.querySelector("#product-images");
productImagesContainer.addEventListener("htmx:afterSwap", (E) => {
  console.log(E.target);
  var buttonImages = E.target.querySelectorAll(".button-image");
  var mainImage = E.target.querySelector(".main-image");

  [...buttonImages].forEach((buttonImage) => {
    buttonImageClickHandler(buttonImage, mainImage, buttonImages);
  });
});
