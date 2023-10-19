const sizes = document.querySelectorAll(".size");

sizes.forEach((size) => {
  size.addEventListener("click", () => {
    // Reset the background color of all labels to "bg-accent"
    sizes.forEach((otherLabel) => {
      otherLabel.classList.remove("bg-accent-focus", "border-black");
      otherLabel.classList.add("bg-accent-focus", "border-transparent");
    });

    // Set the clicked label's background color to "bg-accent-focus"
    size.classList.add("bg-accent-focus", "border-black");
    size.classList.remove("bg-accent-focus", "border-transparent");
  });
});

const colorLabels = document.querySelectorAll(".color-label");

colorLabels.forEach((color) => {
  color.addEventListener("click", () => {
    // Reset the border color of all labels to "transparent"
    colorLabels.forEach((otherLabel) => {
      otherLabel.classList.remove("border-accent");
      otherLabel.classList.add("border-transparent");
    });

    // Set the clicked label's background color to "bg-accent-focus"
    color.classList.add("border-accent");
    color.classList.remove("border-transparent");
  });
});
