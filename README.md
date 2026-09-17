專案名稱：Real-Time Clickstream ELT Pipeline
基於 Docker 構建的即時電商點擊流分析平台。資料由 Python 模擬器生成，經由 Redpanda（Kafka）串流隊列，透過 Materialized View 自動同步入 ClickHouse 列式資料庫，並在 Grafana 實現即時儀表板監控與動態維度過濾。

系統架構 (Architecture)
Plaintext
[ Python Producer ]
        │ (JSON Events)
        ▼
[ Redpanda (Kafka API) ]
        │ (Topic: clickstream_events)
        ▼
  ├── clickstream_kafka            (Kafka Engine 表，負責拉取隊列資料)
  │     │
  │     ▼ (透過第一層物化視圖自動轉移)
  ├── clickstream_mv               (Materialized View 1: 寫入原始明細)
  │     │
  │     ▼
  ├── clickstream_records          (MergeTree 實體表: 儲存所有原始事件明細)
  │     │
  │     ▼ (透過第二層物化視圖即時聚合)
  ├── clickstream_minute_mv        (Materialized View 2: 分鐘級聚合輸送帶)
  │     │
  │     ▼
  └── clickstream_minute_summary  (SummingMergeTree 實體表: 分鐘維度預聚合統計)
        │ (HTTP 8123)
        ▼
[ Grafana Dashboard ] (即時圖表 & 篩選器)
技術棧 (Tech Stack)
訊息隊列：Redpanda (相容 Kafka API)

列式資料庫：ClickHouse

視覺化：Grafana (含 ClickHouse 官方外掛)

資料產生器：Python 3 (相容套件 kafka-python / kafka-python-ng)

容器編排：Docker Compose

快速開始 (Quick Start)
1. 前置需求 (Prerequisites)
Docker & Docker Compose

Python 3.9+

2. 啟動基礎設施
複製倉庫並一鍵啟動容器（Redpanda, ClickHouse, Grafana）：

git clone https://github.com/你的帳號/你的專案.git
cd 你的專案
docker compose up -d
3. 初始化資料庫（若有獨立 SQL 腳本）
進 ClickHouse 容器建立 Kafka Engine、MergeTree 表與 Materialized View：

# 若有 init.sql 檔案，可直接執行
docker exec -i clickhouse-server clickhouse-client < init.sql
4. 啟動資料生產者 (Data Producer)
安裝相依套件並開始打入即時點擊資料：

pip install -r requirements.txt
python producer.py
儀表板檢視 (Grafana Dashboard)
URL：http://localhost:3000

帳號/密碼：admin / admin（或免密碼登入，視 compose 設定）

自動配置 (Provisioning)：

資料來源：已自動配置 ClickHouse（HTTP 協定，Port 8123）

儀表板包含：

每分鐘裝置流量折線圖（Time Series，支援 device_type 篩選）

各站點即時 PV / UV 統計（Bar Chart，支援 site_id 篩選）

購物流程轉化漏斗（Funnel / Bar Chart）

專案結構 (Directory Structure)
.
├── docker-compose.yml              # 容器編排設定
├── producer.py                     # 點擊串流模擬腳本
├── requirements.txt                # Python 套件清單
├── grafana-provisioning/
│   ├── datasources/
│   │   └── datasources.yaml       # 自動綁定 ClickHouse 資料來源 (HTTP)
│   └── dashboards/
│       ├── dashboards.yaml        # Dashboard 自動載入設定
│       └── clickstream.json       # 預設儀表板 Model
└── README.md