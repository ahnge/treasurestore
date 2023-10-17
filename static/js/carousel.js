const carousel = document.getElementById("carousel");
const carouselItems = carousel.getElementsByClassName("carousel-item");
let currentActiveIndex = 0;

function scrollToNextItem() {
  currentActiveIndex = (currentActiveIndex + 1) % carouselItems.length;
  const nextItem = carouselItems[currentActiveIndex];
  carousel.scrollTo({
    top: 0,
    left: nextItem.offsetLeft,
    behavior: "smooth",
  });
}

// Set the interval for auto-scrolling (e.g., every 3 seconds)
const autoScrollInterval = setInterval(scrollToNextItem, 3000);
