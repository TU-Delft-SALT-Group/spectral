# How to makes issues and MRs

- **Type**: Choose Incident if it’s a bug, otherwise just a normal issue
- **Description**: Follow a template
- **Assignees**: assign yourself. if there is a person who is an expert in the topic, and will help you, you should also assign them
- **Reviewers**: Assign two people. If there is a particular person that should review, assign them. Otherwise assign people pseudo-arbitrarily, while trying to keep it evenly distributed.
- **Milestone**: one of MVP (0.1), 1.0
- **Iteration**: Corresponds to each weekly sprint (from 1 to 10, deadlines are on Mondays)
- **Labels**: any number of
    - `bug`: Report/fix of unexpected behavior
    - `feature`: New functionality for product
    - `suggestion`: Suggestion that needs to be reviewed by other team members
    - `build`: Related to the build process of the project
    - `ci`: Related to the continuous integration pipeline
    - `dependencies`: Related to the dependencies of the project (i.e., dep bump)
    - `help-wanted`: Would benefit from someone else
    - `needs-info`: Additional information is required
    - `acknowledged`: Author has requested input from another person, and that person has seen it and acknowledged it
    - `priority::`: one of
        - `P0(urgent)`
        - `P1(soon)`
        - `P2(eventually)`
        - `P3(not-scheduled)`
    - `domain::` one of
        - `kernel`
        - `app`
        - `docs` (have priority over the app/kernel)
    - `question`: Contains a question that needs to be answered to move forward the issue
    - `duplicate`: Seems to be a duplicate of another issue
    - `refactoring`: Rewrite that doesn’t change functionality
- **Weight**: number between 1 and 5, where 5 is “Cannot work on my feature before this is fixed” and 1 is “Don’t care, just a small nitpick”
- **Due date**: Set the due date, usually the end of the sprint (Monday evening)
- **Time tracking**: put the estimate of the time you spend on the project, and add the time you spent accordingly; make sure to add at least some time before closing the issue!
- **Confidentiality**: Always non-confidential for users with `developer` role.
- **Epics**: We decided that epics *do not* work for our workflow.

## Additional notes for issues

- When you close and issue, make sure to add a comment about why you are closing (e.g., “Closing as duplicate of …”) unless it is closed by an MR
- Make issues granular, and add child items and/or linked issues when appropriate

## Additional notes for MRs

- Try to merge MRs in 3 days or less. The limit is 5 days to merge an MR, otherwise we will just close it, as we don't want to clutter the repo with stale MRs (barring exceptional cases, that should be justified). To facilitate this...
- Make MRs as small as possible and generally self-contained.
- Squash commits if history is messy/too detailed.
