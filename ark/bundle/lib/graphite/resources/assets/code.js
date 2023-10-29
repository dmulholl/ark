// Add a copy button to <pre> tags unless they have a 'no-copy' class.
document.addEventListener("DOMContentLoaded", function() {
    if (!navigator.clipboard) {
        return;
    }

    document.querySelectorAll("pre").forEach(node => {
        if (node.classList.contains("no-copy")) {
            return;
        }

        var wrapper = document.createElement('div');
        wrapper.classList.add("pre-copy-wrapper");
        node.parentNode.insertBefore(wrapper, node);
        wrapper.appendChild(node);

        let copyBtn = document.createElement("button");
        copyBtn.innerText = "[COPY]";
        wrapper.appendChild(copyBtn);

        copyBtn.addEventListener("click", async () => {
            let text = node.innerText;
            await navigator.clipboard.writeText(text);
            copyBtn.innerText = "[COPIED]";
            setTimeout(() => copyBtn.innerText = "[COPY]", 1000);
        })
    })
});
