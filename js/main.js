/* M. Walker / RiskByDesign - site behaviour.
   Vanilla JS only. No dependencies, no network calls, no tracking. */

(function () {
  "use strict";

  document.documentElement.classList.remove("no-js");

  /* Footer year */
  var year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());

  /* Mobile nav toggle */
  var toggle = document.querySelector(".nav-toggle");
  var menu = document.getElementById("nav-menu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = menu.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    /* Close the menu after choosing a section */
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) {
        menu.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* Scroll reveal */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0, rootMargin: "0px 0px -40px 0px" }
    );
    reveals.forEach(function (el) {
      observer.observe(el);
    });
    /* Safety net: if any .reveal has not been marked visible after 800 ms
       (e.g. it is taller than the viewport can intersect, or the observer
       misfires), force it visible so content is never permanently hidden. */
    setTimeout(function () {
      reveals.forEach(function (el) {
        if (!el.classList.contains("is-visible")) {
          el.classList.add("is-visible");
        }
      });
    }, 800);
  } else {
    document.documentElement.classList.add("no-observer");
  }
})();
