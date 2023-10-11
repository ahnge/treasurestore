const incrementCarts = document.querySelectorAll(".increment-cart");
const decrementCarts = document.querySelectorAll(".decrement-cart");

const updateTotal = (e, type) => {
  // Update the total value
  const totalTag = e.target.parentElement.parentElement.querySelector(".total");
  const price =
    e.target.parentElement.parentElement.querySelector(".price").innerHTML;
  let newTotal = 0;
  if (type === "increment") {
    newTotal = parseInt(totalTag.innerHTML) + parseInt(price);
  } else if (type == "decrement") {
    newTotal = parseInt(totalTag.innerHTML) - parseInt(price);
    // Remove the row if cart item count becomes zero or newTotal becomes zero
    if (newTotal <= 0) {
      e.target.parentElement.parentElement.remove();
    }
  }
  totalTag.innerHTML = newTotal;
};

incrementCarts.forEach((incrementCart) => {
  incrementCart.addEventListener("htmx:beforeRequest", (e) => {
    e.target.disable = true;
    e.target.innerHTML = "<span class='loading loading-spinner'></span>";
  });

  incrementCart.addEventListener("htmx:afterRequest", (e) => {
    e.target.disable = false;
    e.target.innerHTML = "+";
    updateTotal(e, "increment");
  });
});

decrementCarts.forEach((decrementCart) => {
  decrementCart.addEventListener("htmx:beforeRequest", (e) => {
    e.target.disable = true;
    e.target.innerHTML = "<span class='loading loading-spinner'></span>";
  });

  decrementCart.addEventListener("htmx:afterRequest", (e) => {
    e.target.disable = false;
    e.target.innerHTML = "-";
    updateTotal(e, "decrement");
  });
});
