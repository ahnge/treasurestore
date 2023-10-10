const addToCartForm = document.querySelector("#add-to-cart-form");

addToCartForm.addEventListener("htmx:beforeRequest", () => {
  // Disable the add-to-cart-btn while requesting
  addToCartForm.querySelector("button").disabled = true;
  addToCartForm.querySelector(
    "button"
  ).innerHTML = `<span class="loading loading-spinner"></span>Loading`;
});

addToCartForm.addEventListener("htmx:afterRequest", () => {
  // Enable the add-to-cart-btn while requesting
  addToCartForm.querySelector("button").disabled = false;
  addToCartForm.querySelector("button").innerHTML = `Add to cart`;
  // Change the cart quantity back to 1
  addToCartForm.querySelector("#quantity").value = 1;
});
