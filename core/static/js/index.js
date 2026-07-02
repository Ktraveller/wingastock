/* =========================================
WINGA PLATFORM
MAIN JAVASCRIPT
========================================= */

document.addEventListener("DOMContentLoaded", () => {

```
initStatsCounter();
initSmoothScroll();
initWishlistButtons();
initDarkMode();
initSearchSuggestions();
```

});

/* =========================================
STATISTICS COUNTER
========================================= */

function initStatsCounter() {

```
const counters = document.querySelectorAll(".stat-card h2");

counters.forEach(counter => {

    const target =
        parseInt(counter.innerText.replace(/\D/g, "")) || 0;

    let current = 0;

    const increment = target / 100;

    const updateCounter = () => {

        if (current < target) {

            current += increment;

            counter.innerText =
                Math.ceil(current) + "+";

            requestAnimationFrame(updateCounter);

        } else {

            counter.innerText =
                target.toLocaleString() + "+";
        }
    };

    updateCounter();
});
```

}

/* =========================================
SMOOTH SCROLL
========================================= */

function initSmoothScroll() {

```
document
    .querySelectorAll('a[href^="#"]')
    .forEach(anchor => {

        anchor.addEventListener("click", function(e) {

            const target =
                document.querySelector(
                    this.getAttribute("href")
                );

            if (!target) return;

            e.preventDefault();

            target.scrollIntoView({
                behavior: "smooth"
            });
        });
    });
```

}

/* =========================================
WISHLIST BUTTONS
========================================= */

function initWishlistButtons() {

```
const buttons =
    document.querySelectorAll(".wishlist-btn");

buttons.forEach(btn => {

    btn.addEventListener("click", () => {

        btn.classList.toggle("active");

        if(btn.classList.contains("active")){

            btn.innerHTML =
                '<i class="fa-solid fa-heart"></i>';

        }else{

            btn.innerHTML =
                '<i class="fa-regular fa-heart"></i>';
        }
    });
});
```

}

/* =========================================
DARK MODE
========================================= */

function initDarkMode() {

```
const toggle =
    document.getElementById("darkModeToggle");

if (!toggle) return;

toggle.addEventListener("click", () => {

    document.body.classList.toggle("dark-mode");

    const darkMode =
        document.body.classList.contains(
            "dark-mode"
        );

    localStorage.setItem(
        "wingaDarkMode",
        darkMode
    );
});

if (
    localStorage.getItem(
        "wingaDarkMode"
    ) === "true"
) {
    document.body.classList.add("dark-mode");
}
```

}

/* =========================================
SEARCH SUGGESTIONS
========================================= */

function initSearchSuggestions() {

```
const searchInput =
    document.querySelector(
        ".search-box input"
    );

if (!searchInput) return;

const suggestions = [

    "iPhone 15 Pro Max",
    "Samsung Galaxy",
    "Gaming Laptop",
    "Toyota Harrier",
    "Office Chair",
    "Agriculture Tools",
    "Land for Sale",
    "Men's Shoes",
    "Women's Fashion",
    "Beauty Products"

];

searchInput.addEventListener(
    "input",
    function() {

        const value =
            this.value.toLowerCase();

        console.log(
            suggestions.filter(item =>
                item
                .toLowerCase()
                .includes(value)
            )
        );
    }
);
```

}

/* =========================================
PRODUCT IMAGE HOVER
========================================= */

const productImages =
document.querySelectorAll(
".product-image img"
);

productImages.forEach(img => {

```
img.addEventListener("mouseenter", () => {

    img.style.transform =
        "scale(1.08)";

    img.style.transition =
        "0.4s ease";
});

img.addEventListener("mouseleave", () => {

    img.style.transform =
        "scale(1)";
});
```

});

/* =========================================
CATEGORY FILTER DEMO
========================================= */

const categoryCards =
document.querySelectorAll(
".category-card"
);

categoryCards.forEach(card => {

```
card.addEventListener("click", () => {

    const category =
        card.innerText;

    console.log(
        "Selected Category:",
        category
    );

    /*
      Future API Request

      fetch(
        /api/products?category=
      )

    */
});
```

});

/* =========================================
NEWSLETTER SUBMIT
========================================= */

const newsletterForm =
document.querySelector(
".newsletter form"
);

if(newsletterForm){

```
newsletterForm.addEventListener(
    "submit",
    function(e){

        e.preventDefault();

        alert(
            "Thank you for subscribing!"
        );

        this.reset();
    }
);
```

}

/* =========================================
PRODUCT CONTACT REQUEST
========================================= */

const requestButtons =
document.querySelectorAll(
".product-info button"
);

requestButtons.forEach(button => {

```
button.addEventListener(
    "click",
    () => {

        alert(
            "Contact request sent successfully."
        );

        /*
         Future API

         POST
         /api/contact-request
        */
    }
);
```

});

/* =========================================
SCROLL TO TOP
========================================= */

const scrollBtn =
document.createElement("button");

scrollBtn.innerHTML =
'<i class="fa-solid fa-arrow-up"></i>';

scrollBtn.id =
"scrollTopBtn";

document.body.appendChild(
scrollBtn
);

window.addEventListener(
"scroll",
() => {

```
    if (
        window.scrollY > 500
    ) {

        scrollBtn.style.display =
            "block";

    } else {

        scrollBtn.style.display =
            "none";
    }
}

);

scrollBtn.addEventListener(
"click",
() => {

```
    window.scrollTo({

        top:0,

        behavior:"smooth"
    });
}

);
