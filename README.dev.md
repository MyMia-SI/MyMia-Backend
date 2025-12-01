# MyMia Backend — Developer README (Dev)

This document contains quick developer setup steps: local run, Firebase emulators, and testing.

## Local setup

1. Create `.env` from `.env.example` and populate values.
2. Install virtualenv and dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) Start Firebase Emulator Suite for Auth/Firestore/Storage.

4. Run API locally:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Tests

Run tests locally with pytest:

```bash
pytest
```

## Notes

- Use `README.md` for higher-level overview and design docs.
- Update `docs/` with architecture diagrams and exported PDFs.
