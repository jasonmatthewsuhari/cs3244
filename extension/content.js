console.log("🟢 Content script loaded.");

const predictionCache = new Map();  // Cache: message text → predicted emoji

const delayUntilReady = setInterval(() => {
  const messageElems = document.querySelectorAll("div[data-id] span.selectable-text");

  if (messageElems.length > 0) {
    clearInterval(delayUntilReady);

    messageElems.forEach(elem => {
      elem.addEventListener("mouseenter", async () => {
        const text = elem.innerText;
        console.log("💬 Message hovered:", text);

        if (predictionCache.has(text)) {
          const cachedEmoji = predictionCache.get(text);
          console.log("⚡ Using cached emoji:", cachedEmoji);
          overwriteSuggestedEmojis([cachedEmoji, cachedEmoji, cachedEmoji, cachedEmoji, cachedEmoji, cachedEmoji]);
          return;
        }

        try {
          const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({ text })
          });

          const data = await response.json();
          const emoji = data.emoji;
          predictionCache.set(text, emoji);

          console.log("🎯 Predicted emoji:", emoji);
          overwriteSuggestedEmojis([emoji, emoji, emoji, emoji, emoji, emoji]);
        } catch (err) {
          console.error("❌ Failed to fetch emoji prediction:", err);
        }
      });
    });

    console.log("🟢 Hover logger initialized.");
  }
}, 1000);

function overwriteSuggestedEmojis(emojis) {
  const emojiContainers = Array.from(document.querySelectorAll('div[style^="left:"]'))
    .filter(div => div.querySelector('div[role="button"]'));

  if (emojiContainers.length === 0) {
    console.warn("⚠️ No emoji containers found.");
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

  console.log("✅ Custom emojis injected.");
}

const observer = new MutationObserver((mutations) => {
  for (const mutation of mutations) {
    mutation.addedNodes.forEach(async (node) => {
      if (node.nodeType === 1 && node.querySelector('[aria-label="More reactions"]')) {
        const messageNode = node.closest("div[role='row']")?.querySelector("span.selectable-text");
        const text = messageNode?.innerText;

        if (!text) return;

        if (predictionCache.has(text)) {
          const emoji = predictionCache.get(text);
          console.log("🧠 Observer using cached emoji:", emoji);
          setTimeout(() => {
            overwriteSuggestedEmojis([emoji, emoji, emoji, emoji, emoji, emoji]);
          }, 500);
          return;
        }

        try {
          const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text }),
          });

          const data = await response.json();
          const emoji = data.emoji;
          predictionCache.set(text, emoji);

          console.log("🎯 Observer predicted emoji:", emoji);
          setTimeout(() => {
            overwriteSuggestedEmojis([emoji, emoji, emoji, emoji, emoji, emoji]);
          }, 500);
        } catch (err) {
          console.error("❌ Observer prediction failed:", err);
        }
      }
    });
  }
});

observer.observe(document.body, {
  childList: true,
  subtree: true
});
