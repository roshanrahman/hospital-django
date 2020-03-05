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
    id: "doctor-dashboard",
    path: "/doctor/"
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
    id: "patient_documents",
    path: "/patient/documents"
  },
  {
    id: "doctor_appointments",
    path: "/doctor/appointments"
  },
  {
    id: "admin_users",
    path: "/view-users"
  },
  {
    id: "log_out",
    path: "/users/logout"
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

try {
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
} catch (error) {
  console.log(error);
}

const mainContent = document.querySelectorAll("main");
mainContent.forEach(main => {
  main.addEventListener("click", () => {
    isSideNavOpen = false;
    sideNav.classList.remove("open");
  });
});
