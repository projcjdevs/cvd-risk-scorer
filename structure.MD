cvd-risk-scorer/
│
├── app/
│   ├── scorer.py        ← Layer 1: the Globorisk math
│   ├── mapper.py        ← Layer 2: PhilPEN action logic
│   └── api.py           ← Layer 3: FastAPI (Day 2)
│
├── tests/
│   └── test_scorer.py   ← manual tests 
│
├── requirements.txt
└── README.md