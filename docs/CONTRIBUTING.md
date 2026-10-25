# Contributing to Openline Brand Assets

This document outlines the process for contributing to the Openline brand asset repository. The repository serves as the canonical source for Openline's brand identity, including visual assets, motion graphics, and guidelines.

## Repository Structure

*   `brand-library/`: Contains the current application source for the brand portal.
*   `launch-studio/`: Retained historical application source.
*   `docs/`: Documentation files, including this guide.
*   `library/productions/`: Contains production-ready assets.

## Asset Hydration

Many large binary assets are not stored directly in the Git repository. Instead, they are distributed from `brand.openline.com` and managed via a hydration process. To obtain a complete gallery of assets after cloning the repository, you must perform hydration.

*   **Hydration Manifest:** `brand-library/PUBLIC-ASSETS.json` lists the assets to be downloaded.
*   **Hydration Tool:** `brand-library/tools/hydrate-public.py` is used to download the assets.

**Note:** A clean clone of the repository will not contain all binary files. Hydration is a user-initiated process that downloads multi-gigabyte files only when chosen.

## Development Workflow

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/askopenline/openline-brand.git
    cd openline-brand
    ```
2.  **Install Dependencies:** Refer to `brand-library/README.md` for specific application dependencies.
3.  **Hydrate Assets (if needed):**
    ```bash
    cd brand-library
    python tools/hydrate-public.py --download
    # Optionally, specify a prefix for retrieval:
    # python tools/hydrate-public.py --download --prefix library/productions/motion-150/
    ```
    Running `python tools/hydrate-public.py` without `--download` will display inventory only.
4.  **Make Changes:** Implement your contributions, ensuring adherence to Openline brand guidelines.
5.  **Test Locally:** Verify your changes within the `brand-library` application.
6.  **Prepare Handoff:** Local source handoff is prepared. Fly publication and GitHub synchronization are separate processes.

## Guidelines for Contributions

*   **Brand Consistency:** All contributions must align with Openline's established brand guidelines.
*   **File Formats:** Use approved file formats for assets (e.g., MP4/AAC for motion, FLAC for sound, JPEG/GIF for images).
*   **Documentation:** Update relevant documentation (`docs/`) for any new assets or significant changes.
*   **No Runtime AI Calls or Database:** The brand portal operates statically without runtime AI calls or a database.
*   **Exclusions:** Secrets, provider payloads, receipts, and raw unapproved generations are excluded from the repository.

## Repository Access

Currently, the GitHub connection is configured for READ access. Repository write/push operations are separately unconfirmed through this connection. Local source handoff is the primary method for preparing contributions for publication.