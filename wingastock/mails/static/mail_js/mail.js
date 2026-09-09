(function () {
    "use strict";

    function byId(id) {
        return document.getElementById(id);
    }

    function setPanelState(open) {
        const panel = byId("left-holder-101");
        const content = byId("right-holder-101");
        if (!panel || !content) return;
        panel.classList.toggle("is-open", open);
        content.classList.toggle("panel-open", open);
        document.body.classList.toggle("mail-drawer-open", open);
    }

    window.toggleLeftPanel = function () {
        const panel = byId("left-holder-101");
        setPanelState(!panel || !panel.classList.contains("is-open"));
    };

    window.closeMailPanel = function () {
        setPanelState(false);
    };

    window.open_chart = function (link) {
        const modal = byId("choose-modal");
        if (modal) modal.classList.remove("is-visible");
        window.location.href = link;
    };

    document.addEventListener("DOMContentLoaded", function () {
        const loader = byId("page-loader");
        if (loader) {
            loader.classList.add("hidden");
            window.setTimeout(function () { loader.remove(); }, 400);
        }

        document.querySelectorAll(".choose-receiver-holder-102").forEach(function (modal) {
            modal.addEventListener("click", function (event) {
                if (event.target === modal) modal.classList.remove("is-visible");
            });
        });

        document.querySelectorAll(".mail-list-103").forEach(function (list) {
            list.scrollTop = list.scrollHeight;
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                setPanelState(false);
                document.querySelectorAll(".choose-receiver-holder-102.is-visible").forEach(function (modal) {
                    modal.classList.remove("is-visible");
                });
            }
        });

        document.querySelectorAll("textarea[name='message']").forEach(function (textarea) {
            textarea.addEventListener("keydown", function (event) {
                if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
                    const form = textarea.closest("form");
                    if (form) form.requestSubmit();
                }
            });
        });
    });
}());
