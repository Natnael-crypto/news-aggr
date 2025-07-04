document.addEventListener("DOMContentLoaded", function () {
  const loadBtn = document.getElementById("load-more");
  const newsList = document.getElementById("news-list");
  let currentPage = 1;
  let currentSource = null;

  document.querySelectorAll(".filter-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      currentSource = btn.dataset.source;
      currentPage = 1;
      newsList.innerHTML = "";
      fetchNews();
    });
  });

  loadBtn.addEventListener("click", () => {
    currentPage++;
    fetchNews();
  });

  function fetchNews() {
    fetch(`/load_news?page=${currentPage}&source=${currentSource || ""}`)
      .then(res => res.text())
      .then(html => {
        newsList.insertAdjacentHTML("beforeend", html);
      });
  }
});
