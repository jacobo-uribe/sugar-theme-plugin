# Store editing

How an agent reads and writes files on the user's Sugar Theme. Every skill that touches the theme follows this. The store is the only copy of the theme that counts; anything on the computer is a temporary working copy that exists for one task.

## The rules

1. **The project folder never holds theme files.** Working copies go in a scratch folder in the system temp directory.
2. **Pull only what the task touches.** Not the whole theme.
3. **Push only what you changed, and never let a push delete.** Always pass `--nodelete`.
4. **A scratch copy is valid for one task.** Pull again at the start of every task, even if a copy from an earlier task is still there.
5. **Clean up.** Delete the scratch folder when the task ends, and delete any leftover scratch from earlier tasks before starting a new one. Whoever starts next cleans up for whoever forgot.

## Which theme

The working theme's ID and the store come from the project's AGENTS.md. If they are missing, run `/sugar-theme:setup`. To see what is on the store:

```bash
shopify theme list --store STORE.myshopify.com
```

The first command against a store opens a browser sign-in; the user completes it once.

## The scratch folder

One folder per store and theme, under the system temp directory:

```
$TMPDIR/sugar-theme/STORE/THEME_ID/
```

On Windows use `%TEMP%`. Before pulling, delete anything already at that path, and any sibling folders left by earlier tasks.

## Pull

Download only the files the task needs. `--only` takes a path or a glob and can be repeated.

```bash
shopify theme pull --store STORE.myshopify.com --theme THEME_ID \
  --path "$TMPDIR/sugar-theme/STORE/THEME_ID" \
  --only templates/product.json --only sections/custom-columns.liquid
```

Pull the JSON template you are editing and every file you plan to change or read. A block or section file you intend to place in a template does not need pulling unless you will edit it.

## Edit

Work on the files in the scratch folder. Before pushing a JSON template, validate it: the file parses, every range value is inside its setting's min and max and on its step, and every block type is allowed by its parent. An invalid value does not error; the upload succeeds and the template silently renders wrong or not at all.

If the task runs long, pull the JSON template again right before you push it. The theme editor writes templates too, and a stale copy would overwrite what the user did meanwhile.

## Name what you place

Every section and block in a template can carry its own display name, separate from the file it comes from. The theme editor stores it as a `name` key on the entry:

```json
"hero_cmp": { "type": "classic-comparison", "name": "Comparison table · Javvy vs café", "settings": { … } }
```

Set it on everything you add or build. The editor's sidebar then reads like a page outline instead of a list of file names, so the user can find things at a glance and a later agent knows what each entry is for without opening it. Make the name specific: what it is and what it is for or where it sits, in the user's words. "Hero · comparison table" and "Under buy box · guarantee strip" beat "Custom Columns" and "Container". Keep it short enough to fit the sidebar, and put the same name in the custom-files log when the entry is a new file.

When the entry *is* a new file, tell the user the actual file name at delivery, plainly, next to the display name: "it's the block **Trust strip** in the sidebar, file `blocks/trust-strip.liquid`". The display name is how they find it in the editor; the file name is how they or a later agent find it everywhere else, and the two will usually differ.

## Push

Upload only the files you changed to the same theme.

```bash
shopify theme push --store STORE.myshopify.com --theme THEME_ID \
  --path "$TMPDIR/sugar-theme/STORE/THEME_ID" \
  --only templates/product.json --nodelete
```

- **`--nodelete` is not optional.** Without it, the CLI deletes every remote file that is not in the scratch folder, and the scratch folder holds three files.
- **Pushing to the live theme needs `--allow-live`.** Only do this when the working theme policy in AGENTS.md is *edit directly*, and say so to the user before the push.
- A rejected push prints the error (a Liquid syntax problem, a schema the platform refuses). The theme keeps its previous version. Fix the file and push again.

## Duplicate first

When the policy is *duplicate first* and no working copy exists yet:

```bash
shopify theme duplicate --store STORE.myshopify.com --theme LIVE_THEME_ID --name "NAME"
```

Record the new theme's ID in AGENTS.md as the working theme. The user publishes it from the admin when they are happy.

## Preview and review links

Hand the user a **theme editor deep link** to the exact theme and page. They see the full page and can add or remove things themselves:

```
https://STORE.myshopify.com/admin/themes/THEME_ID/editor?previewPath=%2Fproducts%2FHANDLE
```

Encode the path. To open an alternate template, include its `view` query in the path: `%2Fproducts%2FHANDLE%3Fview%3Dvariations`.

For your own checks in the headless browsers, and for anything the editor cannot show (checkout, an app block that needs a real session), use the storefront preview link:

```
https://STORE.myshopify.com/products/HANDLE?preview_theme_id=THEME_ID
```

On a password-protected store each headless browser keeps its own login; the user entered the password once per browser during setup.

## When a full local copy is needed

Some work wants the CLI's local preview server, which reloads as you edit and needs no storefront password:

```bash
shopify theme dev --store STORE.myshopify.com --theme THEME_ID --path "$TMPDIR/sugar-theme/STORE/THEME_ID"
```

It requires the whole theme in the scratch folder, so pull without `--only` first. It uploads the scratch folder to the theme it is pointed at as you edit, so point it at the working theme, never the live one. Treat the full copy like any other scratch: valid for this task, deleted at the end.

## Cleanup

```bash
rm -rf "$TMPDIR/sugar-theme/STORE/THEME_ID"
```

Run it when the task ends, and run it for any leftover folder under `$TMPDIR/sugar-theme/` at the start of the next task. Screenshots the user should keep go in the project folder, not the scratch.
