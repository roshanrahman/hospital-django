let isSideNavOpen = false;
const toggleButtons = document.querySelectorAll("#side-nav-toggle");
const sideNavItems = document.querySelectorAll(".side-nav-item.clickable");
const sideNav = document.querySelector("#side-nav");

toggleButtons.forEach(toggleButton => {
  toggleButton.addEventListener("click", () => {
    isSideNavOpen = !isSideNavOpen;
    if (isSideNavOpen) {
      sideNav.classList.add("open");
    } else {
      sideNav.classList.remove("open");
    }
  });
});

sideNavItems.forEach(item => {
  item.addEventListener("click", () => {
    handleSideNavClicked(item.id);
    console.log("it works");
  });
});

handleSideNavClicked = id => {
  switch (id) {
    case "dashboard":
      window.location = "/";
      break;
    case "new-appointment":
      window.location = "/new";
  }
};
