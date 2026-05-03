# Supported Entities

Current support is experimental and rule-based / NLP-assisted.

## Usually masked

- persons;
- private organizations;
- passport numbers;
- INN;
- OGRN / OGRNIP;
- KPP;
- BIK;
- bank accounts;
- card numbers when detected with context;
- phones;
- emails;
- cadastral numbers;
- postal indexes with address context;
- sensitive dates such as birth dates and document issue dates;
- address details such as street, house, apartment.

## Usually kept

- public authorities;
- courts;
- tax authorities;
- country / region / city context where useful;
- ordinary contract / claim / procedural dates;
- service document numbers when recognized as such.

## Known gaps

- INN with spaces;
- INN with OCR-letter substitution;
- complex address fragments;
- scanned PDFs and images;
- token fragmentation for person aliases.
