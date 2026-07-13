# TSETMC Flow & yVal Codes

## Flow Codes (بازار / Market Type)

| Code | Persian | English |
|------|---------|---------|
| 0 | عمومی | General / All (contains both بورس and فرابورس) |
| 1 | بورس اوراق بهادار تهران | TSE Main Board |
| 2 | فرابورس ایران | Iran Fara Bourse (OTC) |
| 3 | آتی / مشتقه / بدهی | Futures / Derivatives / Debt |
| 4 | بازار پایه | UTP / Unlisted Trading Privileges |
| 6 | بورس انرژی | Energy Exchange |
| 7 | بورس کالا | Mercantile / Commodities (IME) |
| 18 | صندوق‌های سرمایه‌گذاری | ETFs / Investment Funds |
| 19 | بازار حرفه‌ای | Professional Market |

## yVal Codes (نوع دارایی / Asset Type)

The `yVal` field in instrument info and market watch data identifies the type of instrument.

| yVal | Persian | English |
|------|---------|---------|
| 300 | سهام | Common Stock (سهم) |
| 301 | حق تقدم | Preemptive Right (حق تقدم سهام) |
| 302 | حق تقدم تسهیلات | Preemptive Right (Facilities) |
| 303 | واحد سرمایه‌گذاری | Investment Unit |
| 306 | مهرایران | Mehr Iran (specific fund type) |
| 309 | اوراق اجاره | Leasing Certificates |
| 310 | اوراق مشارکت | Participation Bonds |
| 311 | صکوک اجاره | Sukuk Ijara |
| 312 | صکوک مرابحه | Sukuk Murabaha |
| 313 | اوراق گواهی سپرده | Certificate of Deposit |
| 316 | اختیار خرید تبعی | Put/Call Warrants |
| 317 | بیمه نامه | Insurance Policy |
| 318 | اوراق منفعت | Benefit Certificates |
| 319 | صندوق پروژه | Project Fund |
| 321 | صندوق جسورانه | Venture Capital Fund |
| 327 | شیشه01ن | Specific type |
| Various | Various fund types | ETF, Fund units, etc. |

## cgrValCot Codes (گروه بازار / Market Group)

| Code | Persian | English |
|------|---------|---------|
| N1 | بازار اول (تابلوی اصلی) | First Market (Main Board) |
| N2 | بازار دوم (تابلوی فرعی) | Second Market (Sub Board) |
| N3 | بازار سوم | Third Market |
| F1 | بازار اول فرابورس | Fara Bourse First Market |
| F2 | بازار دوم فرابورس | Fara Bourse Second Market |
| F3 | بازار سوم فرابورس | Fara Bourse Third Market |

## cEtaval Codes (وضعیت نماد / Instrument Status)

| Code | Persian | English |
|------|---------|---------|
| A | مجاز | Permitted (Trading) |
| AS | مجاز-تعلیق | Permitted-Suspended |
| M | ممنوع | Forbidden (Halted) |
| MS | ممنوع-تعلیق | Forbidden-Suspended |
| AG | مجاز-محاق | Permitted-Eclipse |
| MG | ممنوع-محاق | Forbidden-Eclipse |

## FlowTitle Values (نام بازار)

| Value | Persian |
|-------|---------|
| بازار بورس | TSE Main Board |
| بازار فرابورس | Fara Bourse |
| بازار پایه | UTP / Base Market |
| بازار آتی | Futures Market |
| بازار صندوق‌ها | Fund Market |
| بازار کالا | Commodities Market |

## cgrValCotTitle Values

| Value | Persian |
|-------|---------|
| بازار اول (تابلوی اصلی) بورس | First Market Main Board |
| بازار دوم (تابلوی فرعی) بورس | Second Market Sub Board |
| بازار اول فرابورس | Fara Bourse First Market |
| بازار دوم فرابورس | Fara Bourse Second Market |
| بازار سوم فرابورس | Fara Bourse Third Market |

## cComVal Codes (شرکت / Company Type)

| Code | Meaning |
|------|---------|
| 1 | تولیدی (Manufacturing) |
| 2 | خدماتی (Services) |
| 3 | مالی (Financial) |
| 4 | سرمایه‌گذاری (Investment) |

## sourceID Values

| Source | Description |
|--------|-------------|
| 1 | TSETMC |
| 2 | Fara Bourse |
| 3 | Energy Exchange |