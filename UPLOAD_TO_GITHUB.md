# 用 VS Code 上傳 SalesCheck 到 GitHub

## 1. 開啟專案

1. 解壓縮 `SalesCheck.zip`。
2. 在 VS Code 選 **File → Open Folder**，開啟解壓縮後的 **SalesCheck** 資料夾。
3. 左側最上層應直接看到 `README.md`、`dist`、`python`、`examples`、`tests`。
4. 選 **Terminal → New Terminal**。Terminal 應位於這個 SalesCheck 資料夾。

## 2. 確認檔案

執行：

```sh
pwd
ls
```

確認目前資料夾是剛解壓縮的 SalesCheck，並且看得到 `README.md`。請勿在 Downloads 或其他專案的根目錄執行下列上傳指令。

## 3. 上傳到已建立的空 repo

以下指令會建立本機版本紀錄，然後將專案上傳到你的新 repo：

```sh
git init -b main
git add .
git commit -m "Build SalesCheck sales validation dashboard and Python CLI"
git remote add origin https://github.com/SasaWu0136/SalesCheck.git
git remote -v
git push -u origin main
```

`git remote -v` 應顯示 `https://github.com/SasaWu0136/SalesCheck.git`。

如果 VS Code 顯示 GitHub 登入提示，請登入擁有此 repo 的 `SasaWu0136` 帳號並完成授權。若 Terminal 要求 GitHub 密碼，請勿輸入一般帳號密碼；可改用 VS Code 的 GitHub 登入流程完成驗證。

如果出現 `Author identity unknown`，先設定你希望公開於 commit 的姓名與 email，再重新執行 `git commit`：

```sh
git config user.name "Sasa Wu"
git config user.email "你的 GitHub commit email"
```

請將 email 佔位文字換成 GitHub Settings → Emails 中的個人地址或 GitHub 提供的 noreply 地址。

如果 push 被拒絕，或提示 remote 已存在，先停下來，把完整錯誤訊息貼回對話。不要使用 `--force`，也不需要刪掉 repo。

## 4. 確認結果

打開 https://github.com/SasaWu0136/SalesCheck ，重新整理後應看到 README、dist、python、examples、tests。

## 5. 開啟網頁

用 Chrome 開啟 `dist/index.html` 即可操作，也可以在這個資料夾的 Terminal 執行：

```sh
python3 -m http.server 8000 --directory dist
```

然後開啟 http://localhost:8000 。結束時在 Terminal 按 Ctrl+C。

## 6. 執行測試（選用）

需要 Node.js 18+ 與 Python 3.10+：

```sh
node --test tests/core.test.js
python3 -m unittest discover -s tests -p 'test_*.py'
```

## 包含內容

- `dist/`：完整可操作的網頁。
- `python/`：Python 銷售核對程式與 CLI。
- `examples/`：範例 CSV。
- `tests/`：JavaScript 與 Python 測試。
- `README.md`：英文專案說明與中文快速開始。
- `.gitignore`：排除快取與本機輸出。

ZIP 不含舊 Git 紀錄、發布設定或登入憑證。上傳這個新 repo 不會更動原本的兩個 Python repo。GitHub 上傳原始碼完成後，網站尚未自動上線；線上 demo 需要另外部署。
