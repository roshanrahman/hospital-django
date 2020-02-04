let isSideNavOpen = false;
const toggleButtons = document.querySelectorAll("#side-nav-toggle");
const sideNavItems = document.querySelectorAll(".side-nav-item.clickable");
const sideNav = document.querySelector("#side-nav");

const paths = [
  {
    id: "dashboard",
    path: "/"
  },
  {
    id: "new_appointment",
    path: "/new"
  },
  {
    id: "admin_users",
    path: "/view-users"
  }
];

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
    console.log("Clicked ", item);
  });
});

handleSideNavClicked = id => {
  paths.forEach(map => {
    if (map.id === id) {
      window.location = map.path;
    }
  });
};
