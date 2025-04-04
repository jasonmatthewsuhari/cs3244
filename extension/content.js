const delayUntilReady = setInterval(() => {
    const messageElems = document.querySelectorAll("div[data-id] span.selectable-text");
  
    if (messageElems.length > 0) {
      clearInterval(delayUntilReady);
  
      messageElems.forEach(elem => {
        elem.addEventListener("mouseenter", () => {
          console.log("💬 Message hovered:", elem.innerText);
        });
      });

      console.log("🟢 Hover logger initialized.");
    }
  }, 1000);
  
console.log("🟢 Content script loaded.");

function overwriteSuggestedEmojis(emojis) {
    const emojiContainers = Array.from(document.querySelectorAll('div[style^="left:"]'))
      .filter(div => div.querySelector('div[role="button"]'));
  
    if (emojiContainers.length === 0) {
      console.warn("Why are there no emoji containers?");
      return;
    }
  
    for (let i = 0; i < Math.min(6, emojiContainers.length); i++) {
      const wrapper = emojiContainers[i];
      const button = wrapper.querySelector('div[role="button"]');
  
      if (!button || button.dataset.replaced === "true") continue;

      const img = button.querySelector("img");
      if (img) img.remove();
  
      const emojiDiv = document.createElement("div");
      emojiDiv.innerText = emojis[i] || "💥";
      emojiDiv.style.cssText = `
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
      `;
  
      button.appendChild(emojiDiv);
      button.dataset.replaced = "true";
    }
  
    console.log("✅ Custom emojis injected into WhatsApp bubbles.");
}  

const observer = new MutationObserver((mutations) => {
for (const mutation of mutations) {
    mutation.addedNodes.forEach(node => {
    if (node.nodeType === 1 && node.querySelector('[aria-label="More reactions"]')) {
        overwriteSuggestedEmojis(["💩", "💩", "💩", "💩", "💩", "💩"]);
    }
    });
}
});

observer.observe(document.body, {
childList: true,
subtree: true
});
