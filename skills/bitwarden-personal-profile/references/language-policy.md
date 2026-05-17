# Language Policy

Match the target form's language.

- Use `de` values for German forms.
- Use `en` values for English forms.
- Use `default` when the requested language is missing.
- Use plain strings as language-independent values.
- Keep proper nouns, legal names, company names, street names, URLs, emails, and phone numbers unchanged unless the profile explicitly provides localized variants.
- Keep official job titles unchanged when they are already the user's actual title. Use `generalProfession` when a form asks for a broad profession rather than an exact title.
- Format dates for the form locale: ISO internally, `DD.MM.YYYY` for German forms, and the form's visible convention for English forms.

Examples:

- `addressRegion.de = Bayern`, `addressRegion.en = Bavaria`
- `birthPlace.name = Magnitogorsk` stays unchanged.
- `birthPlace.country.de = Russland`, `birthPlace.country.en = Russia`
- `jobTitle = Junior Data Engineer` stays unchanged unless the user supplies a localized title.
