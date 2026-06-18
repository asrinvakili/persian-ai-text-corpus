# پیکره فارسی متن انسانی و هوش مصنوعی

پیکره موازی فارسی برای محک‌زنی روش‌های تشخیص متن تولیدشده توسط هوش مصنوعی. هر موضوع در چهار نسخه ارائه شده است: یک متن انسانی و سه متن تولیدشده توسط مدل‌های زبانی بزرگ متفاوت.

[![License: CC BY-SA 4.0](https://img.shields.io/badge/Data-CC%20BY--SA%204.0-blue.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![License: MIT](https://img.shields.io/badge/Code-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Records](https://img.shields.io/badge/records-4000-green.svg)](#ساختار-پیکره)

فارسی | [English](README.md)

---

## انگیزه پژوهشی

بیشتر دیتاست‌های تشخیص متن هوش مصنوعی، انگلیسی یا چینی‌اند. زبان فارسی (و خانواده گسترده‌تر زبان‌های با خط فارسی-عربی) از این نظر کم‌منبع است. این پیکره یک محک کنترل‌شده برای سه پرسش پژوهشی فراهم می‌کند:

۱. **تشخیص:** آیا یک طبقه‌بند می‌تواند به‌طور قابل اتکا، خروجی LLM فارسی را از نگارش انسانی تمیز دهد؟  
۲. **تحلیل مولدی:** کدام مولد سخت‌ترین تشخیص را دارد؟  
۳. **تعمیم‌پذیری:** آیا آموزش روی چند مولد، به مولد دیده‌نشده منتقل می‌شود؟

**طرح تطبیقی** — تولید هر موضوع توسط همه مدل‌ها — خطای پنهان موضوع را در مقایسه مولدها حذف می‌کند.

---

## ساختار پیکره

| منبع | تعداد | مبدأ |
| --- | ---: | --- |
| انسان (ویکی‌پدیای فارسی، نسخه‌های پیش از ۲۰۲۰) | ۱٬۰۰۰ | استخراج مستقیم با `revision_id` |
| DeepSeek v3.1 | ۱٬۰۰۰ | دروازه AvalAI |
| GPT-4o-mini | ۱٬۰۰۰ | دروازه AvalAI |
| Gemini 2.5 Flash-Lite | ۱٬۰۰۰ | دروازه AvalAI |
| **مجموع** | **۴٬۰۰۰** | |

**پوشش حوزه‌ای.** پنج حوزه، هر کدام ۲۰۰ موضوع: علوم نظری، علوم مهندسی، علوم پزشکی، علوم انسانی، تاریخ و زندگی‌نامه.

**توزیع طول.**
- انسان: میانگین ۷۴٫۷ کلمه (σ=۳۲٫۷)، دامنه ۴۰–۲۵۱.
- AI: میانگین ۶۶٫۸ کلمه (σ=۲۹٫۱)، دامنه ۲۲–۲۳۳.

**تقسیم پیش‌فرض.** آموزش ۷۰٪ / اعتبارسنجی ۱۰٪ / آزمون ۲۰٪ — لایه‌بندی‌شده بر اساس (برچسب، دسته، مدل).

جزئیات کامل در [`docs/datasheet.md`](docs/datasheet.md).

---

## ساختار پوشه

```
persian-ai-text-corpus/
├── data/
│   ├── splits/                # تقسیم آماده برای آموزش مستقیم مدل
│   │   ├── train.jsonl        # ۲٬۸۰۰ رکورد
│   │   ├── val.jsonl          #   ۴۰۰ رکورد
│   │   └── test.jsonl         #   ۸۰۰ رکورد
│   ├── full/                  # کل پیکره، تفکیک‌شده بر اساس منبع
│   │   ├── human_texts.jsonl  # ۱٬۰۰۰ رکورد
│   │   └── ai_texts.jsonl     # ۳٬۰۰۰ رکورد (هر مدل ۱٬۰۰۰)
│   └── dataset_stats.json     # آمار کامل
├── examples/
│   ├── load_dataset.py        # بارگذار کوتاه برای PyTorch و Hugging Face
│   └── merge_full.py          # ساخت یک فایل ادغام‌شده از full/
├── docs/
│   └── datasheet.md           # مستندات استاندارد Datasheets-for-Datasets
├── README.md                  # نسخه انگلیسی
├── README.fa.md               # این فایل
├── LICENSE
└── CITATION.cff
```

---

## ساختار داده

هر خط در فایل‌های JSONL یک رکورد است با فیلدهای زیر.

### رکورد انسانی

```json
{
  "id": "0001",
  "human_id": "0001",
  "label": 0,
  "source": "human",
  "category": "علوم نظری",
  "subcategory": "نابرابری‌ها",
  "title": "نابرابری مارکوف",
  "num_words": 62,
  "revision_id": 27800612,
  "revision_date": "2019-12-13T05:18:36Z",
  "url": "https://fa.wikipedia.org/w/index.php?oldid=27800612",
  "text": "..."
}
```

### رکورد AI

```json
{
  "id": "ai_0001",
  "human_id": "0001",
  "label": 1,
  "source": "ai",
  "model": "deepseek-v3.1",
  "category": "علوم نظری",
  "subcategory": "نابرابری‌ها",
  "title": "نابرابری مارکوف",
  "num_words": 56,
  "target_words": 62,
  "generation_date": "2026-06-17",
  "text": "..."
}
```

فیلد `human_id` کلید اتصال است. هر رکورد انسانی دقیقاً سه رکورد AI متناظر دارد که `human_id` یکسانی دارند.

---

## شروع سریع

### با کتابخانه استاندارد پایتون

```python
import json

def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

train = load_jsonl("data/splits/train.jsonl")
print(f"{len(train)} رکورد، فیلدها: {list(train[0].keys())}")
```

### با کتابخانه Hugging Face Datasets

```python
from datasets import load_dataset

ds = load_dataset(
    "json",
    data_files={
        "train": "data/splits/train.jsonl",
        "validation": "data/splits/val.jsonl",
        "test": "data/splits/test.jsonl",
    },
)
print(ds)
```

### جفت‌کردن انسان و AI برای تحلیل تطبیقی

```python
import json
from collections import defaultdict

humans = {r["human_id"]: r for r in load_jsonl("data/full/human_texts.jsonl")}
ai_by_hid = defaultdict(list)
for r in load_jsonl("data/full/ai_texts.jsonl"):
    ai_by_hid[r["human_id"]].append(r)

# هر متن انسانی دقیقاً ۳ نسخه AI متناظر دارد
hid = "0001"
print(humans[hid]["text"])
for ai in ai_by_hid[hid]:
    print(f"[{ai['model']}] {ai['text']}")
```

اسکریپت کامل بارگذار در [`examples/load_dataset.py`](examples/load_dataset.py).

---

## عدم تعادل کلاس — قبل از آموزش بخوانید

طرح تطبیقی نسبت کلاس ۱:۳ ایجاد می‌کند (۱٬۰۰۰ انسان در برابر ۳٬۰۰۰ AI). برای آموزش طبقه‌بند متعادل، یکی از دو راه را انتخاب کنید:

**گزینه الف — وزن‌دهی کلاس (توصیه‌شده).**
وزن کلاس انسان را ۳ برابر بگذارید. همه داده حفظ می‌شود و مدل از هر نمونه یاد می‌گیرد.

```python
# PyTorch
import torch.nn as nn
criterion = nn.CrossEntropyLoss(weight=torch.tensor([3.0, 1.0]))

# scikit-learn
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(class_weight={0: 3.0, 1: 1.0})
```

**گزینه ب — زیرنمونه‌گیری به نسبت ۱:۱.**
از هر `human_id`، فقط یک نسخه AI تصادفی نگه دارید. نتیجه: ۱٬۰۰۰ + ۱٬۰۰۰ = ۲٬۰۰۰ رکورد.

```python
import random
rng = random.Random(42)
balanced_ai = [rng.choice(ai_by_hid[hid]) for hid in humans]
```

برای **تحلیل تطبیقی مولدها** (کدام مدل سخت‌تر تشخیص داده می‌شود)، از مجموع کامل ۳٬۰۰۰تایی AI استفاده کنید.

---

## آزمایش‌های پیشنهادی

- **تشخیص پایه:** تنظیم دقیق ParsBERT روی `train.jsonl` و ارزیابی روی `test.jsonl`.
- **آزمون حذفی روی مولدها:** آموزش روی یک مدل تنها؛ آزمون روی هر مدل کنارگذاشته‌شده.
- **مقاومت در برابر بازنویسی:** اعمال ترجمه برگشتی (مثل `persiannlp/mt5-small-parsinlu`) روی مجموعه آزمون و ارزیابی مجدد.
- **دقت بر اساس حوزه:** گروه‌بندی `test.jsonl` بر اساس `category`؛ یافتن حوزه‌هایی که طبقه‌بند ضعیف عمل می‌کند.

---

## محدودیت‌ها

- **حوزه:** فقط نثر دانشنامه‌ای؛ فارسی محاوره‌ای و گویشی موجود نیست.
- **پوشش مولدها:** سه LLM پیشرو از طریق AvalAI در ژوئن ۲۰۲۶. مدل‌هایی مثل Claude، Llama و LLMهای بومی فارسی شامل نیستند.
- **زمانی:** مولدها در حال تکامل‌اند؛ این عکس فوری وضعیت ژوئن ۲۰۲۶ است.
- **عدم تعادل:** ذاتی طرح تطبیقی است (بالا توضیح داده شد).
- **تنوع پزشکی:** حوزه پزشکی تنوع زیرحوزه‌ای کمتری دارد (۶۶۹ نامزد مقاله در برابر ۱۲۰۰ در سایر حوزه‌ها).

---

## مجوز

- **کد** (`examples/`): MIT.
- **متن‌های انسانی** (`data/full/human_texts.jsonl`): CC BY-SA 4.0، به ارث‌رسیده از ویکی‌پدیای فارسی. ذکر منبع و انتشار با مجوز مشابه الزامی است.
- **متن‌های AI** (`data/full/ai_texts.jsonl`): مشروط به شرایط استفاده هر ارائه‌دهنده (OpenAI، DeepSeek، Google). برای پژوهش آکادمیک منتشر شده.

برای متن کامل [`LICENSE`](LICENSE) را ببینید.

---

## استناد

```bibtex
@misc{vakili2026persianaitext,
  author       = {Vakili, Asrin},
  title        = {Persian AI-Text Corpus: A Parallel Dataset for AI-Generated Text Detection in Persian},
  year         = {2026},
  publisher    = {GitHub},
  howpublished = {\url{https://github.com/asrinvakili/persian-ai-text-corpus}}
}
```

---

## ریپوی مرتبط

کد تولیدکننده این پیکره در ریپوی جداگانه‌ای قرار دارد: [`persian-ai-text-detection`](https://github.com/asrinvakili/persian-ai-text-detection). از آن برای بازتولید داده از ابتدا یا تولید نسخه‌های دیگر با مدل‌های متفاوت استفاده کنید.

---

## تماس

**اسرین وکیلی** — گروه مهندسی کامپیوتر، دانشگاه ملی مهارت، تهران، ایران.

برای پرسش یا گزارش مشکل، یک [Issue](https://github.com/asrinvakili/persian-ai-text-corpus/issues) باز کنید.
