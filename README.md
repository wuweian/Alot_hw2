# Taiwan Weather Forecast App 🌤️

這是一個基於 Python 與 Streamlit 打造的「台灣一週農業氣溫預報 Web App」。
本專案會自動串接**中央氣象署 (CWA)** 開放資料 API (包含最新日期的實時數據)，並把數據儲存進**本地 SQLite 資料庫**中，再透過互動式動態網頁進行視覺化展示。

## 🌟 核心功能 (Features)

1. **自動化擷取 CWA 開放資料 (API)**
   - 使用 `requests` 串接 `F-A0010-001` 一週農業氣象預報 FileAPI，直接讀取官方公開的最高/最低/平均氣溫。
2. **SQLite 資料庫整合**
   - 所有的氣溫資料處理後自動存入 `weather.db` 的 `forecast` 資料表中，完全符合實作規格。
3. **雙頁籤視覺化面板 (Dual Tabs Dashboard)**
   - **🗺️ Map View (依日期檢視)**：提供日期下拉選單，並在左側動態渲染出全台六大區域 (北部、南部等...) 的 Folium 彩色互動圓點地圖，點開可看氣溫詳細 popup 資訊。
   - **📈 Trend View (依地區檢視)**：提供地區下拉選單，即時對 SQLite 下達 SQL 查詢指令 (`SELECT`) 並產出 7 天連續的氣溫折線圖 (`st.line_chart`) 與預報表格。

## 🛠️ 開發環境與套件 (Dependencies)
- **Python >= 3.9**
- `streamlit`
- `folium` AND `streamlit-folium` (地圖視覺化)
- `pandas`
- `requests`
- `sqlite3` (Python 內建)

## 🚀 如何執行 (How to run)

1. 先安裝好需要用到的套件：
   ```bash
   pip install requests pandas streamlit folium streamlit-folium
   ```
2. 執行爬蟲腳本更新最新的氣溫資料到 SQLite 資料庫 `weather.db` 中：
   ```bash
   python fetch_weather.py
   ```
3. 啟動 Streamlit 服務開啟氣象視覺化網站：
   ```bash
   streamlit run app.py
   ```
4. 開啟瀏覽器訪問預設位址 (通常為 `http://localhost:8502`) 即可操作！
