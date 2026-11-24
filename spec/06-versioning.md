# 6. Versioning and compatibility

- Spec uses semantic versions (1.0, 1.1, 2.0). Every file states its spec version.
- Minor versions only add; readers ignore unknown fields.
- Objects made for 1.x open in every later 1.x reader.
- Long-term rule: files made today must still open in ten years.
