console.log("sanity check");
const sortHighPrice = document.querySelector("#sort-high-price");
const sortLowPrice = document.querySelector("#sort-low-price");

const filterFormSort = document.querySelector("#filter-form-sort");
const filterFormSubmitBtn = document.querySelector("#filter-form-submit-btn");

sortHighPrice.addEventListener("click", () => {
  filterFormSort.value = "high_price";
  filterFormSubmitBtn.click();
});

sortLowPrice.addEventListener("click", () => {
  filterFormSort.value = "low_price";
  filterFormSubmitBtn.click();
});
