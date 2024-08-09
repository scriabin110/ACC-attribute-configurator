# 環境構築

- pythonをインストールしておく

  - Windows版：https://www.python.jp/install/windows/install.html

- 仮想環境の作成
```
python -m venv .venv
```

## 仮想環境の使い分け

- venvを利用

### Windowsの場合

- pipコマンドがバグるときは "python -m" を冒頭につけると動きそう(適当)

```text
# windows版仮想環境に入る
###VScodeのターミナルで下記を入力
.\\.venv\Scripts\activate  

# 必要パッケージの一括読み込み
python -m pip install -r requirements.txt

# 新規ライブラリ(パッケージ)のinstall
python -m pip install (インストールしたいパッケージ名)

# requirements.txtの上書き方法
python -m pip freeze > requirements.txt
```


# ACC ID info

```text
Hub ID: b.21cd4449-77cc-4f14-8dd8-597a5dfef551, Name: JGC GLOBAL ESC
  Project ID: b.01d565fa-872c-4f6b-95ae-ea8cbca344fc, Name: 7-0627_JGC Group Standard Establishment
  Project ID: b.07056904-2be0-4aff-8aea-33afc5a7d4c8, Name: 701211-00_JGC BIM STANDARD
  Project ID: b.0a76f787-f252-41e8-beaa-0479b4ab8bc3, Name: 6-4512_Live Link-Execution Template
  Project ID: b.1f56cb42-81af-466e-8e26-2ea3c7edfda9, Name: 6-4512_BIM Training4
  Project ID: b.1fd68d4e-de62-4bc3-a909-8b0baeec77e4, Name: 6-4512_BIM Training 2
  Project ID: b.74d0a9fe-dbcc-4aed-be6b-dbd118667cda, Name: 5-0682_Tangguh UCC

フォルダ構造:
└── Project Files (ID: urn:adsk.wipprod:fs.folder:co.JDMH-cFiRt2HRhozmFRBSQ)
    ├── 10-WIP (ID: urn:adsk.wipprod:fs.folder:co.3qEvGkvlScqvlGRoUVlVGw)
    │   ├── WIP01_ARC (ID: urn:adsk.wipprod:fs.folder:co.-QYupPdGRCCJE2yNSJ0xFA)
    │   │   ├── Consumed (ID: urn:adsk.wipprod:fs.folder:co.rB0SxpXoTcKdEGMq1v66Rg)
    │   │   ├── WIP-A1_3D (Master) (ID: urn:adsk.wipprod:fs.folder:co.Xkq1sj8VRymnNP97cMMxUQ)
    │   │   │   ├── ARC_Consumed (ID: urn:adsk.wipprod:fs.folder:co.yMET-9MiQfGqoJfuXO3LVg)
    │   │   │   └── Unknown File (ID: urn:adsk.wipprod:dm.lineage:qVjCg6dtS6qmBjGno_XVtg)
    │   │   ├── WIP-A2_2D (ID: urn:adsk.wipprod:fs.folder:co.IVzf3xTDQFOk-1RTdpOt_Q)
    │   │   │   └── Unknown File (ID: urn:adsk.wipprod:dm.lineage:Swd_gVFqTMO7eBUtRzuNXQ)
    │   │   ├── WIP-A3_Other (ID: urn:adsk.wipprod:fs.folder:co.T6NqPtzyTheM3i6IiTzyvA)
    │   │   └── WIP-A4_Reference (ID: urn:adsk.wipprod:fs.folder:co.cXRZryclTJ2XOxX1dHkKIw)
    │   ├── WIP02_STR (ID: urn:adsk.wipprod:fs.folder:co.CQQr7kk2Q1meCvyCWkn4ZA)
    │   │   ├── Consumed (ID: urn:adsk.wipprod:fs.folder:co.Ys0KpUOdQcGeAe-OqK6g8A)
    │   │   ├── WIP-S1_3D (Master) (ID: urn:adsk.wipprod:fs.folder:co.1MMPcKRDSzewgULQvECdKw)
    │   │   │   ├── 02-STR_Consumed (ID: urn:adsk.wipprod:fs.folder:co.MIf4MbOzRj6tH2G56WkBlA)
    │   │   │   └── Unknown File (ID: urn:adsk.wipprod:dm.lineage:Q-TJ1WhRSqSVojqTk_xe6g)
    │   │   ├── WIP-S2_2D (ID: urn:adsk.wipprod:fs.folder:co.UZ9-0f5STyqyO1VZT0bPVQ)
    │   │   ├── WIP-S3_Other (ID: urn:adsk.wipprod:fs.folder:co.QCAVBpVaSBOtr3dPhG2K0A)
    │   │   └── WIP-S4_Reference (ID: urn:adsk.wipprod:fs.folder:co.4WqOL6spSCWPJWF0Db0y4A)
    │   ├── WIP03_HVAC (ID: urn:adsk.wipprod:fs.folder:co.S64O0cd6T5e_xPYA16SVxw)
    │   │   ├── Consumed (ID: urn:adsk.wipprod:fs.folder:co.N9zrYWCDRs2TiiPwQa-UmQ)
    │   │   ├── WIP-H1_3D (Master) (ID: urn:adsk.wipprod:fs.folder:co.cgIvkoaiSd-qXTmwpnYqvg)
    │   │   │   └── HVAC_Consumed (ID: urn:adsk.wipprod:fs.folder:co.nozw8CFqTWS_J74DkYNHhA)
    │   │   ├── WIP-H2_2D (ID: urn:adsk.wipprod:fs.folder:co.Uqk4R4PSSNGkt4AHSSMXCQ)
    │   │   ├── WIP-H3_Other (ID: urn:adsk.wipprod:fs.folder:co.1q72-uYMT7yc3ARCl9FXBg)
    │   │   └── WIP-H4_Reference (ID: urn:adsk.wipprod:fs.folder:co.lxcnHEYTQ_O17UUrmg-WOA)
    │   ├── WIP04_PLB (ID: urn:adsk.wipprod:fs.folder:co.Urho8YR0SdiPeduJ-Bsf9w)
    │   │   ├── Consumed (ID: urn:adsk.wipprod:fs.folder:co.whw4-natRBWRpVRS9cVQ6w)
    │   │   ├── WIP-P1_3D (Master) (ID: urn:adsk.wipprod:fs.folder:co.ymx6nNonRCWq4JCWJutU6g)
    │   │   │   └── 04-PLB_Consumed (ID: urn:adsk.wipprod:fs.folder:co.ge8FP3HZT4OU2y_GQRGvQQ)
    │   │   ├── WIP-P2_2D (ID: urn:adsk.wipprod:fs.folder:co.ArCNn0j2S_-uY7Z_5X9bGg)
    │   │   ├── WIP-P3_Other (ID: urn:adsk.wipprod:fs.folder:co.QWOovwwmQvSn5TAmEFqwdA)
    │   │   └── WIP-P4_Reference (ID: urn:adsk.wipprod:fs.folder:co.Odq_tCDvTu2H5hfqRad4og)
    │   ├── WIP05_ELC (ID: urn:adsk.wipprod:fs.folder:co.K3u-4ZsXQqC2_oJOxCGfaw)
    │   │   ├── Consumed (ID: urn:adsk.wipprod:fs.folder:co.ezJIaDfgTPyxv3xs_zI45Q)
    │   │   ├── WIP-E1_3D (Master) (ID: urn:adsk.wipprod:fs.folder:co.YPcWrEM2SDCA2YHqqDyP5g)
    │   │   │   └── ELC_Consumed (ID: urn:adsk.wipprod:fs.folder:co.c9qYLlJxTyafLOxlifeawA)
    │   │   ├── WIP-E2_2D (ID: urn:adsk.wipprod:fs.folder:co.7GbHxn4mQQKQZhHQCOKXeg)
    │   │   ├── WIP-E3_Other (ID: urn:adsk.wipprod:fs.folder:co.xnSaNrrnQeqU7gjC2J_4Gg)
    │   │   └── WIP-E4_Reference (ID: urn:adsk.wipprod:fs.folder:co.ecnonwtuR-Onc2x3qw6T9g)
    │   └── WIP06_FIRE (ID: urn:adsk.wipprod:fs.folder:co.R7LcjwNXRSqyzWBHEoyxyQ)
    │       ├── Consumed (ID: urn:adsk.wipprod:fs.folder:co.3QaIDKR6Q8WpfkfeCfUeQw)
    │       ├── WIP-F1_3D (Master) (ID: urn:adsk.wipprod:fs.folder:co.JoGnEjRYRbaW0yZLqbdynw)
    │       │   └── 06-FIRE_Consumed (ID: urn:adsk.wipprod:fs.folder:co.LKDOJ787TAC0g01aEm4RUQ)
    │       ├── WIP-F2_2D (ID: urn:adsk.wipprod:fs.folder:co.T80glLpTR96WrHSFhmWpow)
    │       ├── WIP-F3_Other (ID: urn:adsk.wipprod:fs.folder:co.ix4MqOBsRsKmDWZHXsTg-g)
    │       └── WIP-F4_Reference (ID: urn:adsk.wipprod:fs.folder:co.rb0Jq3PDSWK_P4WhWeg6Ew)
    ├── 20-Shared (ID: urn:adsk.wipprod:fs.folder:co.3M5T6zWyRaaABgzWmzTKxg)
    │   ├── 20-Shared-00_Coordination Review (ID: urn:adsk.wipprod:fs.folder:co.LVg3hJGcSOSBJw06jQzR7Q)
    │   │   ├── SH00_Clash Check Report (ID: urn:adsk.wipprod:fs.folder:co.v_4IongsSUC6uYKZNoniKA)
    │   │   ├── SH01_ARC (ID: urn:adsk.wipprod:fs.folder:co.CRZ1Kz2OSXC7Xl-2mU0iKQ)
    │   │   ├── SH02_STR (ID: urn:adsk.wipprod:fs.folder:co.gyTD0GBPRdGkNBgqEUy8yA)
    │   │   ├── SH03_HVAC (ID: urn:adsk.wipprod:fs.folder:co.XeIYwrSAQFuvK1Kuw52ByA)
    │   │   ├── SH04_PLB (ID: urn:adsk.wipprod:fs.folder:co.7ZgdwnKzTnao_IF_EZ3Yjw)
    │   │   ├── SH05_ELC (ID: urn:adsk.wipprod:fs.folder:co.i2_NrAD_T2OmGYt8e1FT8A)
    │   │   └── SH06_FIRE (ID: urn:adsk.wipprod:fs.folder:co.qmkQjwRESia8OfBgYoeFoA)
    │   └── 20-Shared-01_Milestones Review (ID: urn:adsk.wipprod:fs.folder:co.6dXaYGQWTdGZd13ErYRong)
    │       ├── M1_xxxxx(Milestone Name) (ID: urn:adsk.wipprod:fs.folder:co.rMea1MinQCq6aA6b2bCz8g)
    │       │   ├── M1-01-3D (ID: urn:adsk.wipprod:fs.folder:co.bM9ToYQgT1WLqNQmTGnl2A)
    │       │   ├── M1-02-2D (ID: urn:adsk.wipprod:fs.folder:co.Qh1vZB7tT2WsRrFNAe0oxg)
    │       │   │   └── Unknown File (ID: urn:adsk.wipprod:dm.lineage:6yXorb0cRSGr_QCxJAOQFw)
    │       │   ├── M1-03-J-DMS (if any) (ID: urn:adsk.wipprod:fs.folder:co.WgMFIZhiSri8vhwglEsb_g)
    │       │   ├── M1-04-Other (ID: urn:adsk.wipprod:fs.folder:co.s4D_ErRuSmq52KCSDsaFsQ)
    │       │   └── M1-05-Reference (ID: urn:adsk.wipprod:fs.folder:co.Xfgs58IYTQm_mMvknOEklA)
    │       ├── M2_xxxxx(Milestone Name) (ID: urn:adsk.wipprod:fs.folder:co.4vZF2d2oS4-2hZk6GS7K5A)
    │       │   ├── M2-01-3D (ID: urn:adsk.wipprod:fs.folder:co.LE6qn2toRVCcu5Tn4ep5iw)
    │       │   ├── M2-02-2D (ID: urn:adsk.wipprod:fs.folder:co.K9ehlKAgSRCGcBWzAZez_w)
    │       │   ├── M2-03-J-DMS (if any) (ID: urn:adsk.wipprod:fs.folder:co.J_BpJRnLRrSrlctQ4hQkFg)
    │       │   ├── M2-04-Other (ID: urn:adsk.wipprod:fs.folder:co.-g3TgJ96Sl2sEHYctO3lBg)
    │       │   └── M2-05-Reference (ID: urn:adsk.wipprod:fs.folder:co.pUzsDWdETLOufPgux868BA)
    │       └── M3_xxxxx(Milestone Name) (ID: urn:adsk.wipprod:fs.folder:co.wQBX7my0RT-Rpwqg5mYmMQ)
    │           ├── M3-01-3D (ID: urn:adsk.wipprod:fs.folder:co.28OPEdkyS3udK46UUxihfQ)
    │           ├── M3-02-2D (ID: urn:adsk.wipprod:fs.folder:co.oEVBLb6XQj6aeXcIXGi0Ww)
    │           ├── M3-03-J-DMS (if any) (ID: urn:adsk.wipprod:fs.folder:co.sYUyaBYsTPCb6DMW401i3g)
    │           ├── M3-04-Other (ID: urn:adsk.wipprod:fs.folder:co.yGhoCla8TtmLCv8yo38cpA)
    │           └── M3-04-Reference (ID: urn:adsk.wipprod:fs.folder:co.jdIumJ5WRJiURDLyhI3LYA)
    ├── 30-Published (ID: urn:adsk.wipprod:fs.folder:co.gb7D-c41QiekUqO5pbYO0A)
    ├── 40-Archived (ID: urn:adsk.wipprod:fs.folder:co.mdOCUzm8STO7_H94qtgLAA)
    └── P00-Project Information (ID: urn:adsk.wipprod:fs.folder:co.PlYypjs-Rb-DEUoChxkx-g)
        ├── P00_Project Description (ID: urn:adsk.wipprod:fs.folder:co.XzBAXDETSmq9bnWy252nEQ)
        │   ├── P01_Project Brief (ID: urn:adsk.wipprod:fs.folder:co.LljzUAOHRSKP62Lo5nWCSA)
        │   │   ├── Unknown File (ID: urn:adsk.wipprod:dm.lineage:ZfpnXQhaQuyevw0C_UXusQ)
        │   │   └── Unknown File (ID: urn:adsk.wipprod:dm.lineage:3Rb7Qhh8QWiZvgdad39Smg)
        │   ├── P02_Execution Documents List (ID: urn:adsk.wipprod:fs.folder:co.mHetOjzoQbSu9g-BtAV9oQ)
        │   └── P03_RACI (ID: urn:adsk.wipprod:fs.folder:co.qCFXPlkMRf65r9P_2BOsTg)
        ├── P10_Client Requirements(ITB (ID: urn:adsk.wipprod:fs.folder:co.3Unf1VgpTRWesb24BO9RSA)
        │   └── EIR) (ID: urn:adsk.wipprod:fs.folder:co.GAfj9m0YQq6W0G8rjMBANQ)
        │       ├── P11_GENERAL (ID: urn:adsk.wipprod:fs.folder:co.CVIFom7NRceniCs9XtRtQg)
        │       │   └── P11_01_Project Schedule (ID: urn:adsk.wipprod:fs.folder:co.9pV18mkVQD-yHW6AfUMV4w)
        │       │       └── Milestone (ID: urn:adsk.wipprod:fs.folder:co.blE5QlMXQ9CmjXXG1Mqyhw)
        │       ├── P12_ARC (ID: urn:adsk.wipprod:fs.folder:co.OKYj3pgnSRmLWKv3HIdcBw)
        │       ├── P13_STR (ID: urn:adsk.wipprod:fs.folder:co.iYq7ZQI5QDeVeEoDgbs47w)
        │       ├── P14_HVAC (ID: urn:adsk.wipprod:fs.folder:co.CGkMmZIdSSONXqRqoRqXwQ)
        │       ├── P15_PLB (ID: urn:adsk.wipprod:fs.folder:co.waJ3fywKT5GFbemErjtYbA)
        │       ├── P16_ELE (ID: urn:adsk.wipprod:fs.folder:co.qTGrEf3NTmaALyRdvpFPkg)
        │       └── P17_FIRE (ID: urn:adsk.wipprod:fs.folder:co.0a_Ifa3JSmCwMi84-iFJgQ)
        ├── P20_Tender Documents (ID: urn:adsk.wipprod:fs.folder:co.yQW_Q6BzRNWkNjXxlpJZSQ)
        │   ├── P21_Pre-BEP (ID: urn:adsk.wipprod:fs.folder:co.lwoOSq_JSlWieyY3gA7lDQ)
        │   │   └── EIR (ID: urn:adsk.wipprod:fs.folder:co.Kjoie49CTAibhDd6gXwNsg)
        │   ├── P22_Organization&MemberList (ID: urn:adsk.wipprod:fs.folder:co.iN-WiRFlTG67DlDWxCYf2w)
        │   ├── P23_Capability Assessment (ID: urn:adsk.wipprod:fs.folder:co.tAE3DO08ScGTyZDDAObvIA)
        │   │   ├── P22_01_Task Team Capability Assessment (ID: urn:adsk.wipprod:fs.folder:co.LS_LzXRBSxyzD7EEyz17xQ)
        │   │   └── P22_02_Delivery Team Capability Assessment (ID: urn:adsk.wipprod:fs.folder:co.QSxFp2rNTDKao14RmSDsxw)
        │   ├── P24_Mobilization Plan (ID: urn:adsk.wipprod:fs.folder:co.2NclbkW_SEaoGFOVkvz8TA)
        │   ├── P25_Risk Register (ID: urn:adsk.wipprod:fs.folder:co.BboGPiJ9SPSI6qaOHEwcyA)
        │   ├── P26_Lessons Learned (ID: urn:adsk.wipprod:fs.folder:co.DLwEkQ36Q_qP_cbsDXtsqA)
        │   └── P27_High-Level Responsibility Matrix (ID: urn:adsk.wipprod:fs.folder:co.WrFgwKyHR2OtZOVT42CexA)
        ├── P30_Execution Documents (ID: urn:adsk.wipprod:fs.folder:co.UIwS9F_xTiaHS60SkvmMYA)
        │   ├── P31_BEP (ID: urn:adsk.wipprod:fs.folder:co.Y1T1QprqRhmjZwtfEJOteQ)
        │   │   └── Unknown File (ID: urn:adsk.wipprod:dm.lineage:Pv_y86kmQU6WJvAMmjTATA)
        │   ├── P32_Organization&MemberList (ID: urn:adsk.wipprod:fs.folder:co.aRiC4fZlQkiq6u9llBdk0Q)
        │   ├── P33_Capability Assessment (ID: urn:adsk.wipprod:fs.folder:co.z0GPxV6eReugwfIu5Bh24g)
        │   │   ├── P32_01_Task Team Capability Assessment (ID: urn:adsk.wipprod:fs.folder:co.vGX3TPptQY6zay6UVJlWuA)
        │   │   └── P32_02_Delivery Team Capability Assessment (ID: urn:adsk.wipprod:fs.folder:co.3Fm6nOvgQCqlUGCMOHb8oQ)
        │   ├── P34_Mobilization Plan (ID: urn:adsk.wipprod:fs.folder:co.6VZRbtxQR_OHGV7yXM1DQQ)
        │   ├── P35_Risk Register (ID: urn:adsk.wipprod:fs.folder:co.zSicP0pMTuq9tsQLo9kJcA)
        │   ├── P36_Lessons Learned (ID: urn:adsk.wipprod:fs.folder:co.Oi_VKe1UReGmfMe5slv-eQ)
        │   ├── P37_Detailed Responsibility Matrix (ID: urn:adsk.wipprod:fs.folder:co.fp01HE96RFC7eMU6wDue9g)
        │   ├── P38_MIDP (ID: urn:adsk.wipprod:fs.folder:co.zPyFHkpHT8C606QiCTGnuQ)
        │   │   └── TIDP (ID: urn:adsk.wipprod:fs.folder:co.or7ppIviQs6_oFWhMvFJAA)
        │   │       └── MDR (ID: urn:adsk.wipprod:fs.folder:co.PnuOYAWjQ8qpHuzvT6xYBw)
        │   └── P39_CDE Setup (ID: urn:adsk.wipprod:fs.folder:co.5J3v81YkR_i8KB5kaZSjGg)
        ├── P40_JGC BIM Standard (ID: urn:adsk.wipprod:fs.folder:co.et_OfARJTluoSwiDRTef1Q)
        │   ├── P41_International Standards (ID: urn:adsk.wipprod:fs.folder:co.LVhRg1c7RMG_gZVdRUXhMQ)
        │   ├── P42_ClientStandards (ID: urn:adsk.wipprod:fs.folder:co.a_0IkASlS-6TJXD0veS9Lg)
        │   └── P43_JGC Standards (ID: urn:adsk.wipprod:fs.folder:co.iSD-mDA_RAOPkvFJGlgy9w)
        │       ├── P43_01_Document Template (ID: urn:adsk.wipprod:fs.folder:co.h8ttwsWnT2SIp5L_ihkB6Q)
        │       ├── P43_02_Revit Template (ID: urn:adsk.wipprod:fs.folder:co.wzNxOi5iRr6lg9FQmxPYxg)
        │       ├── P43_03_Family Template (ID: urn:adsk.wipprod:fs.folder:co.frmdQ5tDSleHfwSeSALY0A)
        │       ├── P43_04_File Naming Convention (ID: urn:adsk.wipprod:fs.folder:co.rTfOgFkGQFuH78ME9xcFZg)
        │       ├── P43_05_Family Naming Convention (ID: urn:adsk.wipprod:fs.folder:co.de7igSfBS9iKvfscgAUL1Q)
        │       ├── P43_06_Tagging Rule (ID: urn:adsk.wipprod:fs.folder:co.PWN-k4zBTESxlxpbDJX7nA)
        │       ├── P43_07_Cllasification Code (ID: urn:adsk.wipprod:fs.folder:co.QCZZ5wZfR8WgwVKl1rO5Ow)
        │       └── P43_08_Check List (ID: urn:adsk.wipprod:fs.folder:co.ZygTue4lSg-rMPAvS5JBBA)
        └── P50_For Specific Organization (ID: urn:adsk.wipprod:fs.folder:co.cvUxeHiUQReAf6x1i0CFBQ)
```