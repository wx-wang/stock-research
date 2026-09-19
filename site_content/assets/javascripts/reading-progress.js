document$.subscribe(() => {
  let progress = document.querySelector(".reading-progress");
  if (!progress) {
    progress = document.createElement("div");
    progress.className = "reading-progress";
    progress.setAttribute("aria-hidden", "true");
    document.body.appendChild(progress);
  }

  const update = () => {
    const root = document.documentElement;
    const distance = root.scrollHeight - root.clientHeight;
    const ratio = distance > 0 ? Math.min(root.scrollTop / distance, 1) : 0;
    progress.style.transform = `scaleX(${ratio})`;
  };

  update();
  document.addEventListener("scroll", update, { passive: true });
  window.addEventListener("resize", update, { passive: true });
});
