async function api(path, method="GET", body=null) {
  const opts = { method, headers: {} };
  if (body) {
    opts.headers["Content-Type"] = "application/json";
    opts.body = JSON.stringify(body);
  }
  const res = await fetch(path, opts);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status} ${text}`);
  }
  return res.json();
}

async function loadBooks(forceAll=false) {
  const q = document.getElementById("search").value.trim();
  const url = q && !forceAll ? `/api/books?search=${encodeURIComponent(q)}` : "/api/books";
  try {
    const books = await api(url);
    const tbody = document.querySelector("#booksTable tbody");
    tbody.innerHTML = "";
    for (const b of books) {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${b.id}</td>
        <td>${escapeHtml(b.title)}</td>
        <td>${escapeHtml(b.author)}</td>
        <td>${b.year || ""}</td>
        <td>${b.isbn || ""}</td>
        <td>${b.available ? "是" : "否"}</td>
        <td>
          <button onclick="toggleAvailable(${b.id},${b.available})">${b.available ? "借出" : "归还"}</button>
          <button onclick="removeBook(${b.id})">删除</button>
        </td>
      `;
      tbody.appendChild(tr);
    }
  } catch (err) {
    alert("加载失败: " + err);
  }
}

function escapeHtml(s) {
  if (!s) return "";
  return s.replace(/[&<>"]'/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;','"':"&#39;"}[c]));
}

async function addBook() {
  const title = document.getElementById("title").value.trim();
  const author = document.getElementById("author").value.trim();
  const year = parseInt(document.getElementById("year").value) || null;
  const isbn = document.getElementById("isbn").value.trim() || null;
  if (!title || !author) {
    alert("书名和作者为必填");
    return;
  }
  try {
    await api("/api/books", "POST", { title, author, year, isbn });
    document.getElementById("title").value = "";
    document.getElementById("author").value = "";
    document.getElementById("year").value = "";
    document.getElementById("isbn").value = "";
    loadBooks(true);
  } catch (err) {
    alert("添加失败: " + err);
  }
}

async function toggleAvailable(id, current) {
  try {
    await api(`/api/books/${id}`, "PUT", { available: !current });
    loadBooks(true);
  } catch (err) {
    alert("操作失败: " + err);
  }
}

async function removeBook(id) {
  if (!confirm("确认删除该图书？")) return;
  try {
    await api(`/api/books/${id}`, "DELETE");
    loadBooks(true);
  } catch (err) {
    alert("删除失败: " + err);
  }
}

window.onload = () => loadBooks(true);
