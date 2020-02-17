let isSideNavOpen = false;
const toggleButtons = document.querySelectorAll("#side-nav-toggle");
const sideNavItems = document.querySelectorAll(".side-nav-item.clickable");
const sideNav = document.querySelector("#side-nav");
const alerts = document.querySelectorAll(".alert");

const paths = [
  {
    id: "dashboard",
    path: "/"
  },
  {
    id: "new_appointment",
    path: "/patient/new_appointment"
  },
  {
    id: "patient_profile",
    path: "/patient/profile"
  },
  {
    id: "doctor_profile",
    path: "/doctor/profile"
  },
  {
    id: "patient_appointments",
    path: "/patient/appointments"
  },
  {
    id: "doctor_appointments",
    path: "/doctor/appointments"
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

alerts.forEach(alert => {
  alert.addEventListener("click", () => {
    alert.style.display = "none";
  });
  setTimeout(() => {
    alert.style.display = "none";
  }, 3000);
});

const expandToggleAreaElement = document.getElementById("expand-area");
const expandToggleElement = document.getElementById("expand-toggle");
const expandToggleIndicatorElement = document.getElementById(
  "expand-toggle-indicator"
);

expandToggleAreaElement.style.display = "none";

expandToggleElement.addEventListener("click", () => {
  const isHidden = expandToggleAreaElement.style.display === "none";
  if (isHidden) {
    expandToggleAreaElement.style.display = "flex";
    expandToggleIndicatorElement.style.transform = "rotate(180deg)";
  } else {
    expandToggleAreaElement.style.display = "none";
    expandToggleIndicatorElement.style.transform = "rotate(0deg)";
  }
});
