const carousel = document.getElementById("carousel");
const carouselItems = carousel.getElementsByClassName("carousel-item");
let currentActiveIndex = 0;

function scrollToNextItem() {
  currentActiveIndex = (currentActiveIndex + 1) % carouselItems.length;
  const nextItem = carouselItems[currentActiveIndex];
  nextItem.scrollIntoView({ behavior: "smooth", block: "center" });
  console.log("hi");
}

// Set the interval for auto-scrolling (e.g., every 3 seconds)
const autoScrollInterval = setInterval(scrollToNextItem, 3000);
