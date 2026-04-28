# AIoT HW2 - AI 對話紀錄與專案開發過程

這份文件記錄了使用 AI 助理一步步開發「台灣一週氣溫預報 Web App」完整的對話與實作流程。

## 階段一：專案建立與網頁架構
**User 需求：**
> 建立一個完整的 Python 專案，讀取 CWA API 抓取台灣七天的預報資料（北部、中部、南部、東北部、東部、東南部）。將資料轉為 `weather_data.csv`，並使用 Streamlit 和 Folium 製作一個包含左右排版 Web App，左邊是台灣彩色地圖氣候圓點，右邊是表格，並可以透過下拉選單選擇日期。

**AI 助理行動：**
1. 建立虛擬環境 (`venv`) 並安裝 `requests`, `pandas`, `streamlit`, `folium`, `streamlit-folium` 等必要套件。
2. 撰寫 `fetch_weather.py` 處理天氣資料的爬取與 JSON 解析，並過濾掉憑證錯誤機制。
3. 撰寫了 `app.py` 搭建出基礎的地圖 (Map View) 面板，左側支援 Folium 互動圓點（藍、綠、黃、紅），右側放置預報表格。
4. 提供模擬數據集驗證 Streamlit 排版成功無誤。

---

## 階段二：導入 SQLite 資料庫與折線圖面板
**User 需求：**
> 目的：製作氣溫預報視覺化。必須從 SQLite3 資料庫查詢資料、提供下拉選單選擇「地區」、使用折線圖與表格來顯示一週氣溫資料。

**AI 助理行動：**
1. 將原本的 CSV 流程雙軌化，指令呼叫 `pandas.to_sql()` 把天氣資料自動建置為 `weather.db`。
2. 徹底升級 `app.py` 的排版，導入 Streamlit 內建的雙頁籤 (`st.tabs`)：
   - **Tab 1: 🗺️ Map View** (以日期篩選)。
   - **Tab 2: 📈 Trend View** (以特定地區篩選，完全滿足此次新需求)。
3. Tab 2 完全透過 `sqlite3` 直連 `weather.db` 撈取資料，並以 `st.line_chart` 畫出最高低與平均溫度的趨勢折線。

---

## 階段三：修正資料筆數與同步最新真實預報
**User 需求：**
> 原本測試假資料只有兩天，希望變成完整 5/1~5/7 的數據。後來使用者進一步指正，希望套用 CWA API `F-A0010-001` 開放資料網址上即日起（4/28起）真正的一週預報氣溫，不能用假造的溫度。

**AI 助理行動：**
1. 發現該 CWA 開放資料網站支援 FileAPI 以及公用授權碼 `rdec-key-123-45678-011121314`。
2. 全面改寫了 `fetch_weather.py` 的爬蟲解析邏輯，改成正確精準讀取 `cwaopendata` 結構內 `weatherElements` 的真實 `MaxT` 和 `MinT` 數據陣列。
3. 在背景自動幫 User 爬取了即日（4/28）起真正的一週氣溫並直接刷新了 `weather.db` SQLite 資料庫。
4. 針對 Streamlit 的快取問題，拔除了 `@st.cache_data` 的機制，保證每次網頁重整、切換地區，都會撈到最熱騰騰即時的 SQLite 資料庫回傳數據。

---

## 階段四：專案發佈與轉移
**User 需求：**
> 將所有更新檔案推送到 GitHub `https://github.com/wuweian/Alot_hw2.git`，並且另外複製到本機的桌面 `C:\Users\weian\OneDrive\桌面\hw2` 資料夾。

**AI 助理行動：**
1. 配置好乾淨的 `.gitignore` (排除 `venv` 等大型無用快取)。
2. 進行 `git init`, `git commit` 以及強制推送成功至你的遠端 GitHub 倉儲。
3. 使用指令透過 `robocopy` 無痛且乾淨地轉移了所有核心程式碼跟資料庫檔案至你桌面的 `hw2` 目錄中，完成全數作業建置！
