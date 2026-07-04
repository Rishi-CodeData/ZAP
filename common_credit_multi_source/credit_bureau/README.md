## Design Decisions

### Schema Choices
We unified all bureau data into a common schema with the following fields:
- **applicant_id**: bureau‑specific identifier, kept flexible for numeric or alphanumeric formats.
- **name**: applicant’s full name, normalized for consistency.
- **normalized_score**: bureau scores mapped into a 0–1 range for comparability.
- **report_date**: standardized ISO date format.
- **date_of_birth** and **address**: added to strengthen reconciliation and reduce false merges when names are similar.
- **source**: tracks which bureau provided the record, enabling auditing and reconciliation.

### Extensibility
To add a new bureau:
1. Define its raw source in `pipeline.yaml` (format, path, file type).
2. Create an ingestion SQL script to load its raw data into a staging table.
3. Write a parser SQL script to map its fields into the unified schema.
4. Add these new steps to the orchestration flow.  
This modular design means new bureaus can be integrated without changing existing logic.

### One Limitation
While DOB and address greatly improve reconciliation, the pipeline still assumes these fields are consistently available and clean across bureaus. In real‑world data, missing or inconsistent values could cause under‑merging or false splits. I’m not fully satisfied with this dependency — ideally, the solution would include a more robust entity resolution layer that can handle incomplete or noisy data gracefully.
