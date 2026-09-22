const optionsButton =
    document.getElementById("searchOptionsButton");

const optionsDropdown =
    document.getElementById("searchOptionsDropdown");



/* =================================================
   SEARCH OPTIONS
================================================== */

if (optionsButton && optionsDropdown) {

    optionsButton.addEventListener(
        "click",
        function (event) {

            event.stopPropagation();

            optionsDropdown.classList.toggle("show");

        }
    );


    document.addEventListener(
        "click",
        function () {

            optionsDropdown.classList.remove("show");

        }
    );


    optionsDropdown.addEventListener(
        "click",
        function (event) {

            event.stopPropagation();

        }
    );

}



document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.getElementById("searchInput");
    const searchForm = document.getElementById("searchForm");
    const clearSearch = document.getElementById("clearSearch");
    const searchWrapper = document.getElementById("searchBoxWrapper");
    const dropdown = document.getElementById("liveSearchDropdown");

    if (
        !searchInput ||
        !searchForm ||
        !searchWrapper ||
        !dropdown
    ) {
        console.error("Live search elements not found.");
        return;
    }

    const searchUrl = searchWrapper.dataset.searchUrl;

    let searchTimer = null;
    let controller = null;


    /* =====================================================
       ESCAPE HTML
    ===================================================== */

    function escapeHtml(value) {

        if (value === null || value === undefined) {
            return "";
        }

        return String(value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }


    /* =====================================================
       FORMAT PRICE
    ===================================================== */

    function formatPrice(price) {

        const number = Number(price);

        if (Number.isNaN(number)) {
            return price;
        }

        return new Intl.NumberFormat("en-TZ").format(number);
    }


    /* =====================================================
       SHOW DROPDOWN
    ===================================================== */

    function showDropdown() {

        dropdown.classList.add("show");
        dropdown.setAttribute("aria-hidden", "false");

    }


    /* =====================================================
       HIDE DROPDOWN
    ===================================================== */

    function hideDropdown() {

        dropdown.classList.remove("show");
        dropdown.setAttribute("aria-hidden", "true");

    }


    /* =====================================================
       LOADING
    ===================================================== */

    function showLoading() {

        dropdown.innerHTML = `
            <div class="live-search-loading">
                <i class="fas fa-spinner fa-spin"></i>
                <span>Searching...</span>
            </div>
        `;

        showDropdown();
    }


    /* =====================================================
       NO RESULTS
    ===================================================== */

    function showNoResults(query) {

        dropdown.innerHTML = `
            <div class="live-search-empty">

                <div class="live-search-empty-icon">
                    <i class="fas fa-search"></i>
                </div>

                <strong>
                    No products found
                </strong>

                <span>
                    No results for "${escapeHtml(query)}"
                </span>

            </div>
        `;

        showDropdown();
    }


    /* =====================================================
       RENDER RESULTS
    ===================================================== */

    function renderResults(results, query) {

        if (!results || results.length === 0) {

            showNoResults(query);

            return;
        }


        let html = "";


        results.forEach(function (product) {

            const image = product.image
                ? `
                    <img
                        src="${escapeHtml(product.image)}"
                        alt="${escapeHtml(product.title)}"
                    >
                  `
                : `
                    <div class="live-search-image-placeholder">
                        <i class="fas fa-image"></i>
                    </div>
                  `;


            html += `
                <button
                    type="button"
                    class="live-search-result"
                    data-url="${escapeHtml(product.url)}"
                >

                    <div class="live-search-result-image">
                        ${image}
                    </div>


                    <div class="live-search-result-content">

                        <div class="live-search-result-title">
                            ${escapeHtml(product.title)}
                        </div>


                        <div class="live-search-result-description">
                            ${escapeHtml(product.description || "")}
                        </div>


                        <div class="live-search-result-meta">

                            <span class="live-search-result-price">
                                TSh ${formatPrice(product.price)}
                            </span>


                            <span class="live-search-result-category">
                                ${escapeHtml(product.category || "")}
                            </span>

                        </div>


                    </div>


                    <div class="live-search-result-arrow">

                        <i class="fas fa-chevron-right"></i>

                    </div>

                </button>
            `;
        });


        html += `
            <button
                type="button"
                class="live-search-view-all"
                id="liveSearchViewAll"
            >
                <span>
                    View all results for
                    "<strong>${escapeHtml(query)}</strong>"
                </span>

                <i class="fas fa-arrow-right"></i>
            </button>
        `;


        dropdown.innerHTML = html;

        showDropdown();


        /* =================================================
           RESULT CLICK
        ================================================== */

        const resultButtons =
            dropdown.querySelectorAll(".live-search-result");


        resultButtons.forEach(function (button) {

            button.addEventListener("click", function () {

                const url = this.dataset.url;

                if (url) {
                    window.location.href = url;
                }

            });

        });


        /* =================================================
           VIEW ALL
        ================================================== */

        const viewAll =
            document.getElementById("liveSearchViewAll");


        if (viewAll) {

            viewAll.addEventListener("click", function () {

                searchForm.submit();

            });

        }

    }


    /* =====================================================
       FETCH SEARCH
    ===================================================== */

    async function performSearch(query) {

        if (!query) {

            hideDropdown();

            return;
        }


        if (controller) {
            controller.abort();
        }


        controller = new AbortController();


        showLoading();


        try {

            const url =
                searchUrl +
                "?search=" +
                encodeURIComponent(query);


            const response = await fetch(url, {

                method: "GET",

                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "Accept": "application/json"
                },

                signal: controller.signal

            });


            if (!response.ok) {

                throw new Error(
                    "Search request failed: " +
                    response.status
                );

            }


            const data = await response.json();


            renderResults(
                data.results || [],
                query
            );


        } catch (error) {

            if (error.name === "AbortError") {
                return;
            }


            console.error(
                "Live search error:",
                error
            );


            dropdown.innerHTML = `
                <div class="live-search-error">

                    <i class="fas fa-exclamation-circle"></i>

                    <span>
                        Unable to search right now.
                    </span>

                </div>
            `;

            showDropdown();

        }

    }


    /* =====================================================
       INPUT
    ===================================================== */

    searchInput.addEventListener("input", function () {

        const query = this.value.trim();


        clearTimeout(searchTimer);


        if (!query) {

            hideDropdown();

            return;
        }


        searchTimer = setTimeout(function () {

            performSearch(query);

        }, 250);

    });


    /* =====================================================
       CLEAR BUTTON
    ===================================================== */

    if (clearSearch) {

        clearSearch.addEventListener("click", function () {

            searchInput.value = "";

            hideDropdown();

            searchInput.focus();

        });

    }


    /* =====================================================
       FORM SUBMIT
    ===================================================== */

    searchForm.addEventListener("submit", function () {

        const query = searchInput.value.trim();

        if (!query) {
            return;
        }

    });


    /* =====================================================
       CLICK OUTSIDE
    ===================================================== */

    document.addEventListener("click", function (event) {

        if (!searchWrapper.contains(event.target)) {

            hideDropdown();

        }

    });


    /* =====================================================
       ESCAPE KEY
    ===================================================== */

    document.addEventListener("keydown", function (event) {

        if (event.key === "Escape") {

            hideDropdown();

            searchInput.blur();

        }

    });

});