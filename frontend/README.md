Frontend for the application, using [SvelteKit](https://kit.svelte.dev/).

## Developing

We use pnpm. Install pnpm following [the instructions on the website](https://pnpm.io/installation). 

Then install dependencies with `pnpm install` (or `pnpm i`). Run the dev server with

```bash
pnpm dev

# or start the server and open the app in a new browser tab
pnpm dev -- --open
```

### Adding components

We use [shadcn-svelte](https://www.shadcn-svelte.com/docs) to add components. Search for a component there and run the appropriate command to install the component. 

## Building

Create a production version of the app:

```bash
pnpm build
```

Preview the production build with `pnpm preview`.
