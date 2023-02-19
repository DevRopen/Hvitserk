## Feature

### Labels Plugin (`labels_v1`)

Ensures certain labels are present in your GitHub repository. This plugin can help maintain consistency and organization within the project by automatically checking for required labels and creating/updaing them as needed.


### Auto-Triage Plugin (`auto_triage_v1`)

Automatically applies labels to new issues and PRs based on predefined terms in their titles or bodies.


### Stale Plugin (`stale_v1`):

Helps maintainers manage inactive issues and pull requests in a GitHub repository by automatically identifying and handling stale items.

Key Features:

- Automatic Stale Detection: Marks issues as stale after a specified period of inactivity (60 days by default) and pull requests after 30 days.
- Automated Closure: Closes stale items if there’s no further activity within 7 days, keeping the repository clean.
- Labeling: Applies a `stale` label to inactive items for easy identification.
- Custom Comments: Posts informative comments when marking items as stale or closing them, encouraging contributors to re-engage.
- Exemption List: Allows certain labels (e.g., `pinned`, `security`) to exempt issues or PRs from being marked as stale.
