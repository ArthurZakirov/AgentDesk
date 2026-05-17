# Bitwarden Secrets Manager Mapping

Bitwarden Secrets Manager import files are JSON objects with:

- `projects`: an array of project objects.
- `secrets`: an array of secret objects.

Each imported project uses:

```json
{
  "id": "00000000-0000-0000-0000-000000000001",
  "name": "Project Name"
}
```

Each imported secret uses:

```json
{
  "key": "ADC_PERSONAL_PROFILE_YAML",
  "value": "version: 1\n...",
  "note": "Personal profile YAML for form filling.",
  "id": "00000000-0000-0000-0000-000000000002",
  "projectIds": ["00000000-0000-0000-0000-000000000001"]
}
```

Rules from Bitwarden's import docs:

- Include a `projects` array even when it is empty.
- Include non-empty UUID-shaped `id` values. Bitwarden replaces them with real random IDs on import.
- A secret can be associated with only one project during import.
- Importing does not deduplicate existing objects, so repeated imports can create duplicates.

## Skill Convention

Store the entire personal profile YAML as one secret value:

- key: `ADC_PERSONAL_PROFILE_YAML`
- value: the private `personal-profile.yaml` file content
- note: `Personal profile YAML for form filling.`

This keeps the personal profile schema portable and avoids scattering personal facts across many secrets. Other skills consume the materialized local file at `$ADC_PERSONAL_PROFILE_PATH` or `~/.config/AgentDesk/personal-profile.yaml`.

## Direct CLI Convention

When a project already exists, prefer direct `bws` operations over repeated web imports:

```bash
export BWS_ACCESS_TOKEN="..."
export BWS_PERSONAL_PROFILE_PROJECT_ID="..."
profile_to_bws_secret.py ~/.config/AgentDesk/personal-profile.yaml --project-id "$BWS_PERSONAL_PROFILE_PROJECT_ID"
```

On another machine:

```bash
export BWS_ACCESS_TOKEN="..."
export BWS_PERSONAL_PROFILE_PROJECT_ID="..."
bitwarden_to_profile.py --from-bws-project-id "$BWS_PERSONAL_PROFILE_PROJECT_ID"
```
