<!-- OPENLINE-GUIDE-VISUAL -->
![Brand Assets: company resource guide](https://raw.githubusercontent.com/askopenline/openline-brand-assets/main/.github/assets/guide-header.png)

# Openline Virtual-Office Interface Previews

Openline's public visual-reference collection for mini-apps designed for a WorkAdventure-based virtual office. These company-maintained previews illustrate interface patterns; they are not a jointly owned WorkAdventure product or evidence that every integration is implemented.

## Contents

| Location | Purpose |
| --- | --- |
| [`index.html`](index.html) | Preview launcher |
| [`apps/`](apps/) | Individual HTML interface references |
| [`apps/screenshots/`](apps/screenshots/) | Launcher thumbnails |
| [`apps/screenshots/full/`](apps/screenshots/full/) | Larger reference captures |
| [`sdk.html`](sdk.html) | Integration and component reference |
| [`links.html`](links.html) | Preview cross-reference |
| [`readme.html`](readme.html) | Historical visual catalogue |

Use the actual files and launcher as the current inventory. Historical HTML narratives and screenshots can describe earlier snapshots or simulated functionality.

## Preview locally

From this directory:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open [the local launcher](http://127.0.0.1:8000) and inspect the relevant page. Serve the collection together so relative links and assets resolve; a raw GitHub download URL is not an HTML hosting service.

## Design and implementation

The previews share dark navy surfaces, Openline orange accents, and the fonts and components defined by the supplied files. Reuse that visual language when extending the collection, but review each page's actual dependencies and behavior rather than assuming every app is self-contained or production-ready.

Before using a preview in the company office, validate authentication, persistence, data handling, external embeds, keyboard accessibility, and mobile sizing. Sample dashboards, integrations, and state changes must not be presented as connected business systems.

## Updating screenshots

Capture the actual served HTML after the relevant fonts and content load. Keep launcher thumbnails and larger reference images consistent with the changed source, and label any demonstration data appropriately.

The private [Openline virtual-office app repository](https://github.com/askopenline/openline-wa-apps) is maintained separately. Changes here do not automatically update that repository, the office deployment, or existing embeds.

## Attribution

Openline maintains its original interface work in this collection. WorkAdventure, external services, fonts, and other third-party resources retain their own ownership and terms; the presence of a logo or simulated integration does not establish endorsement.

<!-- OPENLINE-GUIDE-NAV -->
## Company reference

This guide belongs to [Openline Brand Assets](https://github.com/askopenline/openline-brand-assets), maintained by Openline. Return to the [project overview](../README.md) for the broader system, current company links, and release context.
