document.addEventListener("DOMContentLoaded", () => {
    const dialog = document.getElementById("delete-dialog");
    const message = document.getElementById("delete-message");

    document.querySelectorAll("[data-delete-url]").forEach((button) => {
        button.addEventListener("click", () => {
            const form = dialog.querySelector("form");
            form.action = button.dataset.deleteUrl;
            message.textContent = `Вы уверены, что хотите удалить книгу ${button.dataset.bookTitle}?`;
            dialog.showModal();
        });
    });

    document.querySelectorAll("[data-open-dialog]").forEach((button) => {
        button.addEventListener("click", () => {
            document.getElementById(button.dataset.openDialog)?.showModal();
        });
    });

    const addToCollectionForm = document.getElementById("add-to-collection-form");
    const collectionSelect = document.querySelector("[data-collection-action-template]");
    if (addToCollectionForm && collectionSelect) {
        const updateAction = () => {
            addToCollectionForm.action = collectionSelect.dataset.collectionActionTemplate.replace(
                "/0/",
                `/${collectionSelect.value}/`
            );
        };
        updateAction();
        collectionSelect.addEventListener("change", updateAction);
    }

    document.querySelectorAll("[data-close-dialog]").forEach((button) => {
        button.addEventListener("click", () => button.closest("dialog")?.close());
    });
});
