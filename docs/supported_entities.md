# Supported Entities

Current support is experimental and rule-based / NLP-assisted.

## Usually masked

- persons;
- private organizations;
- passport numbers, including separated series/number forms with explicit passport context;
- SNILS with common hyphenated or spaced formatting;
- INN;
- OGRN / OGRNIP, including spaced forms with explicit labels;
- KPP, including spaced forms with explicit labels;
- BIK, including spaced forms with explicit labels;
- bank accounts;
- card numbers when detected with context;
- phones;
- emails;
- cadastral numbers;
- postal indexes with address context;
- sensitive dates such as birth dates, registration dates and document issue dates;
- address details such as street, house, apartment.

## Usually kept

- public authorities;
- courts;
- tax authorities;
- country / region / city context where useful;
- ordinary contract / claim / procedural dates;
- service document numbers when recognized as such.

## Known limitations / remaining weak spots

- complex address fragments;
- scanned PDFs and images;
- token fragmentation for person aliases;
- contextual re-identification risks;
- false positives and false negatives in unseen drafting patterns.

Former synthetic XFAIL cases fixed in Sprint 0.6:

- INN with spaces;
- INN with OCR-letter substitution.

Sprint 1.1 quality pack adds synthetic coverage for common formatting variants in SNILS, passports, BIK/KPP/OGRN, address context, mobile phones, private organizations and sensitive dates.