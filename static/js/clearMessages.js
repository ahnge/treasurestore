setTimeout(() => {
  try {
    document.querySelector("#messages").innerHTML = "";
  } catch (error) {
    console.log(error);
  }
}, 5 * 1000);
