App side of Spectral, using [SvelteKit](https://kit.svelte.dev/).

Make sure to also read the [general README](../README.md).

---

The app is responsible not only for the UI, but also for most UX-related aspects.

That is, the app handles:

- General user interface
- Account system, login, etc.
- Managing the data in the db
- Storing state for sessions, modes and files
- Making requests to the kernel

However, the app is mostly responsible for providing an interface to easily create new modes of analysis, as components that display/visualize data fetched from the kernel.

## Contributing

For more info about how to contribute please refer to the CONTRIBUTING.md files:

- [General](./CONTRIBUTING.md)
- [App](./CONTRIBUTING.md)
- [Kernel](../kernel/CONTRIBUTING.md)

## Running standalone

The recommended way to run the app is with docker compose. However, if you want to run the app side by itself, you can do that by installing dependencies with `pnpm install` (or `pnpm i`) and running the dev server with

```bash
pnpm dev

# or start the server and open the app in a new browser tab
pnpm dev -- --open
```

### Building

Create a production version of the app:

```bash
pnpm build
```

Preview the production build with `pnpm preview`.
