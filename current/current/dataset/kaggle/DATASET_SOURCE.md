# Kaggle Fake and Real News Benchmark Dataset

## 1. Provenance and Source Details

- **Dataset Name**: Fake and Real News Dataset (ISOT Fake News Dataset)
- **Primary Source**: University of Victoria ISOT Research Lab / Kaggle
- **Kaggle URL**: [https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset)
- **Original Authors**: H. Ahmed, I. Traore, and S. Saad ("Detecting opinion spams and fake news using text classification", *Security and Privacy*, 2018).
- **License**: Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)

## 2. Original vs. Harmonized Schema

Original Kaggle schema consisted of two distinct files:
- `Fake.csv` (Columns: `title`, `text`, `subject`, `date`) -> mapped to `label = 0`, `label_name = 'FAKE'`
- `True.csv` (Columns: `title`, `text`, `subject`, `date`) -> mapped to `label = 1`, `label_name = 'REAL'`

### Normalized Project Schema:

| Target Column | Source Column | Transformation Rule |
| :--- | :--- | :--- |
| `news_id` | Auto-generated | `KAG-<0001..N>` zero-padded unique identifier |
| `title` | `title` | Trimmed, UTF-8 clean, HTML entity decoded |
| `article` | `text` | Trimmed, Reuters prefix stripped where present |
| `category` | `subject` | Standardized category ('politics', 'world', 'news') |
| `source` | Auto-assigned | `"ISOT/Reuters"` (True) or `"Kaggle/FakeNews"` (Fake) |
| `label` | Origin file | `0` = FAKE, `1` = REAL |
| `label_name` | Derived | `"FAKE"` or `"REAL"` |

## 3. How to Update or Download Full Kaggle Dataset

1. Visit the Kaggle URL: `https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset`
2. Download `True.csv` and `Fake.csv`.
3. Run the validation and ingestion script:
   ```bash
   python scripts/validate_datasets.py
   python scripts/create_hybrid_dataset.py
   ```
4. If working offline, the system provides a curated development benchmark subset in `kaggle_news.csv` ready for immediate training and reproducibility.
